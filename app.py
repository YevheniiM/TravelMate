from pymessenger.bot import Bot
from flask import Flask, request

from dialogflow.api import get_intent, get_fulfillment_message, get_intent_name, detect_query
from dialogflow.intents import Intents
from game_core.progress import Progress
from helpers.secret_constants import ACCESS_TOKEN
from game_core.logic_parts import greeting_part
from helpers.facebook_api import verify_fb_token, send_message
from helpers.client_api import check_get_started, process_current_client

clients = dict()
app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        return verify_fb_token(request, request.args.get("hub.verify_token"))
    else:
        output = request.get_json()
        current_client = process_current_client(output, bot, clients)
        check_get_started(current_client, output, bot)

        for event in output['entry']:
            try:
                messaging = event['messaging']

                for message in messaging:
                    if message.get('message'):
                        client_response = message['message'].get('text')

                        if not client_response:
                            return "There was not a client response"

                        query = detect_query(current_client.session_id, client_response)
                        intent_name = get_intent_name(query)
                        fulfillment_text = get_fulfillment_message(query)

                        from pprint import pprint
                        pprint(intent_name)
                        pprint(fulfillment_text)

                        if intent_name == Intents.default or intent_name == "" or intent_name == "Default Welcome Intent":
                            send_message(bot, current_client.client_id, str(fulfillment_text))

                        elif current_client.progress.value < Progress.tour_started.value:
                            greeting_part(client=current_client, intent=get_intent(query).display_name, bot=bot)
                        else:
                            send_message(bot, current_client.client_id, "Tour has been already started.")
            except KeyError as e:
                print(e)

    return "Message Processed"


if __name__ == "__main__":
    app.run(port=8000)
