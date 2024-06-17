import socket
import threading

from app.reqres import Request
from app.routers import Router


def start_server_and_server_requests():
    print("Starting server...")
    try:
        with socket.create_server(("localhost", 4221), reuse_port=True) as server:
            print("Server started")
            while True:
                server_socket, addr = server.accept() # accept the connection
                threading.Thread(target=handle_request, args=(server_socket, addr)).start() # handle the request
    except KeyboardInterrupt:
        print("\nClosing server...")
    except Exception as e:
        print(f"\nException: {e}")
        print("\nClosing server...")

def handle_request(server_socket, addr):
    data = server_socket.recv(1024)
    print(f"Connected by {addr}")
    if data == b"":
        server_socket.close()
        return
    router = Router()
    request = Request(data)
    print(f"[request]: {str(request.__dict__)}")
    response = router.route(request)
    print(f"[response]: {response}")
    server_socket.sendall(response)
    server_socket.close()
    return response

if __name__ == "__main__":
    start_server_and_server_requests()
