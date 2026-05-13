# 🛡️ USB-TRACE: AI-Powered Unified EDR System

**USB-TRACE** is an advanced, Enterprise-Grade Endpoint Detection and Response (EDR) system specifically engineered for Linux environments. It provides deep kernel-level monitoring, dynamic honeypots, and AI-driven forensic analysis to defend against rogue hardware and malicious USB peripherals.

## 🚀 Key Features

* **Deep Kernel Radar (Anti-BadUSB):** Intercepts keystrokes at the raw hardware layer (`evdev`) to detect inhuman typing speeds indicative of Rubber Ducky or BadUSB attacks.
* **Smart Honeypot Isolation:** Instantly grabs exclusive control of malicious input devices, blinding the host OS while safely capturing the injected payload.
* **AI-Powered Forensic Analyst:** Integrates with Gemini AI to analyze intercepted payloads, determine the attacker's intent, and map the attack to **MITRE ATT&CK** tactics (e.g., T1059, T1071).
* **Rogue Network Defense:** Detects and immediately neutralizes unauthorized network interfaces (e.g., PoisonTap, Bash Bunny) attempting traffic hijacking.
* **Smart Storage Quarantine:** Intercepts untrusted Mass Storage devices, extracts their hardware fingerprints (VID/PID), and places them in a UDEV quarantine blocklist.
* **Centralized SOC Dashboard:** A Flask-based web interface serving as a Command Center to monitor live threat feeds, review AI reports, and manage the Active UDEV Blacklist.
* **SQLite Threat Archive:** Maintains a permanent, searchable database of all historical threat events for post-incident forensic analysis.

## ⚙️ Architecture (Microservices)
The system operates using a unified orchestration script (`app.py`) that deploys three distinct background daemon shields:
1. `speed_controller.py`: Keystroke injection monitoring.
2. `network_radar.py`: Network adapter hijacking prevention.
3. `storage_radar.py`: Auto-run & Data Exfiltration deterrence.

## 🛠️ Prerequisites
* **OS:** Kali Linux (or Debian-based system with `udev` and `evdev` support).
* **Python:** Python 3.x with a configured virtual environment (`venv`).
* **Privileges:** `root` access is strictly required for Kernel manipulation and UDEV rule reloading.

## 📦 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/gaaramk/USB-TRACE.git](https://github.com/gaaramk/USB-TRACE.git)
   cd USB-TRACE
Run the Unified EDR Engine:

Bash
sudo venv/bin/python app.py
Navigate the Toolkit:

Select [1] to initialize the Forensic SQLite Database (First run only).

Select [2] to launch the SOC Web Dashboard (Accessible at http://127.0.0.1:5000).

Select [3] to ignite all EDR shields in the background.

⚠️ Disclaimer
This project was developed as a graduation project to demonstrate advanced concepts in Cybersecurity, Kernel interaction, and Threat Intelligence. It is intended for educational and defensive purposes only.




---

## 🚀 Installation & Usage

**Requirements:**
*   Linux OS (Debian/Ubuntu/Kali recommended)
*   Python 3.8+
*   Root privileges (required for Terminator Mode)

**Setup:**
```bash
# Clone the repository
git clone [https://github.com/YourUsername/usb-trace.git](https://github.com/YourUsername/usb-trace.git)
cd usb-trace

# Set up the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Execution:

Bash
# MUST be run with sudo to enable Port Deauthorization
sudo ./venv/bin/python app.py
Developed by Mohamed Kamal El-dein | Built for Advanced Hardware Forensics
# USB-TRACE.
# USB-TRACE.
# USB-TRACE.
# USB-TRACE.


## 📦 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/gaaramk/USB-TRACE.git](https://github.com/gaaramk/USB-TRACE.git)
   cd USB-TRACE
