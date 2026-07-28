from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import io
import contextlib

# Import the MCP server module
try:
    from tool_poisoning import mcp
except ImportError:
    print("Error: Could not import tool_poisoning module. Ensure mcp and FastMCP are installed.")
    sys.exit(1)

class MCPBridgeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/rpc':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                request = json.loads(body.decode())
                
                # Capture stdout from MCP server execution
                captured_output = io.StringIO()
                try:
                    with contextlib.redirect_stdout(captured_output):
                        # Send request to MCP server (simplified)
                        # For now, just echo back the request as a placeholder
                        response = {
                            "jsonrpc": "2.0",
                            "id": request.get("id"),
                            "result": {"message": "MCP server received your request"}
                        }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {"code": -1, "message": str(e)}
                    }
                
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
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
        sys.exit(0)
