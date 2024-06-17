import re

from app.constants import (
    method_not_allowed_response, 
    not_found_response,
)
from app.handlers import (
    RootHandler, 
    EchoHandler, 
    UserAgentHandler,
)


class Router:
    def __init__(self):
        self.routes = {
            "^/$": RootHandler(),
            "^/echo/(.*)$": EchoHandler(),
            "^/user-agent$": UserAgentHandler(),
        }

    def route(self, method, path, headers, data):
        for route, handler in self.routes.items():
            match = re.match(route, path)
            if match:
                path_params = match.groups()
                route_handler = getattr(handler, method.lower(), None)
                if route_handler is None:
                    return method_not_allowed_response
                return route_handler(path, headers, data, *path_params)
        return not_found_response
