#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
import threading
import socket
import time

TELLO_IP = "192.168.10.1"
TELLO_COMMAND_PORT = 8889
TELLO_COMMAND_ADDRESS = (TELLO_IP, TELLO_COMMAND_PORT)

UDP_SOCKET = socket.socket(socket.AF_INET,    # Internet
                           socket.SOCK_DGRAM) # UDP




# Send a command to the drone via the UDP socket
def send_to_tello(command: str):
    UDP_SOCKET.sendto(command.encode(), TELLO_COMMAND_ADDRESS)


# Send periodically a drone command to keep connection alive
def keep_alive():
    while True:
        print("Sending keep alive")
        send_to_tello("command")
        time.sleep(10)


is_keep_alive_running = False

# The HTTP handler
class Handler(SimpleHTTPRequestHandler):

    def do_GET(self) -> None:
        global is_keep_alive_running
        path = self.path

        if path == "/":
            self.send_response(HTTPStatus.MOVED_PERMANENTLY)
            self.send_header("Location", "/drone-pilot.html")
            self.end_headers()
        elif path.endswith((".html", ".htm", ".js")):
            super().do_GET()
        elif path.startswith("/drone"):
            params = parse_qs(urlparse(path).query, max_num_fields=1)
            command = params['command'][0] if 'command' in params else ""
            self.send_response(HTTPStatus.OK)
            self.end_headers()

            if command: # Send command to tello drone if not empty
                if command == "takeoff" and not is_keep_alive_running:
                    is_keep_alive_running = True
                    print("Starting keep alive daemon")
                    threading.Thread(
                        target=keep_alive, daemon=True).start()
                    

                send_to_tello(command)
        elif path.startswith("/events"):
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/event-stream")
            self.end_headers()

            # Send a message to the client.
            self.wfile.write(b"data: Hello, world!\n\n")

            # Keep the connection open.
            while True:
                time.sleep(1)
                self.wfile.write((f"data: {time.time()} This is a message from the server.\n\n").encode())


        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Resource not found")



HTTP_SERVER_PORT = 8000

try:
    with HTTPServer(("", HTTP_SERVER_PORT), Handler) as httpd:
        print("Drone HTTP server listening at port", HTTP_SERVER_PORT)
        httpd.serve_forever()
finally:
    print("Closing UDP_SOCKET")
    UDP_SOCKET.close()