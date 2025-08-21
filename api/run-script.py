from http.server import BaseHTTPRequestHandler
import subprocess

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        
        try:
            # Execute the cyber.py script
            result = subprocess.run(
                ['python', 'cyber.py'],
                capture_output=True,
                text=True,
                check=True
            )
            self.wfile.write(b"Script executed successfully:\n")
            self.wfile.write(result.stdout.encode())
        except subprocess.CalledProcessError as e:
            self.wfile.write(b"Script execution failed:\n")
            self.wfile.write(e.stderr.encode())
        
        return
