import asyncio
from json import dumps as json_encode
from typing import IO

from .ResourceFile import ResourceFile
from .. import Moodle
from ..error import MoodleParseError


class ResourceList:
    def __init__(self, md: Moodle,
                 session_key: str, item_id: str, client_id: str, context_id: str,
                 file_path: str, full_name: str,
                 files: list[ResourceFile], children: list['ResourceList']):
        self._md: Moodle = md

        self._session_key: str = session_key
        self._item_id: str = item_id
        self._client_id: str = client_id
        self._context_id: str = context_id

        self.file_path: str = file_path
        self.full_name: str = full_name
        self.files: list[ResourceFile] = files
        self.children: list['ResourceList'] = children

    @staticmethod
    async def fetch(md: Moodle,
                    session_key: str, item_id: str, client_id: str, context_id: str, file_path: str) -> 'ResourceList':
        json = await md.session.post_json(
            f'/repository/draftfiles_ajax.php?action=list',
            {
                'sesskey': session_key,
                'itemid': item_id,
                'client_id': client_id,
                'filepath': file_path
            }
        )

        return ResourceList(
            md,
            session_key, item_id, client_id, context_id,
            json['path'][-1]['path'], json['path'][-1]['name'],
            [
                ResourceFile(
                    md,
                    session_key, item_id, client_id,
                    file_path, file['filename'], file['fullname'], file['size'], file['mimetype'],
                    file['author'], file['license'], file['datecreated'], file['datemodified'], file['isref'],
                    file['url']
                )
                for file in json['list']
                if file['type'] == 'file'
            ],
            await asyncio.gather(*(
                ResourceList.fetch(
                    md, session_key, item_id, client_id, context_id, file['filepath']
                )
                for file in json['list']
                if file['type'] == 'folder'
            ))
        )

    async def delete(self):
        json = await self._md.session.post_json(
            '/repository/draftfiles_ajax.php?action=deleteselected',
            {
                'sesskey': self._session_key,
                'client_id': self._client_id,
                'filepath': self.file_path,
                'itemid': self._item_id,
                'selected': json_encode([{
                    'filepath': self.file_path,
                    'filename': '.'
                }])
            }
        )

        if 'error' in json:
            raise MoodleParseError(json['error'])

    async def upload(self, file: IO, name: str, author: str, overwrite: bool = True) -> bool:
        json = await self._md.session.post_json(
            '/repository/repository_ajax.php?action=upload',
            {
                'sesskey': self._session_key,
                'repo_id': str(5),  # always 5?
                'itemid': self._item_id,
                'author': author,
                'savepath': self.file_path,
                'title': name,
                'overwrite': str(1 if overwrite else 0),
                'ctx_id': self._context_id,
                'repo_upload_file': file
            },
            no_check_mimetype=True
        )

        if 'error' in json:
            raise MoodleParseError(json['error'])

        return 'event' not in json or json['event'] != 'fileexists'
