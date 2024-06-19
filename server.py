import datetime
import io
import os
import socket
import sys
    
class WSGIServer:
    
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    
    def __init__(self, init_config: dict):
        self.init_config = init_config
        self._set_socket()
        self._set_server_config()
    
    def _set_socket(self):        
        addr_tuple = (
            self.init_config.get("host", "localhost"), 
            int(self.init_config.get("port", "4221"))
        )
        server_socket = socket.socket(self.address_family, self.socket_type)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(addr_tuple)
        server_socket.listen(self.init_config.get("request_backlog", 1))
        self.server_socket = server_socket  
    
    def _set_server_config(self):
        host, port = self.server_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.server_host = host
        self.server_config = {
            "server_name": self.server_name,
            "server_port": self.server_port,
            "server_host": host,
            "app": self.init_config.get("app"),
            "server_version": "1.0",
            "server_software": "WSGIServer 0.2",
        }
    
    def set_app(self, app):
        self.app = app
    
    def serve_forever(self):
        print(f"WSGIServer: Serving HTTP on {self.server_host}:{self.server_port}")
        while True:
            conn, addr = self.server_socket.accept()
            request_handler = RequestHandler(self.server_config, conn)
            import threading
            thread = threading.Thread(
                target=request_handler.handle_request,
                args=(conn, addr)
            ).start()
        

class RequestHandler:
    
    def __init__(self, server_config, conn):
        self.server_config = server_config
        self.conn = conn
        self.set_environ()
    
    def handle_request(self):
        self.parse_request()
        result = self.server_config.get("app")(self.environ, self.start_response)
        self.finish_response(result)

    def parse_request(self):
        self.request_data = self.conn.recv(1024).decode("utf-8")
        request_line = self.request_data.splitlines()[0].rstrip("\r\n")
        (self.request_method, self.path, self.request_version) = request_line.split()
        print(f"Request Method: {self.request_method} Path: {self.path} Request Data: {self.request_data}")
    
    def set_environ(self):
        os_env = {k: v for k, v in os.environ.items()}
        environ = {
            "wsgi.version": (1, 0),
            "wsgi.input": io.StringIO(self.request_data),
            "wsgi.errors": sys.stderr,
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
            "REQUEST_METHOD": self.request_method,
            "PATH_INFO": self.path,
            "SERVER_NAME": self.server_config.get("server_name"),
            "SERVER_PORT": str(self.server_config.get("server_port")),
        }
        environ["wsgi.url_scheme"] = "http" if os_env.get("HTTPS", "off") in ["off", "0"] else "https",
        environ.update(os_env)
        self.environ = environ
    
    def start_response(self, status, response_headers):
        server_headers = [
            ("Date", datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")),
            ("Server", self.server_config.get("server_software")),
        ]
        self.headers_set = [status, response_headers + server_headers]
        return self.finish_response
    
    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = f"HTTP/1.1 {status}\r\n"
            for header in response_headers:
                response += f"{header[0]}: {header[1]}\r\n"
            response += "\r\n"
            for data in result:
                response += data.decode("utf-8")
            self.response = response
            print(f"Response: {response}")
            self.conn.sendall(response.encode())
        finally:
            self.conn.close()