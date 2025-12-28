import os
from dotenv import load_dotenv

load_dotenv()  # بارگذاری متغیرهای محیطی

class Config:
    # توکن ربات بله
    BOT_TOKEN = os.getenv("BALE_BOT_TOKEN")
    
    # کلیدهای API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # تنظیمات مدل‌ها
    DEFAULT_MODEL = "gemini-pro"  # مدل پیش‌فرض
    MODELS = {
        "gemini-pro": {
            "name": "Gemini Pro",
            "provider": "google",
            "max_tokens": 30720,
            "temperature": 0.7
        },
        "gpt-3.5": {
            "name": "GPT-3.5 Turbo",
            "provider": "openai",
            "max_tokens": 4096,
            "temperature": 0.7
        }
    }
    
    # تنظیمات ربات
    USE_AI = True
    MAX_RESPONSE_LENGTH = 2000
    LOG_FILE = "logs/bot_logs.log"
    
    @classmethod
    def validate(cls):
        """بررسی صحت تنظیمات"""
        errors = []
        if not cls.BOT_TOKEN:
            errors.append("❌ توکن ربات بله تنظیم نشده (BALE_BOT_TOKEN)")
        if not cls.GEMINI_API_KEY:
            errors.append("⚠️  کلید Gemini تنظیم نشده (GEMINI_API_KEY)")
        return errors