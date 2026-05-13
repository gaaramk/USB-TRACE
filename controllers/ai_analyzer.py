import google.generativeai as genai
import json

class AIAnalyzer:
    def __init__(self, api_key):
        # 🔑 إعداد مفتاح الـ API الخاص بك هنا
        genai.configure(api_key="AIzaSyB3KIn_JFRUFVgsSTLqEEwseGXa7x4FNAM")
        # نستخدم نموذج Flash لسرعته الفائقة في تحليل النصوص
        self.model = genai.GenerativeModel('gemini-2.5-flash')    

    def analyze_payload(self, payload_text):
        print("[🧠 AI] Sending intercepted payload to Gemini for forensic analysis...")
        
        # 📝 هندسة الأوامر: إجبار الذكاء الاصطناعي على صيغة JSON
        prompt = f"""
        You are an expert Cybersecurity Incident Responder. 
        Analyze the following intercepted USB keystroke payload.
        You MUST respond ONLY in valid JSON format. Do not add markdown code blocks or any other text.
        
        The JSON MUST strictly follow this structure:
        {{
            "intent": "Brief explanation of what the script is trying to do",
            "iocs": ["Extract any IPs, Domains, URLs, or specific file paths. Empty list if none"],
            "impact": "What is the potential damage if this executed?",
            "mitigation": "Immediate steps to defend against this specific threat",
            "risk_severity": "Must be exactly one of: Low, Medium, High, Critical",
            "mitre_attack": "Related MITRE ATT&CK technique (e.g., T1059)"
        }}

        Payload to analyze:
        {payload_text}
        """

        try:
            # إرسال الطلب للنموذج
            response = self.model.generate_content(prompt)
            
            # تنظيف الرد للتأكد من أنه JSON صالح
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
                
            # تحويل النص إلى قاموس بايثون (Dictionary)
            report_data = json.loads(response_text)
            return report_data
            
        except Exception as e:
            print(f"[-] AI Analysis Failed: {e}")
            return None