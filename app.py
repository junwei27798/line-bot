from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# ✅ 把這裡改成你自己的 Token 與 Secret
line_bot_api = LineBotApi('DGAwp+loaZXLJFaMrtQwdFtUy0ANb8UWontj5espiXHjKnnZvZcjtpqF05jRj8UsxDPAznBT5Xfdz3Q/yGI5ng+Th/dS5Ta5CJfCb6GrDjbhpJan1yspuxMwv+vC5wgTjaRyRAYNKGnMzmHXpb5EBQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e45cafafae3ca8b8db075a92203363b3')

# 內存變數記錄總支出（簡單個人用）
total_expense = 0

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return 'OK'  # LINE webhook 必須回 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global total_expense
    text = event.message.text.strip()

    if text == "總額":
        reply = f"目前總支出：{total_expense} 元"
    else:
        try:
            item, amount = text.split()
            amount = int(amount)
            total_expense += amount
            reply = f"已記錄：{item} {amount} 元"
        except Exception as e:
            reply = "請輸入：項目 金額\n例如：午餐 120"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    # Render 必須用 PORT 環境變數
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
