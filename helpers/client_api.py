from game_core.client import Client
from helpers.facebook_api import send_message
from helpers.bot_responses import GREETING_RESPONSE_4


def get_client(client_id, clients):
    """The function gets client from dictionary.

    Creates new client if it doesn't exist.

    :param clients: [dict(
    :param client_id: [Int]
    :return: [Client]

    """
    if client_id not in clients:
        clients[client_id] = Client(client_id)
    return clients[client_id]


def check_get_started(client, output, bot):
    try:
        if output['entry'][0]['messaging'][0]['postback']['payload'] == 'GET_STARTED_PAYLOAD':
            send_message(bot,
                         output['entry'][0]['messaging'][0]['sender']['id'],
                         GREETING_RESPONSE_4.format(client.first_name))
    except KeyError as e:
        print(e)


def process_current_client(output, bot, clients):
    """The function get current client and fill the public info if
    it has not been filled.

    :param output:
    :param bot:
    :param clients:
    :return:
    """
    try:
        info = bot.get_user_info(output['entry'][0]['messaging'][0]['sender']['id'])
        current_client = get_client(info['id'], clients)
        if not current_client.information_filled:
            current_client.fill_public_info(info['first_name'], info['last_name'], info['profile_pic'])
        return current_client
    except KeyError as e:
        print(e)