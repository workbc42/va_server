from http.server import HTTPServer, BaseHTTPRequestHandler
class MyVanillaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        response_message = "<h1>안녕 나의 바닐라 서버야 ~!</h1>"
        self.wfile.write(response_message.encode('utf-8'))

port = 8000
server_address = ('localhost', port)
print(f"서버 준비 http://{server_address[0]}:{server_address[1]}")
httpd = HTTPServer(server_address, MyVanillaHandler)
httpd.serve_forever()

