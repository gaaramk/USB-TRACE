import os
import sys
import time
import subprocess

# التأكد من تشغيل اللوحة بصلاحيات النواة (Root)
if os.geteuid() != 0:
    print("\n[!] ERROR: USB-TRACE must be run as ROOT!")
    print("    Please use: sudo venv/bin/python app.py\n")
    sys.exit(1)

# ألوان الواجهة
C = '\033[96m'
G = '\033[92m'
Y = '\033[93m'
R = '\033[91m'
W = '\033[0m'

def clear_screen():
    os.system('clear')

def print_banner():
    banner = f"""{C}
    ██╗   ██╗███████╗██████╗       ████████╗██████╗  █████╗  ██████╗███████╗
    ██║   ██║██╔════╝██╔══██╗      ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██║   ██║███████╗██████╔╝█████╗   ██║   ██████╔╝███████║██║     █████╗  
    ██║   ██║╚════██║██╔══██╗╚════╝   ██║   ██╔══██╗██╔══██║██║     ██╔══╝  
    ╚██████╔╝███████║██████╔╝         ██║   ██║  ██║██║  ██║╚██████╗███████╗
     ╚═════╝ ╚══════╝╚═════╝          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝
    {W}"""
    print(banner)
    print(f"{Y}    === AI-Powered USB Endpoint Detection & Response (EDR) ==={W}\n")

def start_all_shields():
    print(f"\n{C}[*] Igniting USB-TRACE Unified EDR Engine...{W}")
    
    # تشغيل الرادارات الثلاثة في الخلفية
    subprocess.Popen(["venv/bin/python", "controllers/speed_controller.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen(["venv/bin/python", "controllers/network_radar.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen(["venv/bin/python", "controllers/storage_radar.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(2)
    print(f"{G}[+] Keystroke Radar (Anti-BadUSB) : ONLINE{W}")
    print(f"{G}[+] Network Radar (Anti-PoisonTap): ONLINE{W}")
    print(f"{G}[+] Storage Radar (Anti-Malware)  : ONLINE{W}")
    print(f"{G}[+] All kernel shields are UP and running in the background!{W}")
    time.sleep(2)

def stop_all_shields():
    print(f"\n{Y}[*] Shutting down all EDR services...{W}")
    # قتل كل العمليات المرتبطة بالرادارات
    os.system("pkill -f 'controllers/speed_controller.py'")
    os.system("pkill -f 'controllers/network_radar.py'")
    os.system("pkill -f 'controllers/storage_radar.py'")
    time.sleep(1)
    print(f"{R}[-] All shields are DOWN.{W}")
    time.sleep(1)

def start_dashboard():
    print(f"\n{G}[*] Launching SOC Web Dashboard...{W}")
    subprocess.Popen(["venv/bin/python", "web_dashboard.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{G}[+] Dashboard is running at: http://127.0.0.1:5000 {W}")
    time.sleep(2)

def main():
    while True:
        clear_screen()
        print_banner()
        print(f"  {G}[1]{W} Initialize SQLite Database")
        print(f"  {G}[2]{W} Start SOC Web Dashboard")
        print(f"  {Y}[3]{W} Enable ALL EDR Shields (Keyboard, Network, Storage)")
        print(f"  {R}[4]{W} Disable ALL EDR Shields")
        print(f"  {C}[5]{W} Exit")
        print("")
        
        choice = input(f"  {C}usb-trace > {W}")

        if choice == '1':
            os.system("venv/bin/python controllers/db_manager.py")
            time.sleep(2)
        elif choice == '2':
            start_dashboard()
        elif choice == '3':
            start_all_shields()
        elif choice == '4':
            stop_all_shields()
        elif choice == '5':
            stop_all_shields()
            # إيقاف خادم الويب أيضاً عند الخروج
            os.system("pkill -f 'web_dashboard.py'")
            print(f"\n{G}Thank you for using USB-TRACE. Goodbye!{W}\n")
            sys.exit(0)
        else:
            print(f"\n{R}[!] Invalid option.{W}")
            time.sleep(1)

if __name__ == "__main__":
    main()