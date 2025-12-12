from bs4 import BeautifulSoup

from .. import Moodle
from ..error import MoodleParseError, MoodleUpdateError


class Activity:
    def __init__(self, md: Moodle, id: int, page: BeautifulSoup = None, **kwargs: bool | str):
        self._md: Moodle = md
        self._id: int = id
        self._page: BeautifulSoup | None = page
        self._kwargs: dict[str, bool | str] = kwargs
        self._update: dict[str, bool | str] = {}

    @property
    def id(self) -> int:
        return self._id

    @property
    def session_key(self) -> str:
        return self._kwargs['sesskey']

    async def fetch(self, inplace: bool = False) -> 'Activity':
        # fetch edit page
        self._page = await self._md.session.get_html(f'/course/modedit.php?update={self._id}')

        # find form and extract parameters
        form = self._page.select_one('form[action="modedit.php"]')

        self._kwargs = {
            **{
                text_input.attrs['name']: text_input.attrs['value']
                for text_input in form.select('input[type="text"]')
            },
            **{
                checkbox_input.attrs['name']: 'checked' in checkbox_input.attrs
                for checkbox_input in form.select('input[type="checkbox"]')
            },
            **{
                textarea.attrs['name']: textarea.text
                for textarea in form.select('textarea')
            },
            **{
                select.attrs['name']: selected_option.attrs['value']
                for select, selected_option in [
                    (select, select.select_one('option[selected]'))
                    for select in form.select('select')
                ]
                if selected_option is not None
            },
            **{
                hidden_input.attrs['name']: hidden_input.attrs['value']
                for hidden_input in form.select('input[type="hidden"]')
            },
        }

        # find type and create specific activity object
        if inplace:
            return self

        nav_links = self._page.select('a.nav-link[role="menuitem"]')

        for nl in nav_links:
            if nl.attrs['href'].endswith(f'view.php?id={self._id}'):
                match nl.text.strip().lower():
                    case 'datei':
                        from .ResourceActivity import ResourceActivity
                        return ResourceActivity(self._md, self._id, self._page, **self._kwargs)
                    case 'externes tool':
                        from .LTIActivity import LTIActivity
                        return LTIActivity(self._md, self._id, self._page, **self._kwargs)

        # raise error if type is unknown
        raise MoodleParseError(f'could not determine activity type for id={self._id}')

    def __contains__(self, key) -> bool:
        return key in self._kwargs

    def __getitem__(self, key: str) -> bool | str:
        return self._kwargs[key]

    async def set(self, **kwargs: str | bool) -> 'Activity':
        # If activity has not been fetched, we need to do it now.
        if self._page is None:
            await self.fetch(inplace=True)

        # send all properties
        await self._md.session.post_html(f'/course/modedit.php', data={
            **{
                k: v if not isinstance(v, bool) else (1 if v else 0)
                for k, v in {
                    **self._kwargs,
                    **self._update,
                    **kwargs
                }.items()
            },
            'submitbutton': 'Speichern und anzeigen'
        })

        self._update = {}

        # fetch again and check the updated properties
        await self.fetch(inplace=True)

        for k, v in kwargs.items():
            if v != self._kwargs[k]:
                raise MoodleUpdateError(k, v, self._kwargs[k])

        return self

    def store(self, **kwargs: str | bool) -> 'Activity':
        for k, v in kwargs.items():
            self._update[k] = v

        return self

    async def _set(self, _autosave: bool, **kwargs: str | bool):
        if _autosave:
            return await self.set(**kwargs)
        else:
            return self.store(**kwargs)

    async def set_name(self, name: str, save: bool = False) -> 'Activity':
        return await self._set(save, name=name)

    async def set_description(self, description: str, description_format: int = 2, save: bool = False) -> 'Activity':
        return await self._set(save, **{
            'introeditor[text]': description,
            'introeditor[format]': str(description_format),
        })
