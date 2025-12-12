from typing import Union, List

from requests_toolbelt.sessions import BaseUrlSession

from pipebio.models.attachment_type import AttachmentType
from pipebio.util import Util


class Attachments:
    _url: str
    _session: BaseUrlSession

    def __init__(self, session: BaseUrlSession):
        self._url = 'entities'
        self._session = session

    def create(self, entity_id: str, attachment_type: AttachmentType, data: Union[dict, List]):
        print(f'Creating attachment: entity_id={entity_id},kind={attachment_type.value}')
        url = f'{self._url}/{entity_id}/attachments'
        json = {
            "data": data,
            "type": attachment_type.value,
        }
        response = self._session.post(url, json=json)
        Util.raise_detailed_error(response)
        print('Created attachment: response', response.status_code)
        return response.json()

    def upsert_single(self, entity_id: str, attachment_type: AttachmentType, data: Union[dict, List], version: int = 1,
                      ignore_version=True):
        """
        Create or update if exists.
        """
        print(f'Upserting attachment: entity_id={entity_id},type={attachment_type.value},version={version},ignore_version={ignore_version}')
        url = f'{self._url}/{entity_id}/attachments'
        json = {
            "data": data,
            "version": version,
            "type": attachment_type.value,
            "ignoreVersion": ignore_version,
        }
        response = self._session.put(url, json=json)
        Util.raise_detailed_error(response)
        print('Upserted attachment: response', response.status_code)

    def upsert_multi(self, attachment_id: str, data: Union[dict, List], version: int):
        """
        Create or update if exists.
        """
        print(f'Upserting multi attachment: attachment_id={attachment_id}')
        url = f'attachments/{attachment_id}'
        json = {
            "attachment": {
                "data": data,
                "version": version,
                "id": attachment_id,
            }
        }
        response = self._session.put(url, json=json)
        Util.raise_detailed_error(response)
        print('Upserted attachment: response', response.status_code)

    def get(self, entity_id: str, attachment_type: AttachmentType):
        url = f'{self._url}/{entity_id}/attachments/{attachment_type.value}'
        response = self._session.get(url)
        Util.raise_detailed_error(response)
        return response.json()
