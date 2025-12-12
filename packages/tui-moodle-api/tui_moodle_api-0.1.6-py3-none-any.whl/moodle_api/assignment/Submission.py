from time import time
from typing import List

from . import Assignment
from .SubmissionFile import SubmissionFile
from .. import Moodle


class Submission:
    def __init__(self, md: Moodle, assignment: Assignment, user_id: int, files: List[SubmissionFile],
                 grade_attempt: int, session_key: str):
        self._md: Moodle = md
        self._assignment: Assignment = assignment
        self._user_id: int = user_id
        self._files: List[SubmissionFile] = files
        self._grade_attempt: int = grade_attempt
        self._session_key: str = session_key

    @property
    def assignment(self) -> Assignment:
        return self._assignment

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def files(self) -> List[SubmissionFile]:
        return self._files

    async def lock(self):
        await self._md.session.get_bytes('/mod/assign/view.php'
                                         f'?id={self.assignment.id}'
                                         f'&userid={self.user_id}'
                                         f'&sesskey={self._session_key}'
                                         f'&action=lock')

    async def grade(self, score: float, comment: str, send_notification: bool = True):
        await self._md.session.post_html('/mod/assign/view.php', {
            'id': self._assignment.id,
            'sesskey': self._session_key,
            'action': 'quickgrade',
            'lastpage': '',
            'content': 'Kommentar hinzufügen...',
            'savequickgrades': 'Bewertungsänderungen sichern',
            'sendstudentnotifications': 1 if send_notification else 0,
            '_qf__mod_assign_quick_grading_form': 1,
            f'grademodified_{self.user_id}': int(time()),
            f'gradeattempt_{self.user_id}': self._grade_attempt,
            f'quickgrade_{self.user_id}': score,
            f'quickgrade_comments_{self.user_id}': comment
        })
