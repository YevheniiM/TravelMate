from dialogflow.api import get_intent
from game_core.progress import Progress
from dialogflow.intents import Intents
from helpers.facebook_api import send_message
from helpers.bot_responses import GREETING_RESPONSE_1, GREETING_RESPONSE_2, GREETING_RESPONSE_3, HARD_TO_RECOGNIZE


def greeting_part(client, intent, bot):
    """The function describes the greeting part of conversation with client.

    It starts the tour if user is agreed and if the user knows how to play
    with the bot. In other case it explains all the needed details.

    :param client: [Client] - the current client to chat with
    :param response: [String] - the client response to the bot
    :param bot: [pymessenger.bot.Bot]

    """
    if client.progress == Progress.are_you_ready_w:
        if intent == Intents.agreement:
            send_message(bot, client.client_id, GREETING_RESPONSE_1)
            client.update_progress(Progress.how_it_works_w)
        elif intent == Intents.disagreement:
            user_does_not_start_the_tour(client, bot)
    elif client.progress == Progress.how_it_works_w:
        if intent == Intents.agreement:
            send_message(bot, client.client_id, "starting the tour...")
            client.update_progress(Progress.tour_started)
            # TODO: starting the tour
        elif intent == Intents.disagreement:
            send_message(bot, client.client_id, GREETING_RESPONSE_2)
            client.update_progress(Progress.want_to_start)
    elif client.progress == Progress.want_to_start:
        if intent == Intents.agreement:
            send_message(bot, client.client_id, "starting the tour...")
            client.update_progress(Progress.tour_started)
            # TODO: starting the tour
        elif intent == Intents.disagreement:
            user_does_not_start_the_tour(client, bot)
    elif client.progress == Progress.tour_does_not_start:
        if intent == Intents.agreement:
            send_message(bot, client.client_id, "starting the tour...")
            client.update_progress(Progress.tour_started)
        elif intent == Intents.disagreement:
            user_does_not_start_the_tour(client, bot)


def user_does_not_start_the_tour(client, bot):
    send_message(bot, client.client_id, GREETING_RESPONSE_3.format(client.first_name))
    client.update_progress(Progress.tour_does_not_start)
