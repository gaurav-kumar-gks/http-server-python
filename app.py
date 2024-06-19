import re
from routers import Router

"""
def simple_app(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/plain")]
    start_response(status, headers)
    return [b"Hello World!"]
"""


class WsgiApp:
    
    def __init__(self):
        pass
    
    def __call__(self, environ, start_response):
        pass

    def set_routes(self, routes: dict):
        self.routes = Router()
        for path, handler in routes:
            self.routes.add_route(path, handler)    
    

app = WsgiApp()
