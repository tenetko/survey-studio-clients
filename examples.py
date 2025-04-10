from src.core.outgoing_calls import SurveyStudioOutgoingCallsClient
from src.settings import API_TOKEN

if __name__ == "__main__":

    # Outgoing Calls
    calls_client = SurveyStudioOutgoingCallsClient(API_TOKEN)
    dataframe = calls_client.get_outgoing_calls(48033, "2025-03-31", "2025-04-01")

    print(len(dataframe))
    print(dataframe)
