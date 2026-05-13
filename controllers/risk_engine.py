import json
import os
import subprocess
from controllers.alert_manager import TelegramAlert 

class RiskEngine:
    def __init__(self):
        # Defining the core rules and limits of the evaluation engine
        self.suspicious_limit = 40
        self.high_risk_limit = 70
        self.threat_db = self.load_threats()

    def load_threats(self):
        # Load the advanced threat intelligence database
        with open(os.path.join(os.path.dirname(__file__), "../config/threats.json"), "r") as f:
            return json.load(f)

    def terminate_device(self, vendor_id, product_id):
        """
        [Active Defense] Terminates a USB device by deauthorizing its port via sysfs.
        """
        base_path = "/sys/bus/usb/devices/"
        try:
            # البحث عن مسار الجهاز في النظام بناءً على VID و PID
            for device_dir in os.listdir(base_path):
                dir_path = os.path.join(base_path, device_dir)
                vid_path = os.path.join(dir_path, "idVendor")
                pid_path = os.path.join(dir_path, "idProduct")

                if os.path.exists(vid_path) and os.path.exists(pid_path):
                    with open(vid_path, 'r') as f_vid, open(pid_path, 'r') as f_pid:
                        current_vid = f_vid.read().strip()
                        current_pid = f_pid.read().strip()

                        # إذا وجدنا الجهاز المشبوه
                        if current_vid == vendor_id and current_pid == product_id:
                            auth_path = os.path.join(dir_path, "authorized")
                            
                            # تنفيذ حكم الإعدام بقطع التصريح (Deauthorization)
                            # يتطلب صلاحيات Root
                            with open(auth_path, 'w') as auth_file:
                                auth_file.write("0")
                                
                            print(f"\n[⚡ TERMINATOR MODE ⚡] Port {device_dir} successfully disabled!")
                            print(f"[*] The device ({vendor_id}:{product_id}) has been isolated from the kernel.")
                            return True
        except PermissionError:
            print("\n[!] MITIGATION FAILED: Root privileges required to disable USB ports. Run with 'sudo'.")
            return False
        except Exception as e:
            print(f"\n[!] MITIGATION ERROR: {str(e)}")
            return False
            
        return False

    def evaluate(self, device):
        score = 0
        
        # 1. Serial Number Check
        if device.serial_number is None or device.serial_number == "N/A":
            score += 15
            
        # 2. Unknown Identity Check
        if device.vendor_id == "Unknown":
            score += 20
        
        # 3. HID Functionality Check
        if getattr(device, 'isHid', False):
            score += 15 
            
        # ==========================================
        # ⚡ Electrical Anomaly Check ⚡
        # ==========================================
        if hasattr(device, 'max_power') and device.max_power != "N/A":
            try:
                power_val = int(''.join(filter(str.isdigit, device.max_power)))
                if getattr(device, 'isHid', False) and power_val > 100:
                    score += 50 
                    device.mitigation_actions.append(f"Hardware Anomaly: High Power ({device.max_power}) detected.")
            except ValueError:
                pass
        
        # 4. Connection Duration Check
        if getattr(device, 'disconnect_time', None) is not None:
            duration = float(device.disconnect_time) - float(device.insert_time)
            if duration < 10:  
                score += 50 
                device.mitigation_actions.append("Behavioral Warning: Suspiciously short connection time.")
        else:  
            score += 5   
        
        # 5. Threat Database Matching (JSON Intelligence)
        if device.vendor_id != "Unknown" and device.product_id != "Unknown":
            for threat in self.threat_db:
                if device.vendor_id == threat["vid"] and device.product_id == threat["pid"]:
                    score += threat["score"]
                    device.threat_name = threat["name"]
                    device.attack_type = threat.get("attack_type", "N/A")
                    
                    mitre = threat.get("mitre_attack_id", [])
                    device.mitre_id = ", ".join(mitre) if isinstance(mitre, list) else mitre
                    device.ioc_indicators = threat.get("ioc_indicators", "N/A")
                    
                    mitigation = threat.get("mitigation_actions", [])
                    device.mitigation_actions.extend(mitigation)
                    break         

        # 6. Final Risk Determination & Active Mitigation
        if score >= self.high_risk_limit:
            status = "High-Risk"
            device.risk_status = status # يجب تعيين الحالة قبل الإرسال
            
            # 🔥 تفعيل سلاح الردع
            device.mitigation_actions.append("ACTION TAKEN: Port Auto-Disabled by Terminator Engine.")
            self.terminate_device(device.vendor_id, device.product_id)
            
            # 📲 إرسال الإنذار السحابي
            alerter = TelegramAlert()
            alerter.send_alert(device)
            
        elif score >= self.suspicious_limit:
            status = "Suspicious"
        else:
            status = "Normal"
            
        device.risk_status = status 
        return status