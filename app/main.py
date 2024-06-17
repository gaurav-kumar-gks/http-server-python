import socket


not_found_response = b'HTTP/1.1 404 Not Found\r\n\r\n'
ok_response = b'HTTP/1.1 200 OK\r\n\r\n'

def main():
    try:
        with socket.create_server(("localhost", 4221), reuse_port=True) as server:
            print("Server started")
            while True:
                server_socket, addr = server.accept() # wait for client
                data = server_socket.recv(1024)
                print(f"Connected by {addr} received: {data}")
                if not data:
                    break
                
                # get the request target from the first line
                request_line = data.decode().split("\r\n")[0]
                request_target = request_line.split(" ")[1]
                request_method = request_line.split(" ")[0]
                print(f"Request Method: {request_method} Request target: {request_target}")
                
                response_body = not_found_response
                if request_target == "/":
                    response_body = ok_response
                server_socket.sendall(response_body)
                server_socket.close()
    except:
        print("Closing server...")
        pass
if __name__ == "__main__":
    main()
