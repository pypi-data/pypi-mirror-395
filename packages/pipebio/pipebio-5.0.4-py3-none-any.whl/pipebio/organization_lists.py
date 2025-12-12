from typing import Any

from requests_toolbelt.sessions import BaseUrlSession

from pipebio.util import Util


class OrganizationLists:
    _session: BaseUrlSession
    _url: str
    _user: Any

    def __init__(self, session: BaseUrlSession, user: Any):
        self._session = Util.mount_standard_session(session)
        self._url = 'organizations'
        self._user = user

    def get_workflow(self, workflow_id: str, organization_id: str = None) -> Any:
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        url = f'{self._url}/{_organization_id}/lists/{workflow_id}'
        response = self._session.get(url)

        Util.raise_detailed_error(response)

        workflow_json = response.json()

        if workflow_json is None:
            raise ValueError('Workflow not found')
        if workflow_json['kind'] != 'WORKFLOW':
            raise ValueError(f'A list was found for the given id "{workflow_id}" but it is not of type "WORKFLOW"')

        return workflow_json

    def get_scaffolds(self, organization_id: str = None) -> Any:
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        url = f'{self._url}/{_organization_id}/lists?kind=scaffold'
        response = self._session.get(url)

        Util.raise_detailed_error(response)

        return response.json()
