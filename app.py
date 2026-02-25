from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import sqlite3
import os

app = Flask(__name__)

line_bot_api = LineBotApi('DGAwp+loaZXLJFaMrtQwdFtUy0ANb8UWontj5espiXHjKnnZvZcjtpqF05jRj8UsxDPAznBT5Xfdz3Q/yGI5ng+Th/dS5Ta5CJfCb6GrDjbhpJan1yspuxMwv+vC5wgTjaRyRAYNKGnMzmHXpb5EBQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e45cafafae3ca8b8db075a92203363b3')

# 建立資料庫
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS expense (amount INTEGER)')
conn.commit()
conn.close()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()

    # 查詢總額
    if text == "總額":
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT SUM(amount) FROM expense")
        total = c.fetchone()[0] or 0
        conn.close()
        reply = f"目前總支出：{total} 元"

    # 記帳
    else:
        try:
            item, amount = text.split()
            amount = int(amount)

            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute("INSERT INTO expense (amount) VALUES (?)", (amount,))
            conn.commit()
            conn.close()

            reply = f"已記錄：{item} {amount} 元"
        except:
            reply = "請輸入：項目 金額\n例如：午餐 120"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 取得 Render 指定的 PORT
    app.run(host="0.0.0.0", port=port)
