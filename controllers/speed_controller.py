import os
import time
import select
import evdev
from datetime import datetime

from controllers.honeypot import UsbHoneypot
from controllers.ai_analyzer import AIAnalyzer
from controllers.alert_manager import TelegramAlert
from controllers.active_defense import ActiveDefense
from controllers.db_manager import log_threat  # 🔥 استدعاء مهندس قاعدة البيانات

class AIDeviceAlert:
    def __init__(self, ai_report):
        self.risk_status = ai_report.get("risk_severity", "High-Risk")
        self.vendor_id = "AI"
        self.product_id = "Intercepted"
        self.threat_name = ai_report.get("mitre_attack", "T1059")
        self.attack_type = ai_report.get("intent", "Malicious Keystroke Injection")

def get_all_keyboards():
    kbds = []
    for path in evdev.list_devices():
        try:
            device = evdev.InputDevice(path)
            if evdev.ecodes.EV_KEY in device.capabilities():
                kbds.append(path)
        except Exception: pass
    return kbds

def analyze_keystroke_speed():
    print("[*] Initializing EVDEV-Native Omni-Directional Radar (SQLite Integrated)...")
    active_devices = {} 
    last_times = {}   
    histories = {}    
    
    while True:
        current_kbds = get_all_keyboards()
        for kbd in current_kbds:
            if kbd not in active_devices:
                try:
                    dev = evdev.InputDevice(kbd)
                    active_devices[kbd] = dev
                    last_times[kbd] = 0.0
                    histories[kbd] = []
                    print(f"[+] Radar attached to new device: {kbd}")
                except Exception: pass
        
        disconnected = [k for k in active_devices.keys() if k not in current_kbds]
        for k in disconnected:
            active_devices[k].close()
            del active_devices[k]
            del last_times[k]
            del histories[k]
            print(f"[-] Device disconnected: {k}")

        if not active_devices:
            time.sleep(1)
            continue

        readable, _, _ = select.select(list(active_devices.values()), [], [], 1.0)
        for dev in readable:
            try:
                for event in dev.read():
                    if event.type == evdev.ecodes.EV_KEY and event.value == 1: 
                        current_time = event.timestamp()
                        last_time = last_times[dev.path]
                        
                        if last_time != 0.0:
                            diff = current_time - last_time
                            if 0 <= diff <= 0.15: 
                                histories[dev.path].append(diff)
                                if len(histories[dev.path]) >= 5:
                                    print(f"\n🚨 [DETECTION] Robotic typing detected on {dev.path}!")
                                    trap = UsbHoneypot()
                                    payload = trap.capture_payload(dev.path, capture_duration=8)
                                    
                                    if payload:
                                        ai = AIAnalyzer(api_key="AIzaSyB3KIn_JFRUFVgsSTLqEEwseGXa7x4FNAM") 
                                        report = ai.analyze_payload(payload)
                                        
                                        if report and report.get('risk_severity') in ["High", "Critical"]:
                                            print("[+] Threat Verified! Sending Telegram Alert & Logging to SQLite...")
                                            telegram = TelegramAlert()
                                            telegram.send_alert(AIDeviceAlert(report))
                                            
                                            # 🔥 حقن الهجوم في قاعدة البيانات الأبدية 🔥
                                            log_threat(
                                                device_path=dev.path,
                                                severity=report.get("risk_severity", "Unknown"),
                                                mitre_tactic=report.get("mitre_attack", "Unknown"),
                                                intent=report.get("intent", "Unknown"),
                                                payload=payload
                                            )
                                            
                                            print("[*] Initiating Active Defense Protocol...")
                                            defense = ActiveDefense()
                                            vid, pid = defense.extract_vid_pid_from_event(dev.path)
                                            if vid and pid:
                                                defense.block_device(vid, pid)
                                            else:
                                                print("[-] Virtual Device Detected: Cannot extract physical VID/PID for UDEV blocking!")
                                        else:
                                            print("[*] Analysis complete: Low risk or false alarm.")
                                    histories[dev.path].clear()
                                    time.sleep(2) 
                            else:
                                histories[dev.path].clear() 
                        last_times[dev.path] = current_time
            except Exception: pass

if __name__ == "__main__":
    analyze_keystroke_speed()