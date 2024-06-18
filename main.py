import sys

from server import WSGIServer

def get_server(module, app):
    app = getattr(__import__(module), app)
    server = WSGIServer({
        "host": "localhost", 
        "port": 4221, 
        "request_backlog": 10
    })
    server.set_app(app)
    return server

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("need to provide wsgi app object e.g. 'main:app'")
    module, app = sys.argv[1].split(":")
    server = get_server(module, app)
    server.serve_forever()
