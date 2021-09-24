from flask import Flask, request, abort
import os
import search
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

@app.route("/", methods=['GET'])
def hello():
    return "hello"

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
    input_message = event.message.text
    first = input_message.split("\n")[0]
    result = first.split(" ")[1:]
    if input_message.startswith("plz"): #特定の文字列から始まるなら
        url = search.one_include_http(" ".join(result))
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(event.reply_token,image_message)
        #by debug
        # mage_message = TextSendMessage(text=url)
        # line_bot_api.reply_message(event.reply_token,mage_message)

    # get url
    if input_message.startswith("url"):
        url = search.one_include_http(" ".join(result))
        text_message = TextSendMessage(text=url)
        line_bot_api.reply_message(event.reply_token,text_message)

    # そうじゃないならとりあえず何もしない

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
