import socket



with socket.create_server(("localhost", 8080), reuse_port=True) as server_socket:
    while True:
        # Blaock untill we receive an incoming req
        connection, address = server_socket.accept()
        print(f"accepted connection from {address}")

        # Read data
        data = connection.recv(1024)
        print("received data:", data)
        # Write the same data back
        connection.sendall(data)