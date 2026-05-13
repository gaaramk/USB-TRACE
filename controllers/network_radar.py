import os
import sys
import time
import subprocess

#  إصلاح مسار لغة بايثون لكي تتعرف على مجلدات المشروع الرئيسية
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.db_manager import log_threat
from controllers.alert_manager import TelegramAlert

class NetworkThreatReport:
    def __init__(self, iface):
        self.risk_severity = "Critical"
        self.mitre_attack = "T1200 (Hardware Additions) / T1040 (Network Sniffing)"
        self.intent = f"Rogue Network Adapter ({iface}) - Possible PoisonTap/Bash Bunny Hijack"

class AIDeviceAlert:
    def __init__(self, report):
        self.risk_status = report.risk_severity
        self.vendor_id = "Network"
        self.product_id = "Adapter"
        self.threat_name = report.mitre_attack
        self.attack_type = report.intent

def get_interfaces():
    """جلب كل كروت الشبكة المتصلة حالياً بالنظام"""
    try:
        return set(os.listdir('/sys/class/net/'))
    except FileNotFoundError:
        return set()

def monitor_network():
    print("[*] Initializing Network EDR (PoisonTap / Bash Bunny Radar)...")
    baseline = get_interfaces()
    print(f"[+] Baseline secure. Trusted interfaces: {', '.join(baseline)}")

    while True:
        current_interfaces = get_interfaces()
        # اكتشاف أي كارت شبكة جديد
        new_interfaces = current_interfaces - baseline

        for iface in new_interfaces:
            iface_path = f"/sys/class/net/{iface}"
            
            # استبعاد الكروت الوهمية الخاصة بلينكس
            if iface.startswith(('veth', 'docker', 'br-', 'lo')):
                baseline.add(iface)
                continue

            print(f"\n🚨 [DETECTION] Rogue Network Interface detected: {iface}!")
            
            try:
                # الردع الفوري: إغلاق كارت الشبكة وإسقاطه
                subprocess.run(["sudo", "ip", "link", "set", "dev", iface, "down"], check=False)
                print(f"[+] Threat neutralized: Interface '{iface}' forced OFFLINE.")

                report = NetworkThreatReport(iface)

                log_threat(
                    device_path=iface_path,
                    severity=report.risk_severity,
                    mitre_tactic=report.mitre_attack,
                    intent=report.intent,
                    payload="Network Traffic Hijack Attempt Blocked"
                )

                print("[*] Sending Telegram Alert & Dashboard Log...")
                telegram = TelegramAlert()
                telegram.send_alert(AIDeviceAlert(report))

            except Exception as e:
                print(f"[-] Failed to neutralize {iface}: {e}")

            baseline.add(iface)

        baseline.intersection_update(current_interfaces)
        time.sleep(1)

if __name__ == "__main__":
    monitor_network()