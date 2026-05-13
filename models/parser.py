import subprocess
import re
import hashlib
import os
from regipy.registry import RegistryHive
from models.device import USB_Device  # استدعاء الكلاس الخاص بالأجهزة

# ==========================================
# 1. دوال التشفير وحساب البصمة (Hashing)
# ==========================================

# دالة لحساب بصمة SHA256 لملف معين
def calculate_sha256(file_path):
    """حساب بصمة SHA256 لملف معين."""
    with open(file_path, 'rb') as f:
        # نقرأ محتوى الملف بالكامل في الذاكرة (يمكن تحسين هذا لملفات كبيرة باستخدام قراءة أجزاء)
        file_data = f.read()
        # نحسب البصمة باستخدام hashlib ونرجع النتيجة في شكل نصي (hexadecimal)
        return hashlib.sha256(file_data).hexdigest()

# دالة جديدة لحساب بصمة SHA256 لنص معين (مثل مخرجات dmesg) بدلاً من ملف
def calculate_text_sha256(text_data):
    """حساب بصمة SHA256 لنص معين بعد تحويله إلى بايتات."""
    return hashlib.sha256(text_data.encode('utf-8')).hexdigest()


# ==========================================
# 2. دوال تحليل نظام لينكس (Linux / dmesg)
# ==========================================

def get_dmesg_log():
    """تنفيذ أمر dmesg وجلب سجل أحداث النظام."""
    try:
        result = subprocess.run(['dmesg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error running dmesg: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception while running dmesg: {e}")
        return None
    
    
    # في بيئة الاختبار، سنستخدم ملف نصي وهمي يحتوي على سجل dmesg بدلاً من تنفيذ الأمر الحقيقي
#def get_dmesg_log():
#    """قراءة سجل الأحداث من ملف وهمي لأغراض الاختبار."""
#    try:
#        # نفتح الملف الوهمي الموجود في نفس المجلد في وضع القراءة
#        with open("dummy_dmesg.txt", "r", encoding="utf-8") as f:
#            return f.read()
#    except Exception as e:
#        print(f"Error reading dummy file: {e}")
#        return None


# تحليل سجل dmesg لاستخراج بيانات أجهزة USB المتصلة والمنفصلة
def parse_dmesg(log):
    """تحليل سجل dmesg لاستخراج بيانات أجهزة USB المتصلة والمنفصلة."""
    devices_list = [] 
            
    for line in log.splitlines():
        # البحث عن نمط اتصال جهاز جديد: [timestamp] idVendor=XXXX, idProduct=XXXX
        result = re.search(r"\[([0-9. ]+)\].*idVendor=([0-9a-fA-F]+).*idProduct=([0-9a-fA-F]+)", line)
        
        # البحث عن نمط فصل الجهاز: [timestamp] usb disconnect
        usb_disconnect = re.search(r"\[([0-9. ]+)\].*usb disconnect", line)
        
        if result:
            timestamp = result.group(1).strip()
            vendor_id = result.group(2)
            product_id = result.group(3)
            
            # إنشاء كائن الجهاز (الرقم التسلسلي غير متوفر في هذا السطر)
            new_device = USB_Device(None, timestamp, vendor_id, product_id, None)
            devices_list.append(new_device)
        
        elif usb_disconnect:
            timestamp = usb_disconnect.group(1).strip()
            
            # تحديث وقت الفصل لآخر جهاز تم رصده في القائمة
            if devices_list:
                last_device = devices_list[-1]
                last_device.disconnect_time = timestamp
        
        elif "hid" in line.lower() or "keyboard" in line.lower():
            # إذا كان الجهاز هو جهاز إدخال (HID)، نحدد ذلك في الكائن
            if devices_list:
                last_device = devices_list[-1]
                last_device.isHid = True
                
    return devices_list


    """فحص سجل dmesg لاكتشاف أجهزة HID المخفية التي قد تشير إلى هجمات BadUSB."""
    hid_devices = []
    
    for line in log.splitlines():
        if "hid" in line.lower() or "keyboard" in line.lower():
            result = re.search(r"\[([0-9. ]+)\].*idVendor=([0-9a-fA-F]+).*idProduct=([0-9a-fA-F]+)", line)
            if result:
                timestamp = result.group(1).strip()
                vendor_id = result.group(2)
                product_id = result.group(3)
                hid_devices.append((timestamp, vendor_id, product_id))
    
    return hid_devices

# دالة جديدة لفحص الواجهات المخفية (Hidden Interfaces) في نظام لينكس
def detect_hidden_interfaces():
    usb_path = '/sys/bus/usb/devices/'
    suspicious_devices = []

    # 1. الحلقة الأولى: المرور على مجلدات الأجهزة (الآباء)
    for device_folder in os.listdir(usb_path):
        device_path = os.path.join(usb_path, device_folder)

        # نتحقق إذا كان هذا المجلد يحتوي على ملف "idVendor" و "idProduct"
        if os.path.isfile(os.path.join(device_path, "idVendor")) and os.path.isfile(os.path.join(device_path, "idProduct")):
            with open(os.path.join(device_path, "idVendor"), 'r') as f:
                vendor_id = f.read().strip()
            with open(os.path.join(device_path, "idProduct"), 'r') as f:
                product_id = f.read().strip()
            

        # 2. الحلقة الثانية (الداخلية): المرور على مجلدات الواجهات (الأبناء)
        # for sub_folder in ... :
        for sub_folder in os.listdir(device_path):
            sub_folder_path = os.path.join(device_path, sub_folder)
            interface_file = os.path.join(sub_folder_path, "bInterfaceClass")
            
            if os.path.isfile(interface_file):
                with open(interface_file, 'r') as f:
                    interface_class = f.read().strip()
                
                # 3. إذا كان class يساوي 03 (HID)، فهذا قد يكون جهاز إدخال مخفي
                if interface_class == "03":
                    suspicious_devices.append((vendor_id, product_id, device_folder, sub_folder))
    return suspicious_devices

# ==========================================
# 3. دوال تحليل نظام ويندوز (Windows Registry)
# ==========================================

def parse_windows_registry(hive_path):
    """تحليل ملف سجل ويندوز (Hive) لاستخراج تاريخ أجهزة USBSTOR."""
    devices_list = []
    # المسار القياسي لأجهزة USB داخل السجل
    usbstor_path = r'\ControlSet001\Enum\USBSTOR'
    
    try:
        # فتح ملف السجل (Registry Hive)
        hive = RegistryHive(hive_path)
        
        # المرور على مفاتيح الأجهزة داخل USBSTOR
        for device_key in hive.iter_subkeys(usbstor_path):
            device_name = device_key.name 
            
            # استخراج VID (Vendor ID) و PID (Product ID) من اسم المفتاح
            vid_match = re.search(r'Ven_([A-Za-z0-9]+)', device_name)
            pid_match = re.search(r'Prod_([A-Za-z0-9]+)', device_name)
            
            vendor_id = vid_match.group(1) if vid_match else "Unknown"
            product_id = pid_match.group(1) if pid_match else "Unknown"
            
            # استخراج الرقم التسلسلي من المجلدات الفرعية للمفتاح الحالي
            for serial_key in hive.iter_subkeys(device_key.path):
                serial_number = serial_key.name
                
                # إنشاء كائن الجهاز وإضافته للقائمة
                new_device = USB_Device(serial_number, None, vendor_id, product_id)
                devices_list.append(new_device)
                
    except Exception as e:
        print(f"Error parsing registry: {e}")
        
    return devices_list