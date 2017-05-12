#!/usr/bin/env python
import json
import requests
from pprint import pprint
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        # self.send_header("Set-Cookie", "foo=bar")

    def do_POST(self):

        request_path = self.path

        print("\n----- Request Start ----->\n")
        print(request_path)

        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        raw_content = self.rfile.read(length)
        json_content = json.loads(raw_content)

        print(request_headers)
        print("\n----- Raw Content -----\n")
        print(raw_content)
        print("\n----- JSON Content -----\n")
        pprint(json_content)
        print("\n----- Query -----\n")
        search_query = json_content.get('query')
        print(search_query)
        result_urls = []
        print("<----- Request End -----\n")
        for url in json_content.get('urls'):
            r = requests.get(url)
            if search_query in r.text:
                result_urls.append  (url)
        response_dict = {"original_query": search_query,
                    "found_urls":result_urls}
        response_string = json.dumps(response_dict)
        print("<----- Response -----\n")
        pprint(response_dict)
        print(response_string)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(response_string)

    do_PUT = do_POST
    do_DELETE = do_GET

def main():
    port = 80
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
