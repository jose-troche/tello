from http.server import SimpleHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
import socket

TELLO_IP = "192.168.10.1"
TELLO_COMMAND_PORT = 8889
TELLO_COMMAND_ADDRESS = (TELLO_IP, TELLO_COMMAND_PORT)

# UDP_SOCKET = socket.socket(socket.AF_INET,    # Internet
#                            socket.SOCK_DGRAM) # UDP

global UDP_SOCKET

def send_to_tello(command: str):
    UDP_SOCKET.sendto(command.encode(), TELLO_COMMAND_ADDRESS)


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        path = self.path

        if path == "/":
            self.send_response(HTTPStatus.MOVED_PERMANENTLY)
            self.send_header("Location", "/drone-controller.html")
            self.end_headers()
        elif path.endswith((".html", ".htm", ".js")):
            super().do_GET()
        elif path.startswith("/drone"):
            params = parse_qs(urlparse(path).query, max_num_fields=1)
            command = params['command'][0] if 'command' in params else ""
            self.send_response(HTTPStatus.OK)
            self.end_headers()

            if command: # Send command to tello drone if not empty
                if command == "takeoff":
                    send_to_tello("command")
                send_to_tello(command)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Resource not found")


HTTP_SERVER_PORT = 8000

with HTTPServer(("", HTTP_SERVER_PORT), Handler) as httpd, socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket:
    UDP_SOCKET = socket
    print("Drone HTTP server listening at port", HTTP_SERVER_PORT)
    httpd.serve_forever()