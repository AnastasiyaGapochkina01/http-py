import socket
import threading
import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import os

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "OK", "version": "1.0.0"}).encode('utf-8')
            self.wfile.write(response)

        elif path == '/main':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html = self.get_main_page().encode('utf-8')
            self.wfile.write(html)

        elif path == '/about':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html = self.get_about_page().encode('utf-8')
            self.wfile.write(html)

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def get_main_page(self):
        hostname = socket.gethostname()
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Добро пожаловать!</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{ background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }}
        h1 {{ color: #fff; text-align: center; }}
        .nav {{ text-align: center; margin: 20px 0; }}
        .nav a {{ color: #fff; margin: 0 15px; text-decoration: none; font-size: 18px; }}
        .nav a:hover {{ text-shadow: 0 0 10px #fff; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 Главная страница 🌟</h1>
        <div class="nav">
            <a href="/health">/health</a> |
            <a href="/main">/main</a> |
            <a href="/about">/about</a>
        </div>
        <p style="font-size: 20px; text-align: center;">
            <br>
            Сервер запущен на хосте: <strong>{hostname}</strong>
        </p>
    </div>
</body>
</html>
        """

    def get_about_page(self):
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
        except:
            ip = 'не удалось определить'

        try:
            load_avg = os.getloadavg()
        except:
            load_avg = 'недоступно'

        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>О сервере</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            max-width: 900px;
            margin: 50px auto;
            padding: 30px;
            background: #1a1a2e;
            color: #00ff88;
        }}
        .container {{
            background: #16213e;
            padding: 40px;
            border-radius: 10px;
            border-left: 5px solid #00ff88;
        }}
        h1 {{ color: #00ff88; margin-bottom: 30px; }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        .info-item {{
            background: rgba(0,255,136,0.1);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #00ff88;
        }}
        .nav {{ text-align: center; margin: 30px 0; }}
        .nav a {{
            color: #00ff88;
            margin: 0 20px;
            text-decoration: none;
            font-size: 16px;
            padding: 8px 15px;
            border: 1px solid #00ff88;
            border-radius: 5px;
        }}
        .nav a:hover {{ background: #00ff88; color: #1a1a2e; }}
        code {{ background: #0f3460; padding: 2px 6px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Информация о сервере</h1>
        <div class="nav">
            <a href="/health">/health</a> |
            <a href="/main">/main</a> |
            <a href="/about">/about</a>
        </div>

        <div class="info-grid">
            <div class="info-item">
                <strong>Hostname:</strong><br>
                <code>{hostname}</code>
            </div>
            <div class="info-item">
                <strong>IP адрес:</strong><br>
                <code>{ip}</code>
            </div>
            <div class="info-item">
                <strong>Python версия:</strong><br>
                <code>{self.server_version}</code>
            </div>
            <div class="info-item">
                <strong>Load Average:</strong><br>
                <code>{load_avg}</code>
            </div>
            <div class="info-item">
                <strong>Сервер:</strong><br>
                Python HTTP Server
            </div>
            <div class="info-item">
                <strong>Эндпоинты:</strong><br>
                /health, /main, /about
            </div>
        </div>

        <p style="text-align: center; font-size: 16px; margin-top: 30px;">
            Demo App on Python
        </p>
    </div>
</body>
</html>
        """

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f"🚀 Сервер запущен на http://0.0.0.0:{port}")
    print("Доступные эндпоинты:")
    print("  GET /health  -> JSON статус")
    print("  GET /main    -> Главная страница")
    print("  GET /about   -> Информация о сервере")
    print("\nCtrl+C для остановки")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server(8000)
