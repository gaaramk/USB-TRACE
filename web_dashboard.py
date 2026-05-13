from flask import Flask, render_template, jsonify
import os
import subprocess
from controllers.db_manager import get_recent_threats

app = Flask(__name__)

RULES_FILE = "/etc/udev/rules.d/99-usbtrace-blacklist.rules"

@app.route('/')
def index():
    return render_template('index.html')

# 🔥 مسار جديد لصفحة السجل التاريخي
@app.route('/history')
def history_page():
    return render_template('history.html')

@app.route('/api/blocked')
def get_blocked_devices():
    blocked_devices = []
    if os.path.exists(RULES_FILE):
        try:
            with open(RULES_FILE, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if 'ATTRS{idVendor}' in line:
                        parts = line.split(',')
                        vid = parts[1].split('==')[1].strip(' "')
                        pid = parts[2].split('==')[1].strip(' "')
                        blocked_devices.append({"vid": vid, "pid": pid, "status": "Terminated 💀"})
        except Exception as e:
            print(f"Error reading rules: {e}")
    return jsonify(blocked_devices)

@app.route('/api/unblock/<vid>/<pid>', methods=['POST'])
def unblock_device(vid, pid):
    try:
        with open(RULES_FILE, "r") as f:
            lines = f.readlines()
        new_lines = [line for line in lines if not (f'ATTRS{{idVendor}}=="{vid}"' in line and f'ATTRS{{idProduct}}=="{pid}"' in line)]
        with open(RULES_FILE, "w") as f:
            f.writelines(new_lines)
        subprocess.run(["udevadm", "control", "--reload-rules"], check=True)
        subprocess.run(["udevadm", "trigger"], check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/threats')
def get_threats():
    try:
        # جلب أحدث 100 هجوم للأرشيف
        threats = get_recent_threats(limit=100)
        return jsonify(threats)
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)