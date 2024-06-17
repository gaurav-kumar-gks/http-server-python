import re
import socket

import socket

not_found_response = b'HTTP/1.1 404 Not Found\r\n\r\n'
method_not_allowed_response = b'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
ok_response = b'HTTP/1.1 200 OK\r\n\r\n'

class BaseHandler:
    def get(self, request_target, request_data, *request_params):
        return method_not_allowed_response

    def post(self, request_target, request_data, *request_params):
        return method_not_allowed_response


class RootHandler(BaseHandler):
    def get(self, request_target, request_data, *request_params):
        return ok_response

class EchoHandler(BaseHandler):
    def get(self, request_target, request_data, *request_params):
        echo_name = request_params[0]
        len_data = len(echo_name)
        response_body = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len_data}\r\n\r\n{echo_name}'.encode()
        return response_body

class Router:
    def __init__(self):
        self.routes = {
            "^/$": RootHandler(),
            "^/echo/(.*)$": EchoHandler(),
        }

    def route(self, request_method, request_target, request_data):
        for route, handler in self.routes.items():
            match = re.match(route, request_target)
            if match:
                params = match.groups()
                route_handler = getattr(handler, request_method.lower(), None)
                if route_handler is None:
                    return method_not_allowed_response
                return route_handler(request_target, request_data, *params)
        return not_found_response


def main():
    print("Starting server...")
    try:
        with socket.create_server(("localhost", 4221), reuse_port=True) as server:
            print("Server started")
            while True:
                server_socket, addr = server.accept() # wait for client
                data = server_socket.recv(1024)
                print(f"Connected by {addr} received: {data}")
                response_body = handle_request(data)
                server_socket.sendall(response_body)
                server_socket.close()
    except KeyboardInterrupt:
        print("\nClosing server...")
    except Exception as e:
        print(f"\nException: {e}")
        print("\nClosing server...")

def handle_request(data):
    router = Router()
    request_line = data.decode().split("\r\n")[0]
    request_target = request_line.split(" ")[1]
    request_method = request_line.split(" ")[0]
    request_data = data.decode().split("\r\n\r\n")[1]
    print(f"Request Method: {request_method} Request target: {request_target} request_data: {request_data}")

    response_body = router.route(request_method, request_target, request_data)
    return response_body

if __name__ == "__main__":
    main()
