import concurrent.futures
import time
from typing import List, Any

import requests
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.models.entity_types import EntityTypes
from pipebio.models.job_status import JobStatus
from pipebio.models.job_type import JobType
from pipebio.models.output_link import OutputLink
from pipebio.models.upload_detail import UploadDetail
from pipebio.util import Util


class Jobs:
    _session: BaseUrlSession
    _url: str
    _job_id: str
    _user: Any

    def __init__(self, session: BaseUrlSession, user: Any, job_id: str = None):
        self._url = 'jobs'
        self._session = Util.mount_standard_session(session)
        self._job_id = job_id
        self._user = user

    def create(self,
               shareable_id: str,
               job_type: JobType,
               name: str,
               input_entity_ids: List[str],
               owner_id: str = None,
               params=None,
               poll_jobs: bool = False,
               client_side: bool = False) -> str:
        """
        :param shareable_id: - project in which the documents are
        :param job_type:
        :param name: - helpful user facing name
        :param input_entity_ids: - document ids
        :param owner_id: - organization id owning this job
        :param params: - specific to this job_type
        :param poll_jobs:
        :param client_side - set true if you want to run the job locally yourself and not on PipeBio servers
        :return:
        """

        if params is None:
            params = {}

        # Use owner_id if supplied, otherwise use default org id.
        _organization_id = owner_id if owner_id is not None else Util.get_organization_id(self._user)

        response = self._session.post(self._url,
                                      json={
                                          'name': name,
                                          'params': params,
                                          'shareableId': shareable_id,
                                          'ownerId': _organization_id,
                                          'inputEntities': input_entity_ids,
                                          'type': job_type.value,
                                          'clientSide': client_side,
                                      })

        Util.raise_detailed_error(response)

        data = response.json()
        job_id = data['id']
        self._job_id = job_id

        if poll_jobs:
            self.poll_jobs([job_id], None)

        return job_id

    def list(self, organization_id: str = None):
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        response = self._session.get(self._url,
                                     params={'organizationId': _organization_id})
        Util.raise_detailed_error(response)
        return response.json()

    def get(self, job_id: str = None):
        if job_id is None:
            job_id = self._job_id
        url = f'{self._url}/{job_id}'
        response = self._session.get(url)
        Util.raise_detailed_error(response)
        return response.json()

    def start_import_job(self):
        """
        Enable the cloud-function to trigger a job run via the kubernetes job processing engine.
        :return:
        """
        response = self._session.patch(f'{self._url}/{self._job_id}/import')
        Util.raise_detailed_error(response)
        return response

    def poll_job(self, job_id: str = None, timeout_seconds=None):
        """
        Poll job until it completes/fails.
        :param job_id:
        :param timeout_seconds:
        :return:
        """
        if job_id is None:
            job_id = self._job_id

        done = False
        job_status = None
        job = None

        print(f'Polling job: {job_id}')

        # 5 mins
        timeout = time.time() + (timeout_seconds if timeout_seconds is not None else 60 * 5)

        while not done:
            time.sleep(5)
            job = self.get(job_id)
            job_status = job['status']
            print(f'     Job {job_id} status: {job_status}')
            done = job_status in [JobStatus.COMPLETE.value, JobStatus.FAILED.value]

            if time.time() > timeout:
                raise Exception(f'Timeout waiting for job {job_id} to finish.')

        print(f'Job {job_id} is: {job_status}')
        return job

    def poll_jobs(self, job_ids: List[str], timeout_seconds=None):
        """
        Poll jobs until they are complete or failed.
        :param job_ids:
        :param timeout_seconds:
        :return:
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        results = [executor.submit(self.poll_job, job_id, timeout_seconds) for job_id in iter(job_ids)]
        executor.shutdown(wait=True)
        return list(map(lambda result: result.result(), results))

    def create_signed_upload(self,
                             file_name: str,
                             parent_id: str,
                             project_id: str,
                             details: List[UploadDetail],
                             file_name_id: str,
                             organization_id: str = None) -> dict:
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        data = dict(
            name=file_name,
            type=EntityTypes.SEQUENCE_DOCUMENT.value,
            targetFolderId=parent_id,
            shareableId=project_id,
            ownerId=_organization_id,
            details=[],
        )

        if details is not None:
            # Details should be an
            for detail in details:
                data['details'].append(detail.to_json())

        if file_name_id is not None:
            data['details'].append({
                'name': 'fileNameId',
                'type': 'fileNameId',
                'value': file_name_id
            })

        response = self._session.post('signed-url', json=data)

        Util.raise_detailed_error(response)

        return response.json()

    def upload_data_to_signed_url(self,
                                  absolute_file_location: str,
                                  signed_url: str,
                                  signed_headers):

        # TODO We do not yet support large uploads.
        if Util.is_aws():
            with open(absolute_file_location, 'rb') as file:
                upload_response = requests.put(signed_url, data=file, headers=signed_headers)
            Util.raise_detailed_error(upload_response)
            print('Upload response: ', upload_response.status_code)
            print('Upload response:', upload_response.text)
        else:
            # 1. Start the signed-upload.
            # NOTE: Url and headers cannot be modified or the upload will fail.
            create_upload_response = self._session.post(signed_url, headers=signed_headers)
            Util.raise_detailed_error(create_upload_response)
            response_headers = create_upload_response.headers
            location = response_headers['Location']

            # 2. Upload bytes.
            with open(absolute_file_location, 'rb') as file:
                upload_response = self._session.put(location, data=file)
                Util.raise_detailed_error(upload_response)
                print('Upload response: ', upload_response.status_code)
                print('Upload response:', upload_response.text)

    def update(self,
               status: JobStatus,
               progress=None,
               messages: List[str] = None,
               output_entity_ids: List[str] = None,
               output_links: List[OutputLink] = None):
        """
        Update a jobs status.
        :param status:
        :param progress:
        :param messages:
        :param output_entity_ids:
        :param output_links:
        :return:
        """

        body = {
            'status': status.value,
        }

        if progress is not None:
            # Clamp the progress between 0 and 100.
            body['progress'] = max(0, min(100, progress))

        if messages is not None:
            body['messages'] = messages

        if output_entity_ids is not None:
            body['outputEntities'] = output_entity_ids

        if output_links is not None:
            body['outputLinks'] = list(map(lambda link: link.to_json(), output_links))

        response = self._session.patch(f'{self._url}/{self._job_id}',
                                       json=body)
        Util.raise_detailed_error(response)
        return response

    def set_complete(self,
                     messages: List[str] = None,
                     output_entity_ids: List[str] = None,
                     output_links: List[OutputLink] = None):
        """
        Complete a job.
        :param messages:
        :param output_entity_ids:
        :param output_links:
        :return:
        """
        return self.update(JobStatus.COMPLETE,
                           100,
                           messages=messages,
                           output_entity_ids=output_entity_ids,
                           output_links=output_links)
