import dataclasses
import logging
from datetime import datetime, timedelta

import jira


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class JiraTimeLogClient:
    jira_server: str
    jira_username: str
    jira_api_token: str

    _jira_client: jira.JIRA = None

    JQL_DATE_FORMAT = "%Y-%m-%d"

    def __post_init__(self):
        try:
            self._jira_client = jira.JIRA(
                server=self.jira_server,
                basic_auth=(self.jira_username, self.jira_api_token),
                validate=True
            )
        except jira.JIRAError:
            logger.exception("Failed to create Jira client object")
            raise

    def _get_logged_stories_for_dates(
            self, start_date: datetime, end_date: datetime, jira_account_id: str = None
    ) -> jira.client.ResultList:

        if not jira_account_id:
            logger.debug("No Jira Account ID passed in, using ID of session owner (%s)", self._jira_client.myself())
            jira_account_id = self._jira_client.myself()["accountId"]

        query = f'worklogDate >= "{start_date.strftime(self.JQL_DATE_FORMAT)}" and ' \
                f'worklogDate < "{end_date.strftime(self.JQL_DATE_FORMAT)}" and ' \
                f'worklogAuthor in ("{jira_account_id}")'

        return self._jira_client.search_issues(query)

    def get_secs_logged_between(self, start_date: datetime, end_date: datetime, jira_account_id: str = None) -> int:
        total_time_logged = 0
        for story in self._get_logged_stories_for_dates(start_date, end_date, jira_account_id):
            for worklog in story.fields.worklog.worklogs:
                total_time_logged += worklog.timeSpentSeconds
        return total_time_logged

    def get_percentage_logged(self, start_date: datetime, end_date: datetime, expected_hours_logged: int):
        minutes_logged = self.get_secs_logged_between(start_date, end_date) / 60
        return ((expected_hours_logged * 60) / minutes_logged) * 100

    @staticmethod
    def get_beginning_of_this_week():
        today = datetime.today()
        return today - timedelta(days=today.weekday())

    @classmethod
    def get_weeks_ago(cls, weeks):
        week_ago_start = cls.get_beginning_of_this_week() - timedelta(weeks=weeks)
        week_ago_end = week_ago_start + timedelta(days=6)
        return week_ago_start, week_ago_end

    @classmethod
    def get_this_week(cls):
        return cls.get_weeks_ago(weeks=0)
