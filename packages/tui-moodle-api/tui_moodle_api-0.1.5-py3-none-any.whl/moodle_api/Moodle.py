import re

from .activity import Activity
from .error import MoodleLoginError
from .assignment import Assignment
from .util import LimitedSession


class Moodle:
    def __init__(self, host: str, wait_time: float = 1.0):
        self.session: LimitedSession = LimitedSession(host, wait_time)

    # context manager
    async def __aenter__(self):
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.__aexit__(exc_type, exc_val, exc_tb)

    # login
    async def logged_in(self) -> bool:
        page = await self.session.get_html('/login/index.php')
        text = page.find(id='modal-body')

        if text is not None:
            if re.match(r'^Sie sind bereits als (.*?) angemeldet. '
                        r'Sie müssen sich abmelden, bevor Sie sich mit anderen Daten wieder anmelden.$',
                        text.text):
                return True

        return False

    async def login(self, username: str, password: str):
        # receive login token
        page = await self.session.get_html('/login/index.php')

        input = page.select_one('input[name="logintoken"]')
        login_token = input['value']

        # send login request
        page = await self.session.post_html('/login/index.php', {
            'logintoken': login_token,
            'username': username,
            'password': password
        })

        error_message = page.find(id='loginerrormessage')
        if error_message is not None:
            raise MoodleLoginError(error_message.text)

    async def shibboleth_login(self, username: str, password: str, provider_id: str):
        # receive idp login page
        page = await self.session.post_html('/Shibboleth.sso/Login', {
            'target': f'{self.session.host}/auth/shibboleth/index.php',
            'providerId': f'{provider_id}/idp/shibboleth'
        })

        # send login
        form = page.select_one('form[method="post"]')
        action = form['action']

        input = form.select_one('input[name="csrf_token"]')
        csrf_token = input['value']

        page = await self.session.post_html(f'{provider_id}{action}', {
            'csrf_token': csrf_token,
            'j_username': username,
            'j_password': password,
            '_eventId_proceed': ''
        })

        error_message = page.select_one('p.output--error')
        if error_message is not None:
            raise MoodleLoginError(error_message.text)

        # handle redirect form
        form = page.select_one('form[method="post"]')
        action = form['action']

        input = form.select_one('input[name="RelayState"]')
        relay_state = input['value']

        input = form.select_one('input[name="SAMLResponse"]')
        saml_response = input['value']

        await self.session.post_html(action, {
            'RelayState': relay_state,
            'SAMLResponse': saml_response
        })

    async def is_logged_in(self) -> bool:
        page, redirects = await self.session.get_html_redirects('/my')

        if not redirects[-1][1].path.endswith(('/my', '/my/')):
            return False

        if 'Sie sind als Gast angemeldet' in page.text:
            return False

        return True

    # assignments
    def assigment(self, id: int) -> Assignment:
        return Assignment(self, id)

    # TODO course, chapters?

    # activity
    def activity(self, id: int) -> Activity:
        return Activity(self, id)
