import requests_mock

from src.core.base import SurveyStudioClient

client = SurveyStudioClient("faketoken")


def test_get_headers():
    result = client._get_headers()
    expected_result = {"SS-Token": "faketoken", "Content-type": "application/json"}

    assert result == expected_result


def test_make_get_request_with_success():
    with requests_mock.Mocker() as m:
        m.get("http://mocked.url", text='{"somekey": "somevalue"}')
        result = client._make_get_request(url="http://mocked.url", headers={})
        expected_result = {"somekey": "somevalue"}

        assert result == expected_result


def test_make_get_request_with_403():
    pass

    # def _make_get_request(url: str, headers: dict) -> str | None:
    #
    #         response = requests.get(url=url, headers=headers)
    #         status_code = response.status_code
    #         response = response.json()
    #
    #     if status_code != 200:
    #         raise Exception(f"Results request ended with HTTP {status_code}.")
    #
    #     if not response["isSuccess"]:
    #         raise Exception(f"Request was unsuccessful: {response['errors']}")
    #
    #     if response["body"]["state"] == 3:
    #         return response["body"]["fileUrl"]
