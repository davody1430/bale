import google.generativeai as genai
import openai
import logging
from config import Config

logger = logging.getLogger(__name__)

class AIManager:
    def __init__(self):
        self.current_model = Config.DEFAULT_MODEL
        
        # تنظیم کلیدهای API
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
        
        if Config.OPENAI_API_KEY:
            openai.api_key = Config.OPENAI_API_KEY
    
    def set_model(self, model_name):
        """تغییر مدل فعال"""
        if model_name in Config.MODELS:
            self.current_model = model_name
            logger.info(f"Model changed to: {model_name}")
            return True, f"✅ مدل به {Config.MODELS[model_name]['name']} تغییر کرد"
        return False, f"❌ مدل '{model_name}' یافت نشد"
    
    def get_model_info(self):
        """اطلاعات مدل فعلی"""
        model_config = Config.MODELS.get(self.current_model, {})
        return {
            "id": self.current_model,
            "name": model_config.get("name", "Unknown"),
            "provider": model_config.get("provider", "unknown")
        }
    
    def list_models(self):
        """لیست مدل‌های موجود"""
        return [
            {
                "id": model_id,
                "name": info["name"],
                "provider": info["provider"],
                "is_current": model_id == self.current_model
            }
            for model_id, info in Config.MODELS.items()
        ]
    
    def generate_response(self, user_message, chat_history=None):
        """تولید پاسخ بر اساس مدل انتخابی"""
        model_config = Config.MODELS.get(self.current_model)
        
        if not model_config:
            return "❌ مدل انتخابی نامعتبر است"
        
        provider = model_config["provider"]
        
        try:
            if provider == "google":
                return self._generate_gemini(user_message, chat_history, model_config)
            elif provider == "openai":
                return self._generate_openai(user_message, chat_history, model_config)
            else:
                return "❌ ارائه‌دهنده مدل پشتیبانی نمی‌شود"
                
        except Exception as e:
            logger.error(f"AI generation error: {e}")
            return f"⚠️ خطا در تولید پاسخ: {str(e)}"
    
    def _generate_gemini(self, user_message, chat_history, model_config):
        """تولید پاسخ با Gemini"""
        try:
            # تنظیم مدل Gemini
            model = genai.GenerativeModel(model_config["id"])
            
            # ساخت محتوا با تاریخچه چت
            if chat_history:
                # برای Gemini باید کل تاریخچه را بفرستیم
                chat = model.start_chat(history=[])
                # اضافه کردن تاریخچه
                for msg in chat_history[-6:]:  # آخرین ۶ پیام
                    chat.send_message(msg.get("user", ""))
                    if msg.get("assistant"):
                        # Gemini نیاز به پاسخ قبلی هم دارد
                        pass
                
                response = chat.send_message(user_message)
            else:
                # چت ساده
                prompt = f"""به عنوان یک دستیار فارسی هوشمند پاسخ بده. پاسخ باید:
                1. مختصر و مفید باشد
                2. به زبان فارسی روان باشد
                3. اگر نمی‌دانی، صادقانه بگو
                
                سوال کاربر: {user_message}
                
                پاسخ:"""
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=model_config.get("temperature", 0.7),
                        max_output_tokens=model_config.get("max_tokens", 2000),
                    )
                )
            
            if response.text:
                return response.text
            else:
                return "❌ Gemini پاسخی تولید نکرد"
                
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            # بررسی خطاهای خاص Gemini
            if "quota" in str(e).lower():
                return "⚠️ سهمیه استفاده از Gemini به پایان رسیده است"
            elif "safety" in str(e).lower():
                return "⚠️ پاسخ به دلیل محدودیت‌های امنیتی مسدود شد"
            else:
                return f"⚠️ خطا در Gemini: {str(e)}"
    
    def _generate_openai(self, user_message, chat_history, model_config):
        """تولید پاسخ با OpenAI"""
        if not Config.OPENAI_API_KEY:
            return "❌ کلید OpenAI تنظیم نشده است"
        
        try:
            messages = []
            
            # اضافه کردن سیستم پرامپت
            messages.append({
                "role": "system",
                "content": "تو یک دستیار فارسی هستی. پاسخ‌ها را مختصر، مفید و به زبان فارسی روان بده."
            })
            
            # اضافه کردن تاریخچه چت
            if chat_history:
                for msg in chat_history[-10:]:  # آخرین ۱۰ پیام
                    if msg.get("user"):
                        messages.append({"role": "user", "content": msg["user"]})
                    if msg.get("assistant"):
                        messages.append({"role": "assistant", "content": msg["assistant"]})
            
            # اضافه کردن پیام فعلی
            messages.append({"role": "user", "content": user_message})
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=model_config.get("temperature", 0.7),
                max_tokens=model_config.get("max_tokens", 1000),
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return f"⚠️ خطا در OpenAI: {str(e)}"