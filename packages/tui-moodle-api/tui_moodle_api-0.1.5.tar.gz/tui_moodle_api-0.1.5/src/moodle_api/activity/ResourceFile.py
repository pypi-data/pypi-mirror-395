from json import dumps as json_encode

from .. import Moodle
from ..error import MoodleParseError


class ResourceFile:
    def __init__(self, md: Moodle,
                 session_key: str, item_id: str, client_id: str,
                 file_path: str, file_name: str, full_name: str, size: int, mime_type: str,
                 author: str, license: str, created: int, modified: int, is_ref: bool,
                 url: str):
        self._md: Moodle = md

        self._session_key: str = session_key
        self._item_id: str = item_id
        self._client_id: str = client_id
        self._file_path: str = file_path

        self.file_name: str = file_name
        self.full_name: str = full_name
        self.size: int = size
        self.mime_type: str = mime_type
        self.author: str = author
        self.license: str = license
        self.created: int = created
        self.modified: int = modified
        self.is_ref: bool = is_ref
        self.url: str = url

    async def delete(self):
        json = await self._md.session.post_json(
            '/repository/draftfiles_ajax.php?action=deleteselected',
            {
                'sesskey': self._session_key,
                'client_id': self._client_id,
                'filepath': self._file_path,
                'itemid': self._item_id,
                'selected': json_encode([{
                    'filepath': self._file_path,
                    'filename': self.file_name
                }])
            }
        )

        if 'error' in json:
            raise MoodleParseError(json['error'])
