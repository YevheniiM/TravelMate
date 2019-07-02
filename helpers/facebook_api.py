from helpers.secret_constants import VERIFY_TOKEN


def verify_fb_token(request, token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid verification token'


def send_message(bot, recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return 'Success'
