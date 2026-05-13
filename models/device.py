class USB_Device:
    def __init__(self, serial_number, insert_time, vendor_id, product_id, disconnect_time=None):
        self.threat_name = "USB_Device"
        self.serial_number = serial_number
        self.insert_time = insert_time        
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.disconnect_time = disconnect_time
        self.connected = disconnect_time is None
        self.duration = None
        self.isHid = False
        self.mitigation_actions = []
        
        # === المتغيرات الجديدة المضافة للفحص المادي والهيكلي ===
        self.manufacturer = "Unknown"
        self.usb_version = "Unknown"
        self.max_power = "N/A"
        
        
        # === Advanced Threat Intelligence Variables ===
        self.mitre_id = "N/A"
        self.attack_type = "N/A"
        self.ioc_indicators = "N/A"

    def __str__(self):
        return f"USB_Device(serial_number={self.serial_number}, insert_time={self.insert_time}, vendor_id={self.vendor_id}, product_id={self.product_id}, disconnect_time={self.disconnect_time}, mitigation_actions={self.mitigation_actions}, threat_name={self.threat_name}, connected={self.connected}, duration={self.duration}, isHid={self.isHid}, manufacturer={self.manufacturer}, max_power={self.max_power})"