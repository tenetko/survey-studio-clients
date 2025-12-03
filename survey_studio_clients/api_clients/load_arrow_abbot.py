from time import sleep

import requests

from survey_studio_clients.api_clients.projects import SurveyStudioProjectsClient
from survey_studio_clients.requests.projects_abbot_request import PROJECT_ABBOT_REQUEST as REQUEST


class SurveyStudioLoadArrowAbbotClient(SurveyStudioProjectsClient):

    def get_dataframe(self, params: dict) -> pd.DataFrame | None:
        request_id = self._post_dataframe_request(params)
        url = self.PROJECT_RESULTS_URL.format(project_id=params["project_id"])
        url = url + f"/{request_id}"

        is_first_request = True
        while True:
            if is_first_request:
                self._make_get_request(url, self._get_headers())
                is_first_request = False

            else:
                sleep(2)  # to prevent an error from the API
                file_url = self._make_get_request(url, self._get_headers())
                if file_url:
                    print(f"----->{file_url}")
                    return self._make_dataframe_from_result_file(file_url, self._make_dataframe_from_csv)

    def _post_dataframe_request(self, params: dict) -> str | None:
        url = self.PROJECT_RESULTS_URL.format(project_id=params["project_id"])
        data = REQUEST.format(counter_id=params["counter_id"])
        print(data)
        response = requests.post(url=url, data=data, headers=self._get_headers()).json()

        if not response["isSuccess"]:
            return None

        return response["body"]
