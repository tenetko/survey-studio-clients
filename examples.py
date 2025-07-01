from src.core.outgoing_calls import SurveyStudioOutgoingCallsClient
from src.core.projects import SurveyStudioProjectsClient
from src.settings import API_TOKEN

if __name__ == "__main__":

    # Outgoing Calls
    calls_client = SurveyStudioOutgoingCallsClient(API_TOKEN)
    dataframe = calls_client.get_dataframe(12345, "2025-03-31", "2025-04-01")

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
