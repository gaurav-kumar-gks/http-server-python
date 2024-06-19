import re

from handlers import (
    RootHandler, 
    EchoHandler, 
    UserAgentHandler,
    FilesHandler,
)
from reqres import Request


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, route, handler):
        """adds the route and handler to the routes dictionary
        """
        self.routes[route] = handler
        
    def route(self, request: Request):
        for route, handler in self.routes.items():
            match = re.match(route, request.path)
            if match:
                method = getattr(handler, request.method.lower(), None)
                if method:
                    return method(request, *match.groups())
        return None
