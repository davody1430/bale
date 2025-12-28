from flask import Flask, request, jsonify
import requests
import sqlite3
import os
import logging
from datetime import datetime
import threading
import time

app = Flask(__name__)

# تنظیمات
BOT_TOKEN = os.getenv("BALE_BOT_TOKEN", "1353714060:AAHdnS6jUAdQGVKu1FwRsRtCA15ZrJjMYfuFH5vmCa")
WEBHOOK_URL = " https://your-public-url.com/webhook"  # 🔴 این را تغییر دهید
PORT = 10000

# تنظیم لاگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_webhook():
    """تنظیم خودکار وب‌هوک در بله"""
    try:
        url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/setWebhook"
        data = {"url": WEBHOOK_URL}
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"✅ وب‌هوک با موفقیت تنظیم شد: {WEBHOOK_URL}")
            return True
        else:
            logger.error(f"❌ خطا در تنظیم وب‌هوک: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ خطا در اتصال به بله: {e}")
        return False

def delete_webhook():
    """حذف وب‌هوک (برای تست)"""
    try:
        url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/deleteWebhook"
        response = requests.get(url, timeout=10)
        logger.info(f"وب‌هوک حذف شد: {response.json()}")
    except Exception as e:
        logger.error(f"خطا در حذف وب‌هوک: {e}")

def get_bot_info():
    """دریافت اطلاعات ربات"""
    try:
        url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("ok"):
            bot_info = data.get("result", {})
            logger.info(f"🤖 اطلاعات ربات: {bot_info.get('first_name')} (@{bot_info.get('username')})")
            return bot_info
        else:
            logger.error(f"❌ خطا در دریافت اطلاعات ربات: {data}")
            return None
            
    except Exception as e:
        logger.error(f"❌ خطا در دریافت اطلاعات: {e}")
        return None

def send_message(chat_id, text, parse_mode="HTML"):
    """ارسال پیام به کاربر"""
    try:
        url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage"
        
        # محدودیت طول پیام
        if len(text) > 4096:
            text = text[:4000] + "\n\n... (متن کوتاه شد)"
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            logger.error(f"خطا در ارسال پیام: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"خطا در ارسال پیام: {e}")
        return False

@app.route('/')
def index():
    """صفحه اصلی"""
    return '''
    <h1>🤖 ربات بله با Gemini AI</h1>
    <p>✅ ربات فعال است</p>
    <p><a href="/setwebhook">تنظیم وب‌هوک</a></p>
    <p><a href="/deletewebhook">حذف وب‌هوک</a></p>
    <p><a href="/botinfo">اطلاعات ربات</a></p>
    <p>آدرس وب‌هوک: ''' + WEBHOOK_URL + '''</p>
    '''

@app.route('/setwebhook')
def set_webhook_page():
    """صفحه تنظیم وب‌هوک"""
    success = setup_webhook()
    if success:
        return "<h1>✅ وب‌هوک تنظیم شد!</h1>"
    else:
        return "<h1>❌ خطا در تنظیم وب‌هوک</h1>"

@app.route('/deletewebhook')
def delete_webhook_page():
    """صفحه حذف وب‌هوک"""
    delete_webhook()
    return "<h1>وب‌هوک حذف شد</h1>"

@app.route('/botinfo')
def bot_info_page():
    """صفحه اطلاعات ربات"""
    info = get_bot_info()
    if info:
        return f'''
        <h1>🤖 اطلاعات ربات</h1>
        <p>نام: {info.get('first_name', 'نامشخص')}</p>
        <p>یوزرنیم: @{info.get('username', 'نامشخص')}</p>
        <p>شناسه: {info.get('id', 'نامشخص')}</p>
        <p>توکن: {BOT_TOKEN[:15]}...</p>
        '''
    else:
        return "<h1>❌ خطا در دریافت اطلاعات</h1>"

@app.route('/webhook', methods=['POST'])
def webhook():
    """دریافت پیام از بله"""
    try:
        # دریافت داده
        data = request.json
        
        if not data:
            logger.warning("داده خالی دریافت شد")
            return "ok", 200
        
        # استخراج اطلاعات پیام
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '').strip()
        from_user = message.get('from', {})
        
        if not chat_id:
            logger.warning("chat_id پیدا نشد")
            return "ok", 200
        
        logger.info(f"پیام از {chat_id}: {text}")
        
        # پاسخ به دستور /start
        if text == '/start':
            welcome_text = '''
            🤖 سلام! من یک ربات هوشمند هستم
            
            🔧 قابلیت‌ها:
            • پاسخ به سوالات با هوش مصنوعی
            • پشتیبانی از زبان فارسی
            • پاسخ‌های سریع و دقیق
            
            💡 فقط سوال خود را بپرسید!
            
            👤 سازنده: @YourUsername
            '''
            send_message(chat_id, welcome_text)
        
        # پاسخ به دستور /help
        elif text == '/help':
            help_text = '''
            📚 راهنمای ربات:
            
            /start - شروع کار با ربات
            /help - نمایش این راهنما
            /about - درباره ربات
            /ping - تست اتصال
            
            💬 برای استفاده، کافیست سوال خود را تایپ کنید.
            ربات با استفاده از هوش مصنوعی به شما پاسخ خواهد داد.
            '''
            send_message(chat_id, help_text)
        
        # پاسخ به دستور /about
        elif text == '/about':
            about_text = f'''
            ℹ️ درباره این ربات:
            
            • نسخه: 1.0
            • پلتفرم: بله (Bale)
            • هوش مصنوعی: Gemini Pro
            • زبان: فارسی
            • توسعه‌دهنده: شما
            
            🔗 کانال پشتیبانی: @ChannelName
            👨‍💻 گزارش مشکل: @SupportUsername
            '''
            send_message(chat_id, about_text)
        
        # پاسخ به دستور /ping
        elif text == '/ping':
            send_message(chat_id, '🏓 پونگ! ربات فعال است.')
        
        # پردازش پیام‌های عادی
        elif text:
            # اینجا می‌توانید کد AI خود را فراخوانی کنید
            # برای مثال فعلاً یک پاسخ ساده می‌دهیم
            
            ai_response = f'''
            🤖 پاسخ ربات:
            
            سوال شما: {text}
            
            (در این بخش پاسخ هوش مصنوعی قرار می‌گیرد)
            
            💡 برای اتصال به Gemini، کلید API را در فایل .env قرار دهید.
            '''
            
            send_message(chat_id, ai_response)
        
        return "ok", 200
        
    except Exception as e:
        logger.error(f"خطا در پردازش وب‌هوک: {e}")
        return "error", 500

