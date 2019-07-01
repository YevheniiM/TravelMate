from game_core.client import Client
from helpers.facebook_api import send_message


def get_client(client_id, clients):
    """The function gets client from dictionary.

    Creates new client if it doesn't exist.

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
                         "Hey, {}! I am TravelMate, your adventure buddy wherever you go. "
                         "I’m gonna help you explore new destinations in a playful way. You won't forget "
                         "this trip! \n"
                         "So... Nice to meet you! Are you ready to have some fun together?".format(client.first_name))
    except KeyError:
        pass


def check_user_info(output, bot, clients):
    try:
        info = bot.get_user_info(output['entry'][0]['messaging'][0]['sender']['id'])
        current_client = get_client(info['id'], clients)
        if not current_client.information_filled:
            current_client.fill_public_info(info['first_name'], info['last_name'], info['profile_pic'])
        return current_client
    except KeyError:
        pass