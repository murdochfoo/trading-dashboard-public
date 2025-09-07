#!/usr/bin/env python3
"""
Development Server for Trading Dashboard
Serves files locally with CORS enabled for development
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Add timestamp and better formatting
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def start_dev_server(port=8000):
    """Start development server on specified port"""
    os.chdir('/home/ib/trading-dashboard-dev')
    
    with socketserver.TCPServer(("", port), CORSHTTPRequestHandler) as httpd:
        print(f"""
🚀 TRADING DASHBOARD DEVELOPMENT SERVER
=======================================
📍 Server running at: http://localhost:{port}
📁 Serving from: {os.getcwd()}
🔄 Auto-refresh: Enabled (no cache)
🌐 CORS: Enabled for all origins

📋 Development Commands:
  - Ctrl+C to stop server
  - Open http://localhost:{port} in browser
  - Edit files and refresh to see changes

⚠️  This is DEVELOPMENT ONLY - never use in production!
=======================================
""")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Development server stopped")
            sys.exit(0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Start Trading Dashboard Development Server')
    parser.add_argument('--port', type=int, default=8000, help='Port to serve on (default: 8000)')
    args = parser.parse_args()
    
    start_dev_server(args.port)