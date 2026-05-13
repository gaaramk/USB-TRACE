import os
import sys
import time
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.db_manager import log_threat
from controllers.alert_manager import TelegramAlert

# مسار ملف قواعد الحظر الذي تقرأ منه لوحة القيادة
RULES_FILE = "/etc/udev/rules.d/99-usbtrace-blacklist.rules"

class StorageThreatReport:
    def __init__(self, device_name):
        self.risk_severity = "High"
        self.mitre_attack = "T1052 (Exfiltration) / T1091 (Removable Media)"
        self.intent = f"Unauthorized USB Storage ({device_name}) - Quarantined for Review"

class AIDeviceAlert:
    def __init__(self, report):
        self.risk_status = report.risk_severity
        self.vendor_id = "Storage"
        self.product_id = "USB Drive"
        self.threat_name = report.mitre_attack
        self.attack_type = report.intent

def get_usb_storage_devices():
    devices = set()
    try:
        output = subprocess.check_output(["lsblk", "-d", "-o", "NAME,TRAN"], text=True)
        for line in output.split('\n'):
            if 'usb' in line:
                dev_name = line.split()[0].strip()
                devices.add(dev_name)
    except Exception: pass
    return devices

def get_vid_pid(dev_name):
    """استخراج البصمة الفيزيائية (VID/PID) للفلاشة باستخدام udevadm"""
    try:
        output = subprocess.check_output(["udevadm", "info", "-q", "property", "-n", f"/dev/{dev_name}"], text=True)
        vid, pid = None, None
        for line in output.split('\n'):
            if line.startswith('ID_VENDOR_ID='):
                vid = line.split('=')[1].strip()
            if line.startswith('ID_MODEL_ID='):
                pid = line.split('=')[1].strip()
        return vid, pid
    except Exception:
        return None, None

def quarantine_device(vid, pid):
    """كتابة الفلاشة في ملف UDEV لتظهر في لوحة القيادة ويمكن فك حظرها"""
    rule = f'SUBSYSTEM=="usb", ATTRS{{idVendor}}=="{vid}", ATTRS{{idProduct}}=="{pid}", ATTR{{authorized}}="0"\n'
    try:
        with open(RULES_FILE, "a") as f:
            f.write(rule)
        subprocess.run(["sudo", "udevadm", "control", "--reload-rules"], check=True)
        subprocess.run(["sudo", "udevadm", "trigger"], check=True)
        return True
    except Exception as e:
        print(f"Error writing UDEV rule: {e}")
        return False

def monitor_storage():
    print("[*] Initializing Smart Storage EDR (Quarantine & Review Mode)...")
    baseline = get_usb_storage_devices()
    print(f"[+] Baseline secure. Trusted storage devices: {', '.join(baseline) if baseline else 'None'}")

    while True:
        current_devices = get_usb_storage_devices()
        new_devices = current_devices - baseline

        for dev in new_devices:
            dev_path = f"/dev/{dev}"
            print(f"\n🚨 [DETECTION] Unauthorized USB Storage detected: {dev}!")
            
            try:
                # 1. محاولة استخراج البصمة (VID/PID)
                vid, pid = get_vid_pid(dev)
                
                if vid and pid:
                    print(f"[*] Fingerprint Extracted -> VID: {vid} | PID: {pid}")
                    # 2. الحجر الصحي الذكي (سيتم إرسالها للوحة القيادة)
                    quarantine_device(vid, pid)
                    print(f"[+] Device {dev} Quarantined! Awaiting manual UNBLOCK from Dashboard.")
                else:
                    # في حال فشل استخراج البصمة، يتم طرد الفلاشة بالقوة כإجراء وقائي
                    sysfs_path = f"/sys/block/{dev}/device/delete"
                    if os.path.exists(sysfs_path):
                        subprocess.run(["sudo", "bash", "-c", f"echo 1 > {sysfs_path}"])
                        print(f"[+] Threat neutralized: Device forcefully EJECTED.")

                report = StorageThreatReport(dev)
                log_threat(dev_path, report.risk_severity, report.mitre_attack, report.intent, "Quarantined USB Storage")

                telegram = TelegramAlert()
                telegram.send_alert(AIDeviceAlert(report))

            except Exception as e:
                print(f"[-] Failed to handle {dev}: {e}")

            baseline.add(dev)

        baseline.intersection_update(current_devices)
        time.sleep(1)

if __name__ == "__main__":
    monitor_storage()