from app.constants import (
    method_not_allowed_response, 
    ok_response,
)

class BaseHandler:
    def get(self, path,  headers, data, *path_params):
        return method_not_allowed_response

    def post(self, path,  headers, data, *path_params):
        return method_not_allowed_response

class RootHandler(BaseHandler):
    def get(self, path,  headers, data, *path_params):
        return ok_response

class EchoHandler(BaseHandler):
    def get(self, path,  headers, data, *path_params):
        echo_name = path_params[0]
        len_data = len(echo_name)
        return f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len_data}\r\n\r\n{echo_name}'.encode()

class UserAgentHandler(BaseHandler):
    def get(self, path,  headers, data, *path_params):
        user_agent = headers.get("User-Agent", "Unknown")
        len_data = len(user_agent)
        return f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len_data}\r\n\r\n{user_agent}'.encode()

