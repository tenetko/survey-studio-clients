import io
import zipfile
from io import BytesIO
from time import sleep

import pandas as pd
import requests

REQUEST = ""


class SurveyStudioClient:
    HEADERS = {"SS-Token": "", "Content-type": "application/json"}
    URL = ""

    def __init__(self, token: str) -> None:
        self.token = token

    def _make_post_request(self, url: str, data: str):
        response = requests.post(url=url, headers=self._get_headers(), data=data)
        status_code = response.status_code

        if status_code != 200:
            raise Exception(f"Results request ended with HTTP {status_code}.")

        try:
            response = response.json()

        except requests.exceptions.JSONDecodeError as e:
            print(e)
            print(response.text[:100])

        if not response["isSuccess"]:
            return None

        return response["body"]

    def _get_headers(self):
        headers = self.HEADERS
        headers["SS-Token"] = self.token

        return headers

    def _get_result_file(self, request_id: str) -> str:
        url = self.URL + f"/{request_id}"

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

    @staticmethod
    def _make_get_request(url: str, headers: dict) -> str | None:
        response = requests.get(url=url, headers=headers)
        status_code = response.status_code
        try:
            response = response.json()

        except requests.exceptions.JSONDecodeError as e:
            print(e)
            print(response.text[:100])

        if status_code != 200:
            raise Exception(f"Results request ended with HTTP {status_code}.")

        if not response["isSuccess"]:
            raise Exception(f"Request was unsuccessful: {response['errors']}")

        if response["body"]["state"] == 3:
            return response["body"]["fileUrl"]

        return None

    @staticmethod
    def _make_dataframe_from_result_file(url: str, maker_function) -> pd.DataFrame:
        response = requests.get(url)

        if response.headers["Content-type"] == "application/zip":
            with zipfile.ZipFile(BytesIO(response.content)) as zip:
                with zip.open(zip.namelist()[0]) as input_file:
                    res = maker_function(input_file)

        else:
            res = maker_function(BytesIO(response.content))

        return res

    @staticmethod
    def _make_dataframe_from_excel(input_file: io.BytesIO) -> pd.DataFrame:
        return pd.read_excel(input_file, engine="openpyxl")

    @staticmethod
    def _make_dataframe_from_csv(input_file: io.BytesIO) -> pd.DataFrame:
        return pd.read_csv(input_file, sep=";", encoding="utf-8", low_memory=False)
