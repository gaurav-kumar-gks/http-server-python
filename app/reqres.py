class Request:
    def __init__(self, data):
        lines = data.decode().split("\r\n")
        self.method, path, _ = lines[0].split(" ")
        self.data = data.decode().split("\r\n\r\n")[1]
        self.headers = {}
        path_split = path.split("?")
        self.path = path_split[0]
        self.query = {}
        if len(path_split) > 1 and path_split[1]:
            self.query = dict([part.split("=") for part in path_split[1].split("&")])
        for header in lines[1:-2]:
            key, value = header.split(": ")
            self.headers[key] = value
            