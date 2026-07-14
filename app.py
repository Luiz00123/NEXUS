#!/usr/bin/env python3
from flask import Flask, request
import json
import os
import datetime

app = Flask(__name__)
LOG_FILE = "captures.json"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS - Training</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            height: 100%;
            background: #0a0a1a;
            font-family: 'Segoe UI', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 15px;
        }
        .container {
            background: #1a1a2e;
            padding: 50px 40px;
            border-radius: 40px;
            box-shadow: 0 0 100px #00ffcc44;
            max-width: 600px;
            width: 100%;
            text-align: center;
            border: 3px solid #00ffcc;
        }
        .warning {
            background: #ff4444;
            color: white;
            padding: 16px 14px;
            border-radius: 20px;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        h1 { color: #00ffcc; font-size: 56px; letter-spacing: 4px; margin: 10px 0 8px 0; }
        .sub { color: #aaa; font-size: 22px; margin-bottom: 30px; }
        input {
            width: 100%;
            padding: 18px 16px;
            margin: 12px 0;
            background: #0f0f2a;
            border: 2px solid #2a2a4a;
            border-radius: 20px;
            color: white;
            font-size: 22px;
        }
        input:focus { outline: none; border-color: #00ffcc; box-shadow: 0 0 20px #00ffcc55; }
        button {
            width: 100%;
            padding: 18px;
            background: #00ffcc;
            color: #0a0a1a;
            border: none;
            border-radius: 20px;
            font-size: 26px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 18px;
        }
        button:hover { background: #00dbb8; }
        .footer { color: #555; margin-top: 30px; font-size: 18px; }
        .footer span { color: #00ffcc; }
        .nexus-icon { font-size: 72px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">🧪 TRAINING MODE - DO NOT ENTER REAL PASSWORDS!</div>
        <div class="nexus-icon">🧸</div>
        <h1>NEXUS</h1>
        <p class="sub">Learn cybersecurity by doing</p>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Your Name" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">🚀 Login</button>
        </form>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸 | <span>"Learn. Understand. Protect."</span></p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = request.remote_addr
    
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    logs.append({
        "timestamp": str(datetime.datetime.now()),
        "username": username,
        "password": password,
        "ip": ip
    })
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    
    return """
    <html>
    <head>
        <title>NEXUS</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            html, body {
                height: 100%;
                background: #0a0a1a;
                font-family: 'Segoe UI', Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: #1a1a2e;
                padding: 50px 40px;
                border-radius: 40px;
                box-shadow: 0 0 100px #ff444444;
                max-width: 600px;
                width: 100%;
                text-align: center;
                border: 3px solid #ff4444;
            }
            h1 { color: #00ffcc; font-size: 56px; }
            h2 { color: #ff4444; font-size: 32px; margin: 20px 0; }
            p { color: #ccc; font-size: 22px; margin: 20px 0; }
            a {
                color: #00ffcc;
                font-size: 24px;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
                padding: 12px 30px;
                border: 2px solid #00ffcc;
                border-radius: 30px;
            }
            a:hover { background: #00ffcc22; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧸 NEXUS</h1>
            <h2>⚠️ THIS IS A TRAINING HONEYPOT! ⚠️</h2>
            <p>Your data has been recorded for educational purposes.</p>
            <a href="/">🔙 Go Back</a>
        </div>
    </body>
    </html>
    """

@app.route('/dashboard')
def dashboard():
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    
    html = """
    <html>
    <head>
        <title>NEXUS Dashboard</title>
        <style>
            body { background: #0a0a1a; color: #00ffcc; font-family: monospace; padding: 20px; }
            table { width: 100%%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #00ffcc; padding: 10px; text-align: left; }
            th { background: #1a1a2e; color: #fff; }
            tr:hover { background: #1a1a2e; }
            .back { color: #00ffcc; text-decoration: none; font-size: 18px; }
        </style>
    </head>
    <body>
        <h1>📊 NEXUS Dashboard</h1>
        <p><a href="/" class="back">← Go Back</a></p>
        <table>
            <tr><th>Time</th><th>Name</th><th>Password</th><th>IP</th></tr>
    """
    
    for log in logs[-20:]:
        html += f"<tr><td>{log['timestamp']}</td><td>{log['username']}</td><td>{log['password']}</td><td>{log['ip']}</td></tr>"
    
    html += f"""
        </table>
        <p style="color: #555;">Total attempts: {len(logs)}</p>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
