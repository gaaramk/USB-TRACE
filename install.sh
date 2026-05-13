#!/bin/bash

# التحقق من صلاحيات الروت
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run this script with sudo."
  exit
fi

# تحديد مسار المشروع الحالي تلقائياً
PROJECT_DIR=$(pwd)
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
RADAR_SCRIPT="$PROJECT_DIR/controllers/speed_controller.py"

echo "[*] Generating systemd service file..."

# إنشاء ملف الخدمة وتوجيهه مباشرة لسكريبت الرادار (speed_controller.py)
cat <<EOF > /etc/systemd/system/usb-trace.service
[Unit]
Description=USB-TRACE Deep Kernel EDR Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
# حرف u- يمنع بايثون من تخزين السجلات ليتم عرضها فوراً (Live Logs)
ExecStart=$VENV_PYTHON -u $RADAR_SCRIPT
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# تفعيل الخدمة في نظام لينكس
echo "[*] Reloading systemd daemon..."
systemctl daemon-reload
systemctl enable usb-trace.service
systemctl restart usb-trace.service

echo "[+] USB-TRACE Deep Radar is now installed and running in the background!"