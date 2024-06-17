import socket

from app.routers import Router


def main():
    print("Starting server...")
    try:
        with socket.create_server(("localhost", 4221), reuse_port=True) as server:
            print("Server started")
            while True:
                server_socket, addr = server.accept() # wait for client
                data = server_socket.recv(1024)
                print(f"Connected by {addr}")
                response = handle_request(data)
                server_socket.sendall(response)
                server_socket.close()
    except KeyboardInterrupt:
        print("\nClosing server...")
    except Exception as e:
        print(f"\nException: {e}")
        print("\nClosing server...")

def handle_request(data):
    router = Router()
    request_line = data.decode().split("\r\n")[0]
    path = request_line.split(" ")[1]
    method = request_line.split(" ")[0]
    request_data = data.decode().split("\r\n\r\n")[1]
    request_headers = {}
    headers = data.decode().split("\r\n")[1:-2]
    for header in headers:
        key, value = header.split(": ")
        request_headers[key] = value
        
    print(f"[request]: {method} {path} headers: {request_headers} data: {request_data}")
    response = router.route(method, path, request_headers, request_data)
    print(f"[response]: {response}")
    return response

if __name__ == "__main__":
    main()
