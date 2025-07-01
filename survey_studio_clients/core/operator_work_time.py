import pandas as pd

from survey_studio_clients.core.base import SurveyStudioClient
from survey_studio_clients.requests.operator_work_time_request import OPERATOR_WORK_TIME_REQUEST as REQUEST


class SurveyStudioOperatorWorkTimeClient(SurveyStudioClient):
    URL = "https://api.survey-studio.com/v1/reports/dex/operator-work-time"

    def get_dataframe(self, date_from: str, date_to: str) -> pd.DataFrame:
        data = REQUEST.format(date_from=date_from, date_to=date_to)
        request_id = self._make_post_request(self.URL, data)
        file_url = self._get_result_file(request_id)

        return self._make_dataframe_from_result_file(file_url, self._make_dataframe_from_excel)
