import socket

not_found_response = b'HTTP/1.1 404 Not Found\r\n\r\n'
ok_response = b'HTTP/1.1 200 OK\r\n\r\n'

def handle_request(data):
    request_line = data.decode().split("\r\n")[0]
    request_target = request_line.split(" ")[1]
    request_method = request_line.split(" ")[0]
    request_data = data.decode().split("\r\n\r\n")[1]
    print(f"Request Method: {request_method} Request target: {request_target} request_data: {request_data}")
    response_body = not_found_response
    
    if request_target == "/":
        response_body = root_handler(request_method, request_data)
    elif request_target.startswith("/echo/"):
        response_body = echo_handler(request_method, request_data)
    return response_body

def echo_handler(request_method, request_data):
    len_data = len(request_data)
    response_body = f'HTTP/1.1 200 OK\r\nContent-Length: {len_data}\r\n\r\n{request_data.decode()}'.encode()
    return response_body

def root_handler(request_method, request_data):
    return ok_response


handlers = {
    "/": root_handler,
    "/echo/": echo_handler
}

def main():
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
    except:
        print("Closing server...")
        pass
if __name__ == "__main__":
    main()
