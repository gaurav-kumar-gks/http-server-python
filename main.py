import socket
import threading

from reqres import Request
from routers import Router

local_file_dir = ""
HOST, PORT = "localhost", 4221

def start_server_and_server_requests(config: dict|None = None):
    """
        server must perform - socket(), bind(), listen(), accept()
        client must perform - socket(), connect()
    
    """
    if config is None:
        config = {}
    print("Starting server...")
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        
        while True:
            conn, addr = server_socket.accept() # accept the connection
            threading.Thread(target=handle_request, args=(conn, addr, config)).start() # handle the request
    except KeyboardInterrupt:
        print("\nClosing server...")
    except Exception as e:
        print(f"\nException: {e}")
        print("\nClosing server...")

def handle_request(conn, addr, config: dict):
    data = conn.recv(1024)
    print(f"Connected by {addr}")
    if data == b"":
        conn.close()
        return
    router = Router()
    request = Request(data, config)
    print(f"[request]: {str(request.__dict__)}")
    response = router.route(request)
    print(f"[response]: {response}")
    conn.sendall(response)
    conn.close()
    return response

if __name__ == "__main__":
    start_server_and_server_requests()
