import os
import subprocess

class ActiveDefense:
    def __init__(self):
        # المسار الرسمي لقواعد udev في لينكس
        self.rules_file = "/etc/udev/rules.d/99-usbtrace-blacklist.rules"

    def extract_vid_pid_from_event(self, event_path):
        """تستخرج الـ Vendor ID و Product ID من مسار الكيبورد المكتشف"""
        try:
            # تحويل المسار إلى المسار الحقيقي في sysfs
            event_name = os.path.basename(os.path.realpath(event_path))
            sysfs_path = f"/sys/class/input/{event_name}/device/id"
            
            with open(f"{sysfs_path}/vendor", "r") as f:
                vid = f.read().strip()
            with open(f"{sysfs_path}/product", "r") as f:
                pid = f.read().strip()
                
            return vid, pid
        except Exception as e:
            print(f"[-] Could not extract VID/PID: {e}")
            return None, None

    def block_device(self, vid, pid):
        """كتابة قاعدة حظر دائمة تقطع الاتصال عن الجهاز"""
        # صياغة قاعدة الحظر (تمنع تصريح العمل Authorized=0)
        rule = f'SUBSYSTEM=="usb", ATTRS{{idVendor}}=="{vid}", ATTRS{{idProduct}}=="{pid}", ATTR{{authorized}}="0"\n'
        
        try:
            # التحقق مما إذا كان الجهاز محظوراً مسبقاً لمنع التكرار
            if os.path.exists(self.rules_file):
                with open(self.rules_file, "r") as f:
                    if rule in f.read():
                        print(f"[*] Device {vid}:{pid} is already blacklisted.")
                        return True

            # كتابة القاعدة
            with open(self.rules_file, "a") as f:
                f.write(rule)
                
            # إجبار نظام لينكس على قراءة القاعدة وتطبيقها فوراً
            subprocess.run(["udevadm", "control", "--reload-rules"], check=True)
            subprocess.run(["udevadm", "trigger"], check=True)
            
            print(f"[🛡️ ACTIVE DEFENSE] FATAL STRIKE! Device {vid}:{pid} has been permanently blocked at the kernel level!")
            return True
        except Exception as e:
            print(f"[-] Active Defense Failed: {e}")
            return False