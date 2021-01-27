#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import ringUtils
import logging

homepagePath = "/usr/local/bell-ringer/index.html"
hostName = "192.168.1.150"
serverPort = 80
logging.basicConfig(filename='/var/log/bell.log', format=' %(message)s %(asctime)s', datefmt='%I:%M:%S %p %m/%d/%Y', level=logging.DEBUG)

class BellServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.handleHomepageRequest()
            return

        self.send_response(404)
           
    def do_POST(self):   # This is where you land when pressing the "RING THAT BELL" button on web page.
        if self.path == "/ring":
            logging.info("Web Ring Request from %s at  ", self.client_address[0])
            print(" Client Address=", self.client_address[0])
            self.handleRingBellRequest();

    def handleHomepageRequest(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content = open(homepagePath, 'rb').read()
        self.wfile.write(content)

    def handleRingBellRequest(self):
        if ringUtils.ringOnce():
            logging.info('    Bell went BONG to honor Web Request ')
            self.send_response(200)
        else:
            self.send_response(429)
        self.send_header("Content-type", "text/html")
        self.end_headers()

def run_server():
    webServer = HTTPServer((hostName, serverPort), BellServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    logging.info('Server Started..........................')

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

