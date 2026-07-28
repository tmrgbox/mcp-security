from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import json
import threading

mcp_process = None
mcp_lock = threading.Lock()

class MCPBridgeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global mcp_process
        if self.path == '/rpc':
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                request = json.loads(body.decode())
                
                with mcp_lock:
                    if mcp_process is None or mcp_process.poll() is not None:
                        mcp_process = subprocess.Popen(
                            ["python", "tool-poisoning.py"],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                    
                    mcp_process.stdin.write(json.dumps(request) + "\n")
                    mcp_process.stdin.flush()
                    response_line = mcp_process.stdout.readline()
                    response = json.loads(response_line) if response_line else {}
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logs

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), MCPBridgeHandler)
    print("MCP HTTP Bridge listening on port 8000")
    server.serve_forever()
