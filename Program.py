from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import re

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(f"Received POST data: {post_data}")

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Request received')

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello World')

def get_port_from_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    port_line = next((line for line in lines if line.startswith('Port:')), None)
    if port_line is None:
        raise ValueError("Port information not found in the file.")
    
    # Extract the port number from the line
    match = re.search(r'localhost:(\d+)', port_line)
    if match:
        return int(match.group(1))
    
    raise ValueError("Port number not found in the port line.")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=None):
    if port is None:
        raise ValueError("Port must be provided.")
    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    ngrok_info_path = './ngrok_information.txt'
    port = get_port_from_file(ngrok_info_path)
    run(port=port)