@app.route('/test', methods=['GET'])
def test_message():
    """تست ارسال پیام (برای مدیر)"""
    try:
        # ارسال پیام تست به خودتان
        # شناسه چت خود را اینجا قرار دهید
        YOUR_CHAT_ID = "123456789"  # 🔴 این را تغییر دهید
        
        test_msg = '''
        🔧 تست ربات بله
        
        این یک پیام تست است.
        اگر این پیام را دریافت می‌کنید، ربات شما فعال است!
        
        ✅ تاریخ: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''
        🌐 وب‌هوک: ''' + WEBHOOK_URL + '''
        
        ربات آماده دریافت پیام‌هاست.
        '''
        
        success = send_message(YOUR_CHAT_ID, test_msg)
        
        if success:
            return "<h1>✅ پیام تست ارسال شد!</h1>"
        else:
            return "<h1>❌ خطا در ارسال پیام تست</h1>"
            
    except Exception as e:
        return f"<h1>❌ خطا: {str(e)}</h1>"

def start_bot():
    """تابع اصلی راه‌اندازی ربات"""
    logger.info("=" * 50)
    logger.info("🚀 در حال راه‌اندازی ربات بله...")
    logger.info("=" * 50)
    
    # نمایش اطلاعات
    print("\n" + "=" * 50)
    print("🤖 ربات بله هوشمند")
    print("=" * 50)
    
    # بررسی توکن
    if BOT_TOKEN == "1353714060:AAHdnS6jUAdQGVKu1FwRsRtCA15ZrJjMYfuFH5vmCa":
        print("⚠️  هشدار: توکن ربات تنظیم نشده است!")
        print("لطفاً توکن ربات خود را در فایل .env قرار دهید.")
        print("BALE_BOT_TOKEN=توکن_شما")
    else:
        print(f"✅ توکن ربات: {BOT_TOKEN[:15]}...")
    
    # دریافت اطلاعات ربات
    bot_info = get_bot_info()
    if bot_info:
        print(f"🤖 نام ربات: {bot_info.get('first_name')}")
        print(f"📌 یوزرنیم: @{bot_info.get('username')}")
    
    print(f"🌐 پورت: {PORT}")
    print(f"🔗 آدرس محلی: http://localhost:{PORT}")
    print(f"📌 وب‌هوک: {WEBHOOK_URL}")
    print("\n📋 دستورات:")
    print("  http://localhost:10000/setwebhook   - تنظیم وب‌هوک")
    print("  http://localhost:10000/deletewebhook - حذف وب‌هوک")
    print("  http://localhost:10000/botinfo      - اطلاعات ربات")
    print("  http://localhost:10000/test         - ارسال پیام تست")
    print("\n" + "=" * 50)

# یا این کد را به main.py اضافه کنید:
@app.route('/getmyid')
def get_my_id():
    import json
    # آخرین پیام را بررسی کن
    url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    updates = response.json().get("result", [])
    
    if updates:
        last_update = updates[-1]
        chat_id = last_update.get("message", {}).get("chat", {}).get("id")
        return f"Chat ID شما: {chat_id}"
    return "چتی یافت نشد"


if __name__ == '__main__':
    # شروع ربات
    start_bot()
    
    # اجرای سرور Flask
    app.run(host='0.0.0.0', port=PORT, debug=True, threaded=True)