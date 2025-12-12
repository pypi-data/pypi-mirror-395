import os
import re
import sys
import tempfile
from typing import Any, List, Dict
from urllib.request import urlopen
from zipfile import ZipFile

from dotenv import load_dotenv
from requests_toolbelt import sessions
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.entities import Entities
from pipebio.jobs import Jobs
from pipebio.models.export_format import ExportFormat
from pipebio.models.job_type import JobType
from pipebio.models.upload_detail import UploadDetail
from pipebio.organization_lists import OrganizationLists
from pipebio.sequences import Sequences
from pipebio.shareables import Shareables
from pipebio.util import Util
from pipebio.workflows import Workflows
import importlib.metadata

class PipebioClient:
    session: BaseUrlSession
    shareables: Shareables
    entities: Entities
    jobs: Jobs
    sequences: Sequences
    organization_lists: OrganizationLists
    workflows: Workflows
    user: Any

    _url: str
    _is_aws: bool

    def __init__(self, url: str = None):
        __version__ = importlib.metadata.version("pipebio")
        print(f"PipeBio SDK version {__version__}")
        self._is_aws = None
        self._url = url
        # Get the path of the script that instantiated this.
        path = os.path.dirname(sys.argv[0])
        # Join with .env
        full_path = os.path.join(os.path.abspath(path), '.env')
        # attempt to load a .env file
        load_dotenv(full_path)

        benchling_s2s_token = os.environ['BENCHLING_S2S_TOKEN'] if 'BENCHLING_S2S_TOKEN' in os.environ else None
        api_key = os.environ['PIPE_API_KEY'] if 'PIPE_API_KEY' in os.environ else None
        # User tokens are used by plugins running inside PipeBio and only ever set by Pipebio.
        # They are never used by users directly, they should always use PIPE_API_KEY.
        user_token = os.environ['USER_TOKEN'] if 'USER_TOKEN' in os.environ else None

        if api_key is None and user_token is None and benchling_s2s_token is None:
            print(f'PIPE_API_KEY={api_key}')
            raise Exception('PIPE_API_KEY required.')

        if url is None:
            raise Exception('url required.')

        base_url = f'{url}/api/v2/'

        self.session = sessions.BaseUrlSession(base_url=base_url)

        # Set Bearer token header with API KEY, Benchling S2S token or USER TOKEN.
        if user_token is not None:
            self.session.headers.update({"Authorization": f"Bearer {user_token}"})
        elif benchling_s2s_token is not None:
            self.session.headers.update({"Authorization": f"Bearer {benchling_s2s_token}"})
        else:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

        # Will also check api_key and fail fast, with friendly error is auth fails.
        self.user = self.get_user()
        print(f'\nUsing api key for {self.user["firstName"]} {self.user["lastName"]}.\n')
        self.shareables = Shareables(self.session)
        self.entities = Entities(self.session)

        job_id = os.environ['JOB_ID'] if 'JOB_ID' in os.environ else None
        self.jobs = Jobs(self.session, self.user, job_id)
        self.sequences = Sequences(self.session, self.is_aws)
        self.organization_lists = OrganizationLists(self.session, self.user)
        self.workflows = Workflows(self.session, self.organization_lists, self.user, self.jobs)

    @staticmethod
    def sanitize_baseurl(url: str) -> str:
        url = url.strip()

        if not url.startswith("https://"):
            raise ValueError(
                "Base URL must start with 'https://'. Please provide a full URL like 'https://app.pipebio.com' or 'https://your-company.pipebio.benchling.com'")

        if url != "https://" and url.endswith("/"):
            url = url[:-1]

        return url

    def get_user(self):
        response = self.session.get('me')
        if response.status_code == 401:
            raise ValueError('Failed to authenticate, please check PIPE_API_KEY')
        user = response.json()
        return user

    def upload_file(self,
                    file_name: str,
                    absolute_file_location: str,
                    parent_id: str,
                    project_id: str,
                    organization_id: str = None,
                    details: List[UploadDetail] = None,
                    file_name_id: str = None,
                    poll_job: bool = False):
        print('  Creating signed upload.')
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self.user)

        response = self.jobs.create_signed_upload(
            file_name=file_name,
            parent_id=parent_id,
            project_id=project_id,
            details=details,
            file_name_id=file_name_id,
            organization_id=_organization_id,
        )

        url = response['data']['url']
        job = response['data']['job']
        job_id = job['id']
        headers = response['data']['headers']

        self.jobs.upload_data_to_signed_url(absolute_file_location, url, headers)
        print('  Upload complete. Parsing contents.')

        if poll_job:
            return self.jobs.poll_job(job_id)
        else:
            return job

    def export(self,
               entity_id: str,
               format: ExportFormat,
               destination_folder: str = None,
               destination_filename: str = None,
               params: dict = None):
        entity = self.entities.get(entity_id)
        entity_name = entity['name']
        user = self.user

        params = {} if params is None else params
        params["format"] = format.value if 'format' not in params else params['format']
        params["fileName"] = entity_name if 'fileName' not in params else params['fileName']

        destination_filename = destination_filename if destination_filename else entity_name
        print(f'Exporting {entity_id} to {destination_folder}/{destination_filename}')
        job_id = self.jobs.create(
            owner_id=user['org']['id'],
            shareable_id=entity['ownerId'],
            job_type=JobType.ExportJob,
            name='Export from python client',
            input_entity_ids=[entity_id],
            params=params,
        )

        # Wait for the file to be converted to Genbank.
        job = self.jobs.poll_job(job_id)

        links = job['outputLinks']

        outputs = []

        for link in links:
            destination = os.path.join(destination_folder, destination_filename)
            response = urlopen(link['url'])
            with open(destination, 'wb') as file:
                file.write(response.read())
            outputs.append(destination)

        return outputs

    @staticmethod
    def _get_file_list(filename_pattern: str,
                       local_folder_path: str):
        """
        Helper function for getting file list from local folder.
        :param filename_pattern:
        :param local_folder_path:
        :return:
        """
        if filename_pattern is not None:
            try:
                re.compile(filename_pattern)
            except re.error:
                raise ValueError('Invalid filename_pattern')

        local_files_to_upload: List[Dict[str, str]] = []
        for (dir_path, dir_names, filenames) in os.walk(local_folder_path):
            for filename in filenames:
                if filename_pattern is None or re.search(filename_pattern, filename):
                    local_files_to_upload.append({
                        'filename': filename,
                        'full_path': os.path.join(local_folder_path, filename)
                    })

        local_file_count = len(local_files_to_upload)
        if local_file_count == 0:
            raise ValueError(f'No files to upload, is the folder empty or your filename_pattern '
                             f'"{filename_pattern}" incorrect?')

        return local_files_to_upload

    def upload_files(self,
                     absolute_folder_path: str,
                     parent_id: str,
                     project_id: str,
                     organization_id: str = None,
                     filename_pattern: str = None,
                     poll_jobs: bool = False):
        """
        Uploads a number of files from a folder.
        Useful for uploading a number of files to a single document e.g. ab1 files.
        :param absolute_folder_path: Full path to folder containing files to upload.
        :param parent_id:
        :param project_id:
        :param organization_id:
        :param filename_pattern: A regular expression pattern to match filenames e.g. ''.*.(ab1)''
        :param poll_jobs:
        :return:
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self.user)

        local_files_to_upload = self._get_file_list(filename_pattern, absolute_folder_path)
        local_file_count = len(local_files_to_upload)
        print(f'Uploading {local_file_count} files')

        # Upload the data, but don't wait for parsing to complete. Just to be efficient.
        index = 1
        upload_ids = []
        upload_jobs = []
        for local_file in local_files_to_upload:
            filename = local_file['filename']
            print(f'Uploading file {index}/{local_file_count} ({filename})')

            upload_job = self.upload_file(
                # Friendly name that will be shown in PipeBio ui.
                file_name=filename,
                # Path on local disk.
                absolute_file_location=local_file['full_path'],
                # Optional.
                parent_id=parent_id,
                project_id=project_id,
                organization_id=_organization_id,
            )

            upload_ids.append(upload_job['id'])
            upload_jobs.append(upload_job)
            index += 1

        if poll_jobs:
            jobs = self.jobs.poll_jobs(upload_ids, None)
            print('  Finished uploading files.')
            return jobs
        else:
            print('  Uploading files.')
            return upload_jobs

    def upload_files_as_zip(self,
                            absolute_folder_path: str,
                            parent_id: str,
                            project_id: str,
                            organization_id: str = None,
                            filename_pattern: str = None,
                            poll_jobs: bool = False):
        """
        Uploads files, firstly zipping them into a single file.
        Useful for uploading a number of files to a single document e.g. ab1 files.
        :param absolute_folder_path: Full path to folder containing files to upload.
        :param parent_id:
        :param project_id:
        :param organization_id:
        :param filename_pattern: A regular expression pattern to match filenames e.g. ''.*.(ab1)''
        :param poll_jobs:
        :return:
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self.user)

        local_files_to_upload = self._get_file_list(filename_pattern, absolute_folder_path)
        local_file_count = len(local_files_to_upload)
        print(f'Uploading {local_file_count} files')

        file = tempfile.NamedTemporaryFile()
        with ZipFile(file.name, 'w') as zip_file:
            for local_file in local_files_to_upload:
                zip_file.write(filename=local_file['full_path'], arcname=local_file['filename'])

        upload_job = self.upload_file(
            # Friendly name that will be shown in PipeBio ui.
            file_name=os.path.basename(absolute_folder_path),
            # Path on local disk.
            absolute_file_location=file.name,
            # Optional.
            parent_id=parent_id,
            project_id=project_id,
            organization_id=_organization_id,
        )

        if poll_jobs:
            job = self.jobs.poll_job(upload_job['id'], None)
            print('  Finished uploading files.')
            return job
        else:
            print('  Uploading files.')
            return upload_job

    @property
    def is_aws(self):
        if self._is_aws is None:
            url = f'{self._url}/debug/about'
            response = self.session.get(url)
            Util.raise_detailed_error(response)
            # Stack is not set in GCP, so we use that as a flag that we are running in AWS here.
            self._is_aws = 'stack' in response.json()
            os.environ['IS_AWS'] = str(self._is_aws)

        return self._is_aws
