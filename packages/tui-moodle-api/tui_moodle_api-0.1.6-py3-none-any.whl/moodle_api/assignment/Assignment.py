from .. import Moodle
from .Submission import Submission
from .SubmissionFile import SubmissionFile


class Assignment:
    def __init__(self, md: Moodle, id: int):
        self._md: Moodle = md
        self._id: int = id

    @property
    def id(self) -> int:
        return self._id

    async def submissions(self) -> list[Submission]:
        # We have to set the filter to `requiregrading` to only receive
        # new submissions that have not been graded yet.
        users_per_page = 20

        # request page and extract required form parameters
        page = await self._md.session.get_html(f'/mod/assign/view.php?id={self._id}&action=grading')
        form = page.find('form', attrs={'class': 'gradingoptionsform'})

        data = {
            'action': 'saveoptions',
            'filter': 'requiregrading',
            'perpage': users_per_page
        }
        for key in 'id', 'userid', 'contextid', 'sesskey', \
                'showonlyactiveenrol', 'downloadasfolders', \
                '_qf__mod_assign_grading_options_form', 'mform_isexpanded_id_general':
            data[key] = form.find('input', attrs={'name': key})['value']

        assert data['id'] == str(self._id)

        # send post request and extract table
        page = await self._md.session.post_html('/mod/assign/view.php', data)
        table = page.find('div', attrs={'class': 'gradingtable'}).find('table')

        if table is None:
            return []

        # find users
        assert len(table.select('tbody tr')) == users_per_page

        submissions: list[Submission] = []
        for row in table.select('tbody tr:not(.emptyrow)'):
            # extract user id
            for class_name in row['class']:
                if class_name.startswith('user'):
                    user_id = int(class_name[4:])
                    break
            else:
                # TODO raise MoodleParseError
                raise AssertionError

            # extract grade attempt
            grade_attempt = row.find('input', attrs={'name': f'gradeattempt_{user_id}'})['value']

            # extract attached files
            files: list[SubmissionFile] = []
            for submission in row.find_all('div', attrs={'class': 'fileuploadsubmission'}):
                anchor = submission.find('a')
                assert anchor['href'].endswith('?forcedownload=1')

                files.append(SubmissionFile(self._md, anchor.text.strip(), anchor['href']))

            # add submission to result list
            submissions.append(Submission(self._md, self, user_id, files, grade_attempt, data['sesskey']))

        return submissions
