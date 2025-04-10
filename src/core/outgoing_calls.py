from time import sleep

import pandas as pd

import requests
from src.core.base import SurveyStudioClient
from src.requests.outgoing_calls_request import OUTGOING_CALLS_REQUEST


class SurveyStudioOutgoingCallsClient(SurveyStudioClient):
    CALLS_URL = "https://api.survey-studio.com//v1/calls/export"

    def __init__(self, token: str) -> None:
        super().__init__(token)

    def get_outgoing_calls(self, project_id: str, date_from: str, date_to: str) -> pd.DataFrame:
        outgoing_calls_request_id = self._post_outgoing_calls_request(project_id, date_from, date_to)
        outgoing_calls_file_url = self._get_file_with_outgoing_calls(outgoing_calls_request_id)

        return self._make_dataframe(outgoing_calls_file_url)

    def _post_outgoing_calls_request(self, project_id: str, date_from: str, date_to: str) -> str | None:
        url = self.CALLS_URL.format(project_id=project_id)
        data = OUTGOING_CALLS_REQUEST.format(date_from=date_from, date_to=date_to, project_id=project_id)
        response = requests.post(url=url, headers=self._get_headers(), data=data).json()

        if not response["isSuccess"]:
            return None

        return response["body"]

    def _get_file_with_outgoing_calls(self, request_id: str) -> str:
        url = self.CALLS_URL + f"/{request_id}"

        is_first_request = True
        while True:
            if is_first_request:
                self._make_get_request(url, self._get_headers())
                is_first_request = False

            else:
                sleep(2)  # to prevent an error
                file_url = self._make_get_request(url, self._get_headers())
                if file_url:
                    return file_url
