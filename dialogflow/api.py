import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
from helpers.secret_constants import PROJECT_ID, KEY_FILE

credentials = service_account.Credentials.from_service_account_file(KEY_FILE)


def detect_intent(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same session_id between requests allows continuation
    of the conversation.

    """
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.intent.display_name


def get_intent(client_session, client_response):
    """Returns the intent associated with the client_response

    :param client_response: [String]
    :param client_session: [Int]

    :return: [String]

    """
    return detect_intent(PROJECT_ID, client_session, [client_response], 'en')
