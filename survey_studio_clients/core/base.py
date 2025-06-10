import zipfile
from io import BytesIO

import pandas as pd
import requests


class SurveyStudioClient:
    HEADERS = {"SS-Token": "", "Content-type": "application/json"}

    def __init__(self, token: str) -> None:
        self.token = token

    def _get_headers(self):
        headers = self.HEADERS
        headers["SS-Token"] = self.token

        return headers

    @staticmethod
    def _make_get_request(url: str, headers: dict) -> str | None:
        response = requests.get(url=url, headers=headers)
        status_code = response.status_code
        response = response.json()

        if status_code != 200:
            raise Exception(f"Results request ended with HTTP {status_code}.")

        if not response["isSuccess"]:
            raise Exception(f"Request was unsuccessful: {response['errors']}")

        if response["body"]["state"] == 3:
            return response["body"]["fileUrl"]

    @staticmethod
    def _make_dataframe(url) -> pd.DataFrame:
        response = requests.get(url)
        with zipfile.ZipFile(BytesIO(response.content)) as zip:
            with zip.open(zip.namelist()[0]) as input_file:
                return pd.read_excel(input_file, engine="openpyxl")
