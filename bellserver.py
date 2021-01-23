#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import ringUtils

homepagePath = "/usr/local/bell-ringer/index.html"
hostName = "192.168.1.150"
serverPort = 80

class BellServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.handleHomepageRequest()
            return

        self.send_response(404)
           
    def do_POST(self):
        if self.path == "/ring":
            self.handleRingBellRequest();

    def handleHomepageRequest(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content = open(homepagePath, 'rb').read()
        self.wfile.write(content)

    def handleRingBellRequest(self):
        if ringUtils.ringOnce():
            self.send_response(200)
        else:
            self.send_response(429)
        self.send_header("Content-type", "text/html")
        self.end_headers()

def run_server():
    webServer = HTTPServer((hostName, serverPort), BellServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("  Server stopped.")

if __name__ == "__main__":        
    ringUtils.initialize()
    try:
        run_server()
    finally:
        ringUtils.cleanup()

