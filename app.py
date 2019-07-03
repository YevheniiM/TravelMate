from pymessenger.bot import Bot
from flask import Flask, request

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

                        if current_client.progress.value < Progress.tour_started.value:
                            greeting_part(client=current_client, response=client_response, bot=bot)
                        else:
                            send_message(bot, current_client.client_id, "Tour has been already started.")
            except KeyError:
                pass

    return "Message Processed"


if __name__ == "__main__":
    app.run(port=5000)
