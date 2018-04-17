from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('iAJNjyrOPPm1ahAobtCY8SClSbekUSvOAPiXQ+4um3QXn90wUOZ8CmIas/mqrBL7lF4KvaHR7TzuZoVIa/35Yd2pzd4p8v6NJo40QvayqnwOcBCqi9l04eSEuDWd9TX+HeILSiA2yNAKL+HkTzzRAgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('aaff4eff258de58ae6d92f4d497b8e47')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()