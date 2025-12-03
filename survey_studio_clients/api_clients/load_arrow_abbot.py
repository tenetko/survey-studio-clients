from time import sleep


import pandas as pd
import requests

from survey_studio_clients.api_clients.base import SurveyStudioClient
from survey_studio_clients.requests.projects_abbot_request import PROJECT_ABBOT_REQUEST as REQUEST


class SurveyStudioLoadArrowAbbotClient(SurveyStudioClient):
    URL = "https://api.survey-studio.com/v1/projects/{project_id}/results/data"

    def get_dataframe(self, project_id: str) -> pd.DataFrame:
        data = REQUEST.format(project_id=project_id)
        request_id = self._make_post_request(self.URL, data)
        file_url = self._get_result_file(request_id)
        print(f"----->{file_url}")

        return self._make_dataframe_from_result_file(file_url, self._make_dataframe_from_csv)