from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 你的 Channel Access Token 與 Channel Secret
line_bot_api = LineBotApi('DGAwp+loaZXLJFaMrtQwdFtUy0ANb8UWontj5espiXHjKnnZvZcjtpqF05jRj8UsxDPAznBT5Xfdz3Q/yGI5ng+Th/dS5Ta5CJfCb6GrDjbhpJan1yspuxMwv+vC5wgTjaRyRAYNKGnMzmHXpb5EBQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('242ead87541e17927f571d7f1e351dcc')

# 內存變數累加總支出（簡單個人用）
total_expense = 0

# 測試連線用
@app.route("/", methods=['GET'])
def home():
    return "LINE Bot is running!"

# LINE webhook route
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print("Webhook error:", e)
    return 'OK'  # LINE 必須在 webhook 立刻收到 200

# 處理訊息
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
        except:
            reply = "請輸入：項目 金額\n例如：午餐 120"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# Render 必須使用環境變數 PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
