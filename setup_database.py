import sqlite3
import json

def init_database():
    conn = sqlite3.connect('database/bot_database.db')
    c = conn.cursor()
    
    # جدول دانش پایه
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question TEXT UNIQUE,
                  answer TEXT,
                  usage_count INTEGER DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # اضافه کردن داده‌های اولیه
    with open('knowledge/qa_pairs.json', 'r', encoding='utf-8') as f:
        qa_pairs = json.load(f)
    
    for q, a in qa_pairs.items():
        c.execute("INSERT OR IGNORE INTO knowledge_base (question, answer) VALUES (?, ?)", 
                 (q, a))
    
    conn.commit()
    conn.close()
    print("✅ دیتابیس ایجاد شد!")

if __name__ == "__main__":
    init_database()