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
