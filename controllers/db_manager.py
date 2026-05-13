import sqlite3
import os
from datetime import datetime

# مسار ملف قاعدة البيانات (سيتم إنشاؤه في المجلد الرئيسي للمشروع)
DB_FILE = "usb_trace.db"

def init_db():
    """إنشاء قاعدة البيانات وجدول الهجمات إذا لم يكن موجوداً"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # بناء هيكل الجدول (الأعمدة المطلوبة لتسجيل الهجوم)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS threat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        device_path TEXT,
        severity TEXT,
        mitre_tactic TEXT,
        intent TEXT,
        payload TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[*] SQLite Database initialized successfully at: {DB_FILE}")

def log_threat(device_path, severity, mitre_tactic, intent, payload=""):
    """حقن هجوم جديد في قاعدة البيانات (سيستخدمها الرادار)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
    INSERT INTO threat_logs (timestamp, device_path, severity, mitre_tactic, intent, payload)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, device_path, severity, mitre_tactic, intent, payload))
    
    conn.commit()
    conn.close()

def get_recent_threats(limit=50):
    """استدعاء أحدث الهجمات (ستستخدمها لوحة القيادة لعرض البيانات)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # جلب البيانات وترتيبها من الأحدث للأقدم
    cursor.execute('''
    SELECT timestamp, device_path, severity, mitre_tactic, intent 
    FROM threat_logs 
    ORDER BY id DESC LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # تحويل البيانات إلى قواميس (JSON format) ليفهمها المتصفح
    threats = []
    for row in rows:
        threats.append({
            "timestamp": row[0],
            "device": row[1],
            "severity": row[2],
            "mitre": row[3],
            "intent": row[4]
        })
    return threats

if __name__ == "__main__":
    # عند تشغيل هذا الملف بشكل مباشر، سيقوم ببناء قاعدة البيانات
    init_db()