from app import app
from handlers import RootHandler, EchoHandler, UserAgentHandler, FilesHandler

routes = {
    "^/$": RootHandler(),
    "^/echo/(.*)$": EchoHandler(),
    "^/user-agent$": UserAgentHandler(),
    "^/files/(.*)$": FilesHandler(),
}

app.set_routes(routes)
