import dialogflow_v2 as dialogflow
import re
from google.oauth2 import service_account
from helpers.secret_constants import PROJECT_ID, KEY_FILE

credentials = service_account.Credentials.from_service_account_file(KEY_FILE)


def detect_query(session_id, text, project_id=PROJECT_ID, language_code='en'):
    """Returns the result of detect intent with texts as inputs.

    Using the same session_id between reques    ts allows continuation
    of the conversation.

    """
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    return response.query_result


def get_intent(query):
    """Returns the intent associated with the client_response

    :param query:

    :return: [String]

    """
    try:
        return query.intent
    except Exception as e:
        print(e)
        return None


def get_intent_name(query):
    """Returns the intent name associated with the client_response

    :param query:

    :return: [String]

    """
    try:
        return get_intent(query).display_name
    except Exception as e:
        print(e)
        return None


def get_fulfillment_message(query):
    try:
        return parse_message(query.fulfillment_messages[0].text)
    except Exception as e:
        print(e)
        return None


def parse_message(full_message):
    return re.findall("^text: \"(.+)\"", str(full_message))[0]
