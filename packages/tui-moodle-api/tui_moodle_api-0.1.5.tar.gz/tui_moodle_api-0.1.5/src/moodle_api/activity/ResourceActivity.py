from .Activity import Activity
from .ResourceList import ResourceList
from ..error import MoodleParseError


class ResourceActivity(Activity):
    async def resource_list(self) -> ResourceList:
        # session key and files id can be obtained from the form
        session_key = self.session_key
        files = self['files']

        # for the client id, we need to find the file manager div
        for div in self._page.select('div.filemanager'):
            if div.attrs['id'].startswith('filemanager-'):
                client_id = div.attrs['id'][len('filemanager-'):]
                break
        else:
            raise MoodleParseError(f'could not extract client id from file manager')

        # for the context id, we need to find an integrated object
        context_id = None
        for object in self._page.select('object[type="text/html"]'):
            for attr in object.attrs['data'].split('&'):
                if attr.startswith(('ctx_id', 'amp;ctx_id')):
                    _, context_id = attr.split('=', 1)
                    break

        if context_id is None:
            raise MoodleParseError(f'could not extract client id from file manager')

        # fetch tree
        return await ResourceList.fetch(self._md, session_key, files, client_id, context_id, '/')
