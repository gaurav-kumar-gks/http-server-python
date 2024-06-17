import re

from constants import (
    not_found_response,
)
from handlers import (
    RootHandler, 
    EchoHandler, 
    UserAgentHandler,
    FilesHandler,
)
from reqres import Request


class Router:
    def __init__(self):
        self.routes = {
            "^/$": RootHandler(),
            "^/echo/(.*)$": EchoHandler(),
            "^/user-agent$": UserAgentHandler(),
            "^/files/(.*)$": FilesHandler(),
        }

    def route(self, request: Request):
        for route, handler in self.routes.items():
            match = re.match(route, request.path)
            if match:
                method = getattr(handler, request.method.lower(), None)
                if method:
                    return method(request, *match.groups())
        return not_found_response
