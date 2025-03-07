from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
      if self.path == '/now-engine':
        content_length = int(self.headers.get('Content-Length', 0))
        content_type = self.headers.get('Content-Type', '')
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'message': f'success'}
        self.wfile.write(json.dumps(response).encode())
      else:
        return self.send_response(404)


def run_server():
  server = HTTPServer(('127.0.0.1', 8080), RequestHandler)
  print("Server running on http://127.0.0.1:8080")
  server.serve_forever()

if __name__ == "__main__":
  run_server()