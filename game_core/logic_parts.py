from dialogflow.api import get_intent
from game_core.progress import Progress
from dialogflow.intents import Intents
from helpers.facebook_api import send_message


def greeting_part(client, response, bot):
    intent = get_intent(client.session_id, response)
    if client.progress == Progress.are_you_ready_w:
        if intent == Intents.agreement:
            send_message(bot,
                         client.client_id,
                         "Great! We’ve made an Insta Tour for you this time! Do you know how it works?")
            client.update_progress(Progress.how_it_works_w)
        elif intent == Intents.disagreement:
            user_does_not_start_the_tour(client)
        else:
            send_message(bot, client.client_id, "Hard to recognize :(")
    elif client.progress == Progress.how_it_works_w:
        if intent == Intents.agreement:
            send_message(bot,
                         client.client_id,
                         "starting the tour...")
            client.update_progress(Progress.tour_started)
            # TODO: starting the tour
        elif intent == Intents.disagreement:
            send_message(bot,
                         client.client_id,
                         "Alright, let me explain you in a few words how our tours work. "
                         "Basically, it’s a quest. We’ve found and put together locations "
                         "that are both instagram-worthy and interesting, also places to "
                         "have some food, drink and fun! You will be having tasks on where "
                         "to go and what to do. After you accomplish one, you will be told "
                         "about next one, and so on. "
                         "Wanna start?")
            client.update_progress(Progress.want_to_start)
        else:
            send_message(bot, client.client_id, "Hard to recognize :(")
    elif client.progress == Progress.want_to_start:
        if intent == Intents.agreement:
            send_message(bot,
                         client.client_id,
                         "starting the tour...")
            client.update_progress(Progress.tour_started)
            # TODO: starting the tour
        elif intent == Intents.disagreement:
            user_does_not_start_the_tour(client)
        else:
            send_message(bot, client.client_id, "Hard to recognize :(")
    elif client.progress == Progress.tour_does_not_start:
        if intent == Intents.agreement:
            send_message(bot,
                         client.client_id,
                         "starting the tour...")
            client.update_progress(Progress.tour_started)
        elif intent == Intents.disagreement:
            user_does_not_start_the_tour(client)
        else:
            send_message(bot, client.client_id, "Hard to recognize :(")


def user_does_not_start_the_tour(client, bot):
    send_message(bot,
                 client.client_id,
                 "Sad to hear that, {}. But that’s not a problem! "
                 "When would you like to carry on with this trip?".format(client.name))
    client.update_progress(Progress.tour_does_not_start)
