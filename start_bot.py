#!/usr/bin/env python3
"""
اسکریپت راه‌اندازی آسان ربات بله
"""

import os
import sys
import subprocess
import time
import webbrowser
from colorama import init, Fore, Style

init(autoreset=True)

def print_header():
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════╗
║         راه‌انداز ربات بله              ║
╚══════════════════════════════════════════╝
""")

def check_requirements():
    """بررسی نیازمندی‌ها"""
    print(Fore.YELLOW + "🔍 بررسی نیازمندی‌ها...")
    
    required = ['flask', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(Fore.RED + f"❌ کتابخانه‌های زیر نصب نیستند: {', '.join(missing)}")
        print(Fore.GREEN + "📦 در حال نصب...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    
    print(Fore.GREEN + "✅ همه نیازمندی‌ها نصب هستند")

def setup_environment():
    """تنظیم محیط"""
    print(Fore.YELLOW + "\n⚙️  تنظیم محیط...")
    
    # ایجاد فایل .env اگر وجود ندارد
    if not os.path.exists('.env'):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("""# تنظیمات ربات بله
BALE_BOT_TOKEN=توکن_ربات_خود_را_اینجا_قرار_دهید
GEMINI_API_KEY=کلید_gemini_اختیاری

# برای ngrok (اختیاری)
NGROK_AUTHTOKEN=توکن_ngrok_اختیاری
""")
        print(Fore.GREEN + "✅ فایل .env ایجاد شد")
        print(Fore.YELLOW + "⚠️  لطفاً توکن ربات را در فایل .env وارد کنید")
    else:
        print(Fore.GREEN + "✅ فایل .env موجود است")

def start_bot():
    """راه‌اندازی ربات"""
    print(Fore.YELLOW + "\n🚀 در حال راه‌اندازی ربات...")
    
    # بررسی توکن
    with open('.env', 'r') as f:
        content = f.read()
        if 'توکن_ربات_خود_را_اینجا_قرار_دهید' in content:
            print(Fore.RED + "❌ لطفاً توکن ربات را در فایل .env قرار دهید")
            input("Enter برای ویرایش فایل .env...")
            webbrowser.open('.env')
            return
    
    # اجرای ربات در پس‌زمینه
    print(Fore.GREEN + "✅ ربات در حال اجرا است...")
    print(Fore.CYAN + "\n🌐 آدرس‌های مهم:")
    print(Fore.WHITE + "   • کنترل پنل: http://localhost:10000")
    print(Fore.WHITE + "   • تنظیم وب‌هوک: http://localhost:10000/setwebhook")
    print(Fore.WHITE + "   • اطلاعات ربات: http://localhost:10000/botinfo")
    
    print(Fore.YELLOW + "\n💡 نکته: برای آدرس عمومی:")
    print(Fore.WHITE + "   1. در ترمینال جدید: ngrok http 10000")
    print(Fore.WHITE + "   2. آدرس https:// را کپی کنید")
    print(Fore.WHITE + "   3. در مرورگر: http://localhost:10000/setwebhook")
    
    # اجرای main.py
    subprocess.Popen([sys.executable, "main.py"])
    
    # باز کردن مرورگر
    time.sleep(2)
    webbrowser.open('http://localhost:10000')

if __name__ == '__main__':
    print_header()
    check_requirements()
    setup_environment()
    start_bot()
    
    print(Fore.GREEN + "\n🎉 آماده است! ربات در مرورگر باز شد.")
    print(Fore.YELLOW + "برای توقف ربات: Ctrl+C در این ترمینال")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n⏹️  ربات متوقف شد")
