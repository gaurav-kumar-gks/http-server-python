from constants import (
    method_not_allowed_response, 
    ok_response,
)
from reqres import Request


class BaseHandler:
    def get(self, request: Request, *path_params):
        return method_not_allowed_response

    def post(self, request: Request, *path_params):
        return method_not_allowed_response
    
class RootHandler(BaseHandler):
    def get(self, request: Request, *path_params):
        return ok_response

class EchoHandler(BaseHandler):
    def get(self, request: Request, *path_params):
        echo_name = path_params[0]
        len_data = len(echo_name)
        return f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len_data}\r\n\r\n{echo_name}'.encode()

class UserAgentHandler(BaseHandler):
    def get(self, request: Request, *path_params):
        user_agent = request.headers.get("User-Agent", "Unknown")
        len_data = len(user_agent)
        return f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len_data}\r\n\r\n{user_agent}'.encode()

class FilesHandler(BaseHandler):
    def get(self, request: Request, *path_params):
        file_dir = "/tmp/"
        file_name = path_params[0]
        try:
            print(f"File name: {file_name} and local_file_dir: {file_dir}")
            with open(f'{file_dir}{file_name}', 'r') as file:
                data = file.read()
                len_data = len(data)
                return f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len_data}\r\n\r\n{str(data)}'.encode()
        except FileNotFoundError:
            return b'HTTP/1.1 404 Not Found\r\n\r\n'
        except Exception as e:
            return f'HTTP/1.1 500 Internal Server Error\r\n\r\n{e}'.encode()
      
    def post(self, request: Request, *path_params):
        file_dir = "/tmp/"
        file_name = path_params[0]
        try:
            with open(f'{file_dir}{file_name}', 'w') as file:
                file.write(request.data)
                return b'HTTP/1.1 201 Created\r\n\r\n'
        except Exception as e:
            return f'HTTP/1.1 500 Internal Server Error\r\n\r\n{e}'.encode()
        