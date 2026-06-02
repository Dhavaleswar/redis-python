import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment the code below to pass the first stage
    #
    with socket.create_server(("localhost", 6379), reuse_port=True) as server_socket:
        while True:
            connection_, _ = server_socket.accept()  # wait for client
            data = connection_.recv(1024)
            if not data:
                break
            connection_.sendall(b"+PONG\r\n")

if __name__ == "__main__":
    main()
