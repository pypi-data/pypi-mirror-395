from typing import List, Any, Dict

from requests_toolbelt.sessions import BaseUrlSession

from pipebio.jobs import Jobs
from pipebio.organization_lists import OrganizationLists
from pipebio.util import Util


class Workflows:
    _session: BaseUrlSession
    _url: str
    _user: Any
    _organization_lists: OrganizationLists
    _jobs: Jobs

    def __init__(self, session: BaseUrlSession, organization_lists: OrganizationLists, user: Any, jobs: Jobs):
        self._url = 'jobs'
        self._session = Util.mount_standard_session(session)
        self._organization_lists = organization_lists
        self._user = user
        self._jobs = jobs

    def run_workflow(self,
                     project_id: str,
                     workflow_id: str,
                     name: str,
                     input_entity_ids: List[str],
                     organization_id: str = None,
                     target_folder_id: str = None,
                     params: Dict[str, Any] = None,
                     poll_job: bool = False
                     ) -> Dict[str, Any]:
        """

        :param project_id:
        :param workflow_id:
        :param name:
        :param input_entity_ids:
        :param organization_id:
        :param target_folder_id:
        :param params: Place any params needed by the workflow in this dictionary
        :param poll_job
        :return:
        """
        if params is None:
            params = dict()

        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        scaffolds = self._organization_lists.get_scaffolds()['data']

        response = self._organization_lists.get_workflow(workflow_id=workflow_id)
        workflow = response['options']['workflow']
        workflow_name = response['name']
        workflow_description = workflow['description'] if 'description' in workflow else ''

        param_names = list(params.keys())

        jobs = workflow['jobs']

        self._process_jobs(jobs, param_names, params, workflow_id, scaffolds)

        workflow_params = dict(name=name,
                               params=dict(jobs=jobs,
                                           name=workflow_name,
                                           description=workflow_description),
                               shareableId=project_id,
                               ownerId=_organization_id,
                               inputEntities=input_entity_ids,
                               type='WorkflowJob')
        if target_folder_id is not None:
            workflow_params['params']['targetFolderId'] = target_folder_id

        workflow_response = self._session.post('jobs', json=workflow_params)

        Util.raise_detailed_error(workflow_response)

        job = workflow_response.json()

        if poll_job:
            return self._jobs.poll_job(job['id'])
        else:
            return job

    def _process_jobs(self, jobs: List[Dict],
                      param_names: List[str],
                      params: Dict[str, Any],
                      workflow_id: str,
                      scaffolds: List[Dict]):
        """
        Iterates over all the jobs, replacing params if they are settable.
        If a settableParam has a required validator - it checks that either:
            - it is included in the params
            - has a default value already set in the workflow
        :param jobs:
        :param param_names:
        :param params:
        :param workflow_id:
        :param scaffolds:
        :return:
        """
        # iterate over each job
        for job in jobs:
            if 'jobs' in job:
                # Recursion!
                self._process_jobs(job['jobs'], param_names, params, workflow_id, scaffolds)
            else:
                if 'params' in job:
                    job_params = list(job['params'].items())
                    for key, value in job_params:
                        # iterate over each param for a job
                        if 'settableParams' in job:
                            settable_param = next(filter(lambda p: p['name'] == key, job['settableParams']), None)
                            # if its a settable param, use supplied value or validate
                            if settable_param is not None:
                                if key in param_names:
                                    # TODO validate options['allowedValues']?
                                    # set the job param to the supplied value
                                    job['params'][key] = params[key]
                                else:
                                    if 'validators' in settable_param:
                                        self._validate_required(workflow_id, key, value, settable_param)
                                del job['settableParams']

                        if key == 'scaffold':
                            scaffold = next(filter(lambda s: s['name'] == value, scaffolds), None)
                            if scaffold is not None:
                                job['params'][key] = dict(id=scaffold['id'], name=value)
                            else:
                                names = ', '.join(f'"{s["name"]}"' for s in scaffolds)
                                raise ValueError(
                                    f'No scaffold with the name specified in the workflow ({value}) was found. '
                                    f'Available scaffolds are: {names}'
                            )

    @staticmethod
    def _validate_required(workflow_id: str, key: str, value: Any, settable_param: Dict):
        is_required = next(
            filter(lambda p: p['name'] == 'required', settable_param['validators']),
            {'value': False}
        )['value']
        default_value_is_none = (value is None or value == 'None' or
                                 (isinstance(value, list) and len(value) == 0))
        if is_required and default_value_is_none:
            raise ValueError(f'Parameter {key} is required for workflow {workflow_id}')
