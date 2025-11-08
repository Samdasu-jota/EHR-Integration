"""
Simple HTTP server to host JWK Set for testing
This is for development/testing only - use a proper web server for production!
"""

import http.server
import socketserver
import json
import os

PORT = 8000

class JWKHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/jwks.json' or self.path == '/.well-known/jwks.json':
            # Try to serve jwks.json
            if os.path.exists('jwks.json'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open('jwks.json', 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'JWK Set file not found. Run create_jwks.py first.')
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <head><title>JWK Set Server</title></head>
            <body>
                <h1>JWK Set Server</h1>
                <p>This server hosts your JWK Set for Epic FHIR authentication.</p>
                <p><a href="/jwks.json">View JWK Set</a></p>
                <p><strong>For testing:</strong> Use ngrok or similar to expose this server:</p>
                <pre>ngrok http 8000</pre>
                <p>Then use the ngrok URL in Epic app settings.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

if __name__ == "__main__":
    if not os.path.exists('jwks.json'):
        print("⚠️  WARNING: jwks.json not found!")
        print("Run 'python3 create_jwks.py' first to create the JWK Set file.")
        exit(1)
    
    with socketserver.TCPServer(("", PORT), JWKHandler) as httpd:
        print(f"JWK Set server running on http://localhost:{PORT}")
        print(f"JWK Set available at: http://localhost:{PORT}/jwks.json")
        print(f"\nFor Epic, you need a publicly accessible URL.")
        print(f"Options:")
        print(f"  1. Use ngrok: ngrok http {PORT}")
        print(f"  2. Deploy to a web server")
        print(f"\nPress Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

