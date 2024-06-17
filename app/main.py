import socket


def main():
    print("main --")
    with socket.create_server(("localhost", 4221), reuse_port=True) as server:
        while True:
            server_socket, addr = server.accept() # wait for client
            data = server_socket.recv(1024)
            print(f"Connected by {addr} received: {data}")
            if not data:
                break
            server_socket.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
            server_socket.close()
if __name__ == "__main__":
    main()
