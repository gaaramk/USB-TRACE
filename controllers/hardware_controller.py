import os
import glob

def read_sys_attr(device_path, attr_name):
    """
    دالة مساعدة لقراءة خصائص الجهاز من ملفات نظام لينكس (sysfs) بشكل آمن.
    """
    filepath = os.path.join(device_path, attr_name)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except Exception:
            return "ERROR"
    return "N/A"

def get_hardware_fingerprints():
    """
    يقوم بفحص منافذ الـ USB واستخراج البصمة المادية لكل جهاز، 
    ثم يحلل استهلاك الطاقة مقارنة بوظيفة الجهاز المكتشفة.
    """
    results = []
    # البحث عن جميع منافذ USB المتصلة بالنظام
    usb_devices = glob.glob('/sys/bus/usb/devices/*-*')
    
    if not usb_devices:
        return results

    for device_path in usb_devices:
        # تجاهل مداخل الـ Hub الداخلية في اللوحة الأم
        if "usb" in device_path.split('/')[-1]:
            continue
            
        vid = read_sys_attr(device_path, "idVendor")
        # تخطي الأجهزة الوهمية التي لا تمتلك Vendor ID حقيقي
        if vid == "N/A":
            continue

        pid = read_sys_attr(device_path, "idProduct")
        mfg = read_sys_attr(device_path, "manufacturer")
        prod = read_sys_attr(device_path, "product")
        max_power = read_sys_attr(device_path, "bMaxPower")
        usb_ver = read_sys_attr(device_path, "version")
        
        # تجهيز هيكل البيانات الخاص بالجهاز (Dictionary)
        device_info = {
            "vid": vid,
            "pid": pid,
            "product": prod,
            "manufacturer": mfg,
            "usb_version": usb_ver,
            "max_power": max_power,
            "is_suspicious": False,
            "anomaly_reason": "None"
        }
        
        # محرك التحليل الاستدلالي (Heuristic Engine)
        if max_power != "N/A":
            try:
                # استخراج القيمة الرقمية لاستهلاك الطاقة (مثلاً 500 من 500mA)
                power_val = int(''.join(filter(str.isdigit, max_power)))
                
                # البحث عن مسار واجهة الجهاز (Interface Class)
                interface_path = glob.glob(f"{device_path}:*.0")
                
                if interface_path:
                    # قراءة فئة الواجهة (03 تعني أجهزة HID مثل الكيبورد)
                    intf_class = read_sys_attr(interface_path[0], "bInterfaceClass")
                    
                    # كمين الطاقة: إذا كان الجهاز يدعي أنه كيبورد بسيط ولكنه يسحب طاقة عالية
                    if intf_class == "03" and power_val > 100: 
                        device_info["is_suspicious"] = True
                        device_info["anomaly_reason"] = f"Claimed HID (Keyboard) but draws {max_power} (Power Anomaly)"
            except ValueError:
                pass
        
        results.append(device_info)
        
    return results