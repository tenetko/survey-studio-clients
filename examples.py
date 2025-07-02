from datetime import datetime

from survey_studio_clients.api_clients.outgoing_calls import SurveyStudioOutgoingCallsClient
from survey_studio_clients.api_clients.projects import SurveyStudioProjectsClient
from survey_studio_clients.settings import API_TOKEN
from survey_studio_clients.web_scrapers.daily_counters import DailyCountersPageScraper

if __name__ == "__main__":

    # Outgoing Calls
    calls_client = SurveyStudioOutgoingCallsClient(API_TOKEN)
    dataframe = calls_client.get_dataframe("12345", "2025-03-31", "2025-04-01")

    print(len(dataframe))
    print(dataframe)

    # A single counter in a project

    projects_client = SurveyStudioProjectsClient(API_TOKEN)

    project_name = "Project Name"
    counter_name = "30 июня"

    project_id = projects_client.get_project_id_by_name(project_name)
    counter_id = projects_client.get_counter_id_by_name(project_id=project_id, counter_name=counter_name)

    params = {
        "project_id": project_id,
        "counter_id": counter_id,
        "date_from": "2025-06-30",
        "date_to": "2025-07-01",
    }

    dataframe = projects_client.get_dataframe(params)
    print(len(dataframe))
    print(dataframe)

    # A webpage parser


if __name__ == "__main__":
    parser = DailyCountersPageScraper("https://...")
    counter_name = parser.get_daily_counter_name(datetime(2025, 6, 30))
    value = parser.get_value_by_counter_name(counter_name)
    print(counter_name)
    print(value)
