import pandas as pd

from survey_studio_clients.api_clients.base import SurveyStudioClient
from survey_studio_clients.requests.outgoing_calls_request import OUTGOING_CALLS_REQUEST as REQUEST


class SurveyStudioOutgoingCallsClient(SurveyStudioClient):
    URL = "https://api.survey-studio.com/v1/calls/export"

    def get_dataframe(self, project_id: str, date_from: str, date_to: str, operator_talk: bool) -> pd.DataFrame:
        data = REQUEST.format(project_id=project_id, date_from=date_from, date_to=date_to, operator_talk=operator_talk)
        request_id = self._make_post_request(self.URL, data)
        file_url = self._get_result_file(request_id)
        print(f"----->{file_url}")

        return self._make_dataframe_from_result_file(file_url, self._make_dataframe_from_csv)
