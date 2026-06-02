import socket  # noqa: F401
import threading


def handle_client(connection:socket.socket) -> None:
    while True:
        data = connection.recv(1024)
        # print("Recieved:", data.decode())
        connection.sendall(b"+PONG\r\n")

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment the code below to pass the first stage
    #
    with socket.create_server(("localhost", 6379), reuse_port=True) as server_socket:
        while True:
            connection_, _ = server_socket.accept()  # wait for client
            print("New Connection Created")
            threading.Thread(target=handle_client, args=(connection_,)).start()


if __name__ == "__main__":
    main()
