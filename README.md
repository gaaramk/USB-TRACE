# 🛡️ USB-TRACE: Advanced Hardware & Behavioral Analyzer
**An Enterprise-Grade Endpoint Detection & Response (EDR) system designed to detect, mitigate, and report malicious USB threats (BadUSB/Rubber Ducky) using triple-layered intelligence.**

---

## 🎯 Architecture & Core Mechanisms
USB-TRACE operates beyond traditional signature-based detection. It utilizes a **Triple-Dimensional Radar** to identify sophisticated physical attacks:

1.  **🧠 Behavioral Typing DNA (Speed Radar):** Hooks into `/dev/input/` events to calculate the microsecond delta ($\Delta t$) between keystrokes. It instantly flags robotic typing patterns (e.g., $< 50ms$ variance) characteristic of DuckyScript payloads.
2.  **🔌 Hardware Power Fingerprinting:** Parses `sysfs` descriptors to uncover electrical anomalies. A device claiming to be a generic keyboard but drawing suspiciously high power ($> 100mA$) is flagged as a potential SoC-based implant.
3.  **🦠 Threat Intelligence Database:** Cross-references dynamic VID/PID pairs against a customized JSON database of known offensive security tools (e.g., Hak5 Bash Bunny, O.MG Cable), linking them to specific **MITRE ATT&CK** techniques.

---

## ⚡ Active Defense (Terminator Mode)
USB-TRACE is not just a monitoring tool; it is an active defense weapon. Upon evaluating a device as `High-Risk` via the central `RiskEngine`, it triggers the **Terminator Protocol**:
*   Interfaces directly with the Linux Kernel (`/sys/bus/usb/devices/`).
*   Executes an immediate `Unbind/Deauthorize` command.
*   **Result:** The port is electronically disabled within milliseconds, physically choking the malicious payload before execution completes.

---

## 📲 Cloud SOC Alerting & Forensic Reporting
To simulate a real-world enterprise environment, USB-TRACE features comprehensive incident response capabilities:
*   **Telegram Bot Integration:** Dispatches real-time, Markdown-formatted security alerts to a centralized SOC dashboard via the Telegram API, detailing threat classification and IOCs.
*   **Automated Forensics:** Generates immutable, timestamped reports in both **HTML** and **PDF** formats, preserving the chain of custody for post-incident analysis.

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
