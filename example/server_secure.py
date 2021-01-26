import http.server
import ssl

server_address = ('localhost', 4443)


class S(http.server.BaseHTTPRequestHandler):

    def _set_headers(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):

        content = f"<html><body>{message}</body></html>"

        return content.encode("utf8")

    def do_GET(self):

        self._set_headers()
        self.wfile.write(self._html("Howdy Pardner"))

    def do_HEAD(self):

        self._set_headers()

    def do_POST(self):

        self._set_headers()
        self.wfile.write(self._html("POST!"))


httpd = http.server.HTTPServer(server_address, S)
httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               certfile='server.pem',
                               ssl_version=ssl.PROTOCOL_TLS)
httpd.serve_forever()
