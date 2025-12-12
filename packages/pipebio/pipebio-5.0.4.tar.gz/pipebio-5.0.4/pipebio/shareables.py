import csv
from io import StringIO
from typing import List

from requests_toolbelt.sessions import BaseUrlSession

from pipebio.util import Util


class Shareables:

    def __init__(self, session: BaseUrlSession):
        self._url = 'shareables'
        self._session = session

    def list(self) -> List[dict]:
        response = self._session.get(self._url)

        print(f'ShareablesService:list - response:{response.status_code}')

        Util.raise_detailed_error(response)

        return response.json()['data']

    def create_project(self, name: str, owner_id: str) -> dict:
        response = self._session.post(self._url, json={
            'name': name,
            'type': 'PROJECT',
            'ownerId': owner_id,
        })

        print(f'ShareablesService:create - response:{response.status_code}')

        Util.raise_detailed_error(response)

        return response.json()

    def list_entities(self, shareable_id: str):
        url = f'{self._url}/{shareable_id}/entities'

        response = self._session.get(url)

        print(f'ShareablesService:list_entities - response:{response.status_code}')

        Util.raise_detailed_error(response)

        file = StringIO(response.text)
        reader = csv.DictReader(file, dialect='excel-tab')
        rows = []
        for row in reader:
            rows.append(row)
        return rows

    def get_project(self, project_name: str) -> dict:
        projects = self.list()

        # Find a specific project having a name "Example".
        project = next((project for project in projects if project['name'] == project_name), None)
        if project is None:
            raise Exception(f'Error: Project named "{project_name}" not found')

        return project