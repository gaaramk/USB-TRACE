import requests

class TelegramAlert:
    def __init__(self):
        # التوكن والـ ID الخاصين بك (جاهزان للعمل)
        self.bot_token = "8749112458:AAGkRKT6kX-4CXmpxXNW8tBgfS8Rp3I1D9s"
        self.chat_id = "6311079878"
        
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_alert(self, device):
        # تم إصلاح الفخ البرمجي هنا! (نتحقق فقط إذا كان فارغاً)
        if self.bot_token.strip() == "" or self.bot_token == "ضع_التوكن_هنا":
            print("[-] Telegram SOC alerting is disabled. Configure tokens first.")
            return

        # صياغة رسالة الإنذار بشكل احترافي (Markdown)
        message = (
            "🚨 *USB-TRACE SECURITY ALERT* 🚨\n\n"
            f"⚠️ *Threat Level:* {getattr(device, 'risk_status', 'High-Risk')}\n"
            f"🔌 *Device Identity:* {device.vendor_id}:{device.product_id}\n"
            f"🦠 *Threat Name:* {getattr(device, 'threat_name', 'Unknown Threat')}\n"
            f"💀 *Attack Type:* {getattr(device, 'attack_type', 'N/A')}\n"
            f"🛡️ *Action Taken:* Port Auto-Disabled (Terminator Mode) ⚡\n\n"
            "🔍 _Check the local forensic report for full details._"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            # إرسال الطلب إلى خوادم تليجرام
            response = requests.post(f"{self.base_url}/sendMessage", json=payload)
            
            # فحص حالة الرد من تليجرام
            if response.status_code == 200:
                print("[+] SOC Alert sent to Telegram successfully! 📲")
            else:
                print(f"[-] Failed to send Telegram alert. HTTP Status: {response.status_code}")
                
        except Exception as e:
            print(f"[-] Telegram connection error: {e}")