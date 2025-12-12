import json
import os.path
import re
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import List

import pandas as pd
import requests
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.attachments import Attachments
from pipebio.column import Column
from pipebio.models.entity_types import EntityTypes
from pipebio.models.field import Field
from pipebio.models.table_column_type import TableColumnType
from pipebio.models.upload_summary import UploadSummary
from pipebio.util import Util


class Entities:
    _url: str
    _session: BaseUrlSession
    attachments_service: Attachments

    def __init__(self, session: BaseUrlSession):
        self._url = 'entities'
        self._session = session
        self.attachments_service = Attachments(session)

    def create_file(self,
                    project_id: str,
                    name: str,
                    parent_id: str = None,
                    entity_type: EntityTypes = EntityTypes.SEQUENCE_DOCUMENT,
                    visible: bool = False) -> dict:
        print(f'create_file for parent_id:{str(parent_id)} name:{str(name)}')

        payload = {
            'name': name,
            'type': entity_type.value,
            'visible': visible,
            'shareableId': project_id,
        }

        if parent_id is not None:
            payload['parentId'] = str(parent_id)

        response = self._session.post(
            self._url,
            json=payload,
        )
        print(f'create_file response: {str(response.status_code)}')
        Util.raise_detailed_error(response)
        return response.json()

    def create_folder(self, project_id: str, name: str, parent_id: str = None, visible=False):
        return self.create_file(
            project_id=project_id,
            name=name,
            parent_id=parent_id,
            entity_type=EntityTypes.FOLDER,
            visible=visible
        )

    def mark_file_visible(self, entity_summary: UploadSummary):
        print('marking visible:', entity_summary)
        response = self._session.patch(
            f'{self._url}/{entity_summary.id}',
            json=entity_summary.to_json(),
        )
        print('mark_file_visible response:' + str(response.status_code))
        print('mark_file_visible text    :' + str(response.text))
        Util.raise_detailed_error(response)
        return response.json()

    def get(self, entity_id):
        response = self._session.get(f'{self._url}/{entity_id}')
        Util.raise_detailed_error(response)
        return response.json()

    def get_all(self, entity_ids):
        results = list(ThreadPool(8).imap_unordered(lambda entity_id: self.get(entity_id), entity_ids))
        for result in results:
            print(result)
        return results

    def delete(self, entity_ids: list):
        headers = {"Content-Type": "application/json"}
        data = {"ids": entity_ids}
        response = self._session.delete(f'{self._url}', json=data, headers=headers)
        Util.raise_detailed_error(response)

    @staticmethod
    def merge_fields(schema_a: List[Column], schema_b: List[Column]) -> List[Column]:
        result = []
        result.extend(schema_a)

        for column in schema_b:
            found = next((col for col in result if col.name == column.name), None)
            if found is None:
                result.append(column)

        return result

    def get_fields_for_all_entities(self, entity_ids: List[str]) -> List[Column]:
        schema = []
        for entity_id in entity_ids:
            new_schema = self.get_fields(entity_id)
            schema = Entities.merge_fields(schema, new_schema)
        return schema

    def get_fields(self, entity_id: str, ignore_id=False) -> List[Column]:
        """
        Returns the fields for a document or 404 if there are no fields (e.g. it's a folder).
        :return:
        """
        response = self._session.get(f'{self._url}/{entity_id}/fields')
        Util.raise_detailed_error(response)
        columns = []
        for field in response.json():

            if ignore_id and field == 'id':
                continue
            else:
                # Not all columns have field so we need to check it's set.
                description = field['description'] if 'description' in field else None
                columns.append(Column(field['name'], TableColumnType[field['type']], description))

        return columns

    def download_original_file(self, entity_id: str, destination_filename: str) -> str:
        """
        Download the originally uploaded file corresponding to a PipeBio document.
        Two requests are made:
        1. Request a signed url for this document (GET /api/v2/entities/:id/original)
        2. Download the data from that signed url (GET <result-from-step-1>)
        """
        # First request a signed url from PipeBio.
        signed_url_response = self._session.get(f'{self._url}/{entity_id}/original')

        # Did the signed-url request work ok?
        Util.raise_detailed_error(signed_url_response)

        # Parse the results to get the signed url.
        download_url = signed_url_response.json()['url']

        # Download the original file.
        download_response = requests.get(download_url)

        # Did the download request work ok?
        Util.raise_detailed_error(download_response)

        # Write the result to disk in chunks.
        with open(destination_filename, 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                f.write(chunk)

        return destination_filename

    @staticmethod
    def convert_pandas_type(pandas_type: str) -> TableColumnType:
        if pandas_type == 'int64':
            return TableColumnType.INT64
        elif pandas_type == 'float64':
            return TableColumnType.BIGNUMERIC
        else:
            return TableColumnType.STRING

    def get_file_handle(self, absolute_file_path):
        try:
            # Try as excel, fallback to csv/tsv.
            read_file = pd.read_excel(absolute_file_path)
            return read_file
        except Exception:
            # try as csv
            read_file = pd.read_table(absolute_file_path, sep=",")
            columns_length = len(read_file.columns.to_list())
            if columns_length > 1:
                return read_file
            else:
                read_file = pd.read_table(absolute_file_path, sep="\t")
                return read_file

    def merge(self,
              entity_id: str,
              assay_absolute_file_path: str,
              assay_column: str,
              entity_column: str,
              ):
        """
        Merge assay data from a tabular assay file (csv/tsv/excel) on your local disk into a PipeBio sequence document
        by matching values in the sequence document with rows from the tabular file.

        Equivalent to `add assay data <https://docs.pipebio.com/docs/assay-and-functional-data#add-assay-data>`
        :param entity_id: id of doc to merge into
        :param assay_absolute_file_path: location of tabular data on local disk
        :param assay_column: column having values matching those in entity_column
        :param entity_column: column having values matching those in assay_column
        :return:
        """
        if not os.path.isfile(assay_absolute_file_path):
            raise ValueError(f'File "{assay_absolute_file_path}" does not exist')

        path = Path(assay_absolute_file_path)
        stem = path.stem
        suffix = path.suffix[1:]
        # filtered_name = f'{stem}{suffix}'
        filtered_name = re.sub('[^a-zA-Z0-9]', '', f'{stem}{suffix}')
        # Mimicking the current front end functionality, if there are already columns with filtered name, append 2
        # to the end e.g. AdimabAssayxlsx becomes AdimabAssayxlsx2 and AdimabAssayxlsx2 becomes AdimabAssayxlsx22.
        columns = self.get_fields(entity_id)
        existing_assay_columns = list(filter(lambda c: c.name.startswith(filtered_name), columns))
        if len(existing_assay_columns) > 0:
            # Get the longest prefix
            prefixes = list(map(lambda c: c.name.split('_')[0], existing_assay_columns))
            longest_prefix = max(prefixes, key=len)
            filtered_name = f'{longest_prefix}2'

        # File needs to be uploaded as tsv, so use pandas here to transform it.
        tsv_file_name = f'{filtered_name}.tsv'
        tsv_absolute_file_path = f'/tmp/{tsv_file_name}'
        read_file = self.get_file_handle(assay_absolute_file_path)
        read_file.to_csv(path_or_buf=tsv_absolute_file_path,
                         index=False,
                         header=True,
                         sep='\t')

        fields_dict = read_file.dtypes.to_dict()
        fields = []
        for key in list(fields_dict.keys()):
            _type = Entities.convert_pandas_type(str(fields_dict[key]))
            safe_name = re.sub('[^a-zA-Z0-9]', '', key)
            if safe_name == 'id':
                safe_name = f'{filtered_name}_AssayImport_1'
                if len(safe_name) > 128:
                    safe_name = f'{safe_name[:125]}...'
                if entity_column == 'id':
                    assay_column = 'AssayImport_1'
            else:
                safe_name = f'{filtered_name}_{safe_name}'
            fields.append(Field(original=key, name=safe_name, type=_type))

        schema = json.dumps(list(map(lambda f: f.to_json(), fields)))
        multipart_form_data = dict(mappings=(None, '[]'),
                                   appendUnmatchedRows=(None, False),
                                   assayTableField=(None, f'{filtered_name}_{assay_column}'),
                                   targetTableField=(None, entity_column),
                                   targetFilter=(None, ''),
                                   schema=(None, schema),
                                   file=(tsv_file_name, open(tsv_absolute_file_path, 'rb')))

        response = self._session.post(f'{self._url}/{entity_id}/_merge', files=multipart_form_data)

        Util.raise_detailed_error(response)

        return response
