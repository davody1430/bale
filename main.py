from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "ربات بله من آماده‌ست!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("پیام دریافت شد:", data)
    # اینجا می‌تونی کد پردازش پیام رو بنویسی
    return "ok", 200

if __name__ == "__main__":
    # روی پورت 10000 اجرا می‌کنیم چون Render همین پورت رو قبول داره
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
