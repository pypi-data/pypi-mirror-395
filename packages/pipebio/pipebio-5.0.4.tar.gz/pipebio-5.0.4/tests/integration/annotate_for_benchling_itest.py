import uuid
import os
from pipebio.pipebio_client import PipebioClient
from pipebio.models.job_type import JobType
from annotate.AnnotateForBenchlingParams import (
    AnnotateForBenchlingParams,
    GermlineBasedDomain,
    LinkerDomain,
    ConstantDomain,
    ShortScaffold,
)
from annotate.selection_range import SelectionRange
from annotate.service_token_service import set_sts_token

class TestAnnotateForBenchlingIntegration:

    def setup_method(self):
        self.api_url = os.environ.get("PIPE_API_URL")
        print('PIPE_API_URL', self.api_url)

    def test_full_sdk_run(self):

        print('Starting')

        set_sts_token(
            benchling_user_id='my_benchling_user_id',
            url=self.api_url,
            tenant_id="ten_brgw1g3r2c",
            tenant_subdomain="https://pipebio-dtt.benchling.com"
        )
        client = PipebioClient(url=self.api_url)

        shareable_id = client.user['shareableId']
        organization_id = client.user['org']['id']

        job_run = f'test-{uuid.uuid4()}'

        folder = client.entities.create_folder(
            project_id=shareable_id,
            name=job_run,
            parent_id=None,
            visible=True
        )

        folder_id = folder['id']

        print('Uploading query/reference sequences in parallel.')
        test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_data')
        uploads = [
            client.upload_file(
                file_name='aa_database.fasta',
                absolute_file_location=os.path.join(test_data_dir, 'aa_database.fasta'),
                parent_id=folder_id,
                project_id=shareable_id
            ),
            client.upload_file(
                file_name='test_sequences_aa.fasta',
                absolute_file_location=os.path.join(test_data_dir, 'test_sequences_aa.fasta'),
                parent_id=folder_id,
                project_id=shareable_id
            )
        ]

        # Wait for uploads to complete.
        job_ids = list(job['id'] for job in uploads)
        # TODO Confirm if these are in order.
        upload_jobs = client.jobs.poll_jobs(job_ids)
        reference_db_doc_id = upload_jobs[0]['outputEntities'][0]['id']
        query_db_doc_id = upload_jobs[1]['outputEntities'][0]['id']

        params = AnnotateForBenchlingParams(
            target_folder_id=folder_id,
            scaffolds=[
                ShortScaffold(
                    selection=SelectionRange(start_id=1, end_id=2),
                    domains=[
                        GermlineBasedDomain(name='vh', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e'])
                    ]
                ),
                ShortScaffold(
                    selection=SelectionRange(start_id=3, end_id=4),
                    domains=[
                        GermlineBasedDomain(name='vh', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e']),
                        LinkerDomain(name='l', reference_sequences=[reference_db_doc_id]),
                        GermlineBasedDomain(name='vl', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e'])
                    ]
                ),
                ShortScaffold(
                    selection=SelectionRange(start_id=5, end_id=6),
                    domains=[
                        GermlineBasedDomain(name='vl', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e']),
                        LinkerDomain(name='l1', reference_sequences=[reference_db_doc_id]),
                        GermlineBasedDomain(name='vh', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e']),
                        LinkerDomain(name='l2', reference_sequences=[reference_db_doc_id]),
                        GermlineBasedDomain(name='vh', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e']),
                        ConstantDomain(name='ch1', reference_sequences=[reference_db_doc_id]),
                        ConstantDomain(name='hinge', reference_sequences=[reference_db_doc_id]),
                        ConstantDomain(name='ch2', reference_sequences=[reference_db_doc_id]),
                        ConstantDomain(name='ch3', reference_sequences=[reference_db_doc_id]),
                        LinkerDomain(name='l3', reference_sequences=[reference_db_doc_id]),
                        GermlineBasedDomain(name='vh', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e'])
                    ]
                ),
                ShortScaffold(
                    selection=SelectionRange(start_id=7, end_id=8),
                    domains=[
                        GermlineBasedDomain(name='vl', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e']),
                        LinkerDomain(name='l1', reference_sequences=[reference_db_doc_id]),
                        GermlineBasedDomain(name='vh', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e']),
                        LinkerDomain(name='l2', reference_sequences=[reference_db_doc_id]),
                        GermlineBasedDomain(name='vh', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e']),
                        ConstantDomain(name='ch1', reference_sequences=[reference_db_doc_id]),
                        ConstantDomain(name='hinge', reference_sequences=[reference_db_doc_id]),
                        ConstantDomain(name='ch2', reference_sequences=[reference_db_doc_id]),
                        ConstantDomain(name='ch3', reference_sequences=[reference_db_doc_id]),
                        LinkerDomain(name='l3', reference_sequences=[reference_db_doc_id]),
                        GermlineBasedDomain(name='vh', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e']),
                        LinkerDomain(name='l4', reference_sequences=[reference_db_doc_id]),
                        GermlineBasedDomain(name='vl', germline_ids=['845a6eb1-9dda-4f98-b1b1-eb6788d0296e'])
                    ]
                ),
            ]
        )

        annotation_job_id = client.jobs.create(
            shareable_id=shareable_id,
            job_type=JobType.AnnotateForBenchlingJob,
            name=job_run,
            input_entity_ids=[reference_db_doc_id, query_db_doc_id],
            params=params.to_json(),
            owner_id=organization_id,
        )
        # Set a timeout to allow sufficient time for the job to finish.
        client.jobs.poll_job(job_id=annotation_job_id, timeout_seconds=60*10)
        annotation_job = client.jobs.get(annotation_job_id)

        if not annotation_job.get('outputEntities'):
            raise Exception(f"Job failed or produced no output. Status: {annotation_job.get('status')}")

        result_id = annotation_job['outputEntities'][0]['id']

        # Download the results (e.g. for post-processing in Benchling).
        absolute_location = os.path.join(os.getcwd(), f'Benchling annotation - {job_run}.tsv')
        client.sequences.download(result_id, destination=absolute_location)
        print(f'Downloaded results to: {absolute_location}')


