from time import sleep

import pandas as pd
import requests

from survey_studio_clients.core.base import SurveyStudioClient
from survey_studio_clients.requests.projects_request import PROJECTS_REQUEST as REQUEST


class SurveyStudioProjectsClient(SurveyStudioClient):
    ALL_PROJECTS_URL = "https://api.survey-studio.com/v1/projects?PageSize=100&PageNumber={page_number}"
    COUNTERS_URL = "https://api.survey-studio.com/v1/projects/{project_id}/counters"
    PROJECT_RESULTS_URL = "https://api.survey-studio.com/v1/projects/{project_id}/results/data"

    def get_project_id_by_name(self, project_name: str) -> int | None:
        all_projects = self._get_all_projects()

        for project in all_projects:
            if project["name"] == project_name:
                return project["id"]

        return None

    def _get_all_projects(self) -> list[dict]:
        url = self.ALL_PROJECTS_URL.format(page_number=1)
        response = requests.get(url=url, headers=self._get_headers()).json()
        page_count = response["pageCount"]
        all_projects = response["body"]

        if page_count > 1:
            for page_number in range(2, page_count + 1):
                url = self.ALL_PROJECTS_URL.format(page_number=page_number)
                sleep(12)  # Превышено максимальное количество обращений к методу "getprojects": 2 > 1 за 10 сек.
                response = requests.get(url=url, headers=self._get_headers()).json()
                all_projects += response["body"]

        return all_projects

    def get_counter_id_by_name(self, project_id: int, counter_name: str) -> str | None:
        all_counters = self._get_all_counters(project_id)

        for counter in all_counters:
            if counter["name"] == counter_name:
                return counter["id"]

        return None

    def _get_all_counters(self, project_id: int) -> list[dict | None]:
        url = self.COUNTERS_URL.format(project_id=project_id)
        response = requests.get(url=url, headers=self._get_headers()).json()

        if not response["isSuccess"]:
            return []

        return response["body"]

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
                    return self._make_dataframe_from_result_file(file_url, self._make_dataframe_from_excel)

    def _post_dataframe_request(self, params: dict) -> str:
        url = self.PROJECT_RESULTS_URL.format(project_id=params["project_id"])
        data = REQUEST.format(counter_id=params["counter_id"], date_from=params["date_from"], date_to=params["date_to"])
        response = requests.post(url=url, data=data, headers=self._get_headers()).json()

        if not response["isSuccess"]:
            return None

        return response["body"]
