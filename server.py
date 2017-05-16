#!/usr/bin/env python
import json
import redis
import uuid
import os
from pprint import pprint
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from rq import Worker, Queue, Connection
from searcher import search
from worker import redistogo_conn

queue = Queue(connection=redistogo_conn)
redis_conn = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/1"))

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        request_path = self.path
        print(request_path)
        val = redis_conn.get(request_path[1:])
        if val is None:
            self.send_response(404)
        else:
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(val)

    def do_POST(self):
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        json_content = json.loads(self.rfile.read(length))
        request_id = uuid.uuid4().hex
        if("query" not in json_content or "urls" not in json_content):
            self.send_error(400,"JSON object has no query or urls")
        else:
            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(request_id)
            queue.enqueue(search, request_id, json_content[query], json_content[urls])

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*');
        self.send_header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Content-Length, X-Requested-With');

    def send_error(self, code, message=None):
        self.log_error("code %d, message %s", code, message)
        self.send_response(code, message)
        self.send_cors_headers()
        self.send_header("Content-Type", 'application/json')
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write('{"error": "%d %s"}' % (code,message))

    do_PUT = do_POST
    do_DELETE = do_GET

def main():
    port = int(os.environ.get('PORT', 8080))
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
