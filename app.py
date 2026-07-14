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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEXUS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            height: 100%;
            width: 100%;
            background: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container { max-width: 400px; width: 100%; text-align: center; }
        .icon { font-size: 60px; margin-bottom: 10px; }
        h1 { font-size: 40px; font-weight: 700; color: #111; margin-bottom: 6px; }
        .sub { font-size: 16px; color: #666; margin-bottom: 30px; }
        input {
            width: 100%;
            padding: 16px 14px;
            margin: 8px 0;
            background: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 12px;
            font-size: 18px;
            color: #111;
        }
        input:focus { outline: none; border-color: #007aff; background: #fff; }
        button {
            width: 100%;
            padding: 16px;
            background: #007aff;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 20px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 12px;
        }
        button:hover { background: #0066d9; }
        .footer { margin-top: 25px; font-size: 14px; color: #999; }
        .footer span { color: #111; font-weight: 500; }
        .warning {
            font-size: 14px;
            color: #e74c3c;
            font-weight: 500;
            margin-bottom: 20px;
            background: #fef0ef;
            padding: 10px 14px;
            border-radius: 10px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">🧸</div>
        <h1>NEXUS</h1>
        <p class="sub">Learn cybersecurity by doing</p>
        <div class="warning">⚠️ Training mode — use fake data</div>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Your Name" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
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
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            height: 100%;
            background: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container { max-width: 400px; width: 100%; text-align: center; }
        h1 { font-size: 40px; color: #111; margin-bottom: 6px; }
        .icon { font-size: 60px; }
        .msg { font-size: 18px; color: #333; margin: 20px 0; }
        .sub { font-size: 16px; color: #666; }
        a {
            display: inline-block;
            margin-top: 25px;
            color: #007aff;
            text-decoration: none;
            font-size: 18px;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">🧸</div>
        <h1>NEXUS</h1>
        <p class="msg">⚠️ This is a training honeypot.</p>
        <p class="sub">Your data has been recorded.</p>
        <a href="/">← Go back</a>
    </div>
</body>
</html>
    """

@app.route('/dashboard')
def dashboard():
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NEXUS Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: #ffffff;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                padding: 20px;
                max-width: 700px;
                margin: 0 auto;
            }
            h1 { font-size: 32px; color: #111; margin-bottom: 8px; }
            .back { color: #007aff; text-decoration: none; font-size: 16px; }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                font-size: 14px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px 8px;
                text-align: left;
            }
            th { background: #f5f5f5; color: #111; font-weight: 600; }
            tr:nth-child(even) { background: #fafafa; }
            .total { color: #666; margin-top: 20px; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>📊 NEXUS Dashboard</h1>
        <p><a href="/" class="back">← Go back</a></p>
        <table>
            <tr><th>Time</th><th>Name</th><th>Password</th><th>IP</th></tr>
    """
    
    for log in logs[-20:]:
        html += f"<tr><td>{log['timestamp']}</td><td>{log['username']}</td><td>{log['password']}</td><td>{log['ip']}</td></tr>"
    
    html += f"""
        </table>
        <p class="total">Total attempts: {len(logs)}</p>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
