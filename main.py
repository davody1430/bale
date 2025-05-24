from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "ربات بله من آماده‌ست!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("پیام دریافت شد:", data)

    chat_id = data.get("message", {}).get("chat", {}).get("id")
    text = data.get("message", {}).get("text", "")

    if chat_id and text:
        answer = f"پیام شما دریافت شد: {text}"
        url = f"https://tapi.bale.ai/bot1353714060:HcnS6jUAdQGVKu1FwRsRtCA15ZrJjMYfuFH5vmCa/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": answer})

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
