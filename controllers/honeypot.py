import evdev
from evdev import ecodes
import time

class UsbHoneypot:
    def __init__(self):
        # خريطة مبسطة لتحويل إشارات الكيبورد إلى حروف مقروءة
        self.key_map = {
            'KEY_A': 'a', 'KEY_B': 'b', 'KEY_C': 'c', 'KEY_D': 'd', 'KEY_E': 'e',
            'KEY_F': 'f', 'KEY_G': 'g', 'KEY_H': 'h', 'KEY_I': 'i', 'KEY_J': 'j',
            'KEY_K': 'k', 'KEY_L': 'l', 'KEY_M': 'm', 'KEY_N': 'n', 'KEY_O': 'o',
            'KEY_P': 'p', 'KEY_Q': 'q', 'KEY_R': 'r', 'KEY_S': 's', 'KEY_T': 't',
            'KEY_U': 'u', 'KEY_V': 'v', 'KEY_W': 'w', 'KEY_X': 'x', 'KEY_Y': 'y',
            'KEY_Z': 'z', 'KEY_SPACE': ' ', 'KEY_ENTER': '\n', 'KEY_DOT': '.',
            'KEY_SLASH': '/', 'KEY_MINUS': '-', 'KEY_1': '1', 'KEY_2': '2',
            'KEY_3': '3', 'KEY_4': '4', 'KEY_5': '5', 'KEY_6': '6', 'KEY_7': '7',
            'KEY_8': '8', 'KEY_9': '9', 'KEY_0': '0', 'KEY_LEFTSHIFT': '',
            'KEY_RIGHTSHIFT': '', 'KEY_CAPSLOCK': '', 'KEY_TAB': '\t',
            'KEY_BACKSPACE': '', 'KEY_ESC': '', 'KEY_UP': '', 'KEY_DOWN': '',
            'KEY_LEFT': '', 'KEY_RIGHT': '', 'KEY_COMMA': ',', 'KEY_SEMICOLON': ';',
            'KEY_APOSTROPHE': "'", 'KEY_GRAVE': '`', 'KEY_LEFTBRACE': '[',
            'KEY_RIGHTBRACE': ']', 'KEY_BACKSLASH': '\\', 'KEY_EQUAL': '='
        }

    def capture_payload(self, device_path, capture_duration=5):
        captured_script = ""
        try:
            device = evdev.InputDevice(device_path)
            device.grab()
            print(f"\n[🪤 HONEYPOT] Device {device_path} grabbed successfully! OS is now blind to it.")
            print(f"[*] Recording payload for {capture_duration} seconds...")

            start_time = time.time()
            
            for event in device.read_loop():
                if time.time() - start_time > capture_duration:
                    break
                
                if event.type == ecodes.EV_KEY and event.value == 1:
                    key_event = evdev.categorize(event)
                    keycode = key_event.keycode
                    
                    if isinstance(keycode, list):
                        keycode = keycode[0]
                        
                    if keycode in self.key_map:
                        captured_script += self.key_map[keycode]
                    elif keycode == 'KEY_ENTER':
                        captured_script += "\n"

            device.ungrab()
            print("\n[+] Payload capture complete!")
            return captured_script.strip()

        # 🔥 التعديل الجديد: اصطياد خطأ اختفاء الجهاز (Errno 19 أو Errno 2)
        except OSError as e:
            if getattr(e, 'errno', None) in [19, 2] or 'No such device' in str(e):
                print("\n[!] Device vanished during capture (Ghosted!). Saving intercepted data...")
                return captured_script.strip()
            print(f"\n[!] OSError: {e}")
            return captured_script.strip()

        except PermissionError:
            print("[!] Permission Denied: Run with sudo to use the Honeypot.")
            return None
        except Exception as e:
            print(f"[!] Honeypot Error: {e}")
            return captured_script.strip() if captured_script else None