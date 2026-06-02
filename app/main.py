import socket  # noqa: F401
import threading


def parse_redis_type_protocol(decoded_data:str):
    if decoded_data[0] == '*':
        pass
    elif decoded_data:
        pass



def create_output_msg_redis_type_protoc(message:str):
    message_len = len(message)
    return f"+{message_len}\r\n{message}\r\n".encode()



def handle_client(connection:socket.socket) -> None:
    while True:
        data = connection.recv(1024)
        decoded_data = data.decode()
        if "*1\r\n$4\r\nPING\r\n" in decoded_data:
            connection.sendall(b"+PONG\r\n")
        elif decoded_data[0] == "*":
            message_ = decoded_data.split("\r\n")[-2]
            connection.send(f"${len(message_)}\r\n{message_}\r\n".encode())


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
