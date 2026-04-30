import socket
import threading
import sys

def handle_client(client_socket, addr):
    print(f"New client connected from {addr}")

    try:
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Client says: {message}")

        command, key, value = process_message(message)
        print(f"Reveived command from Client = {command}, key={key}, value={value}")
        # response = response_message(command)
        client_socket.sendall(response.encode('utf-8'))

    finally:
        client_socket.close()
        print(f"Connection with {addr} closed.")

def start_server():
    host = 'localhost'
    port = 51234
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server is running and ready to accept multiple client.")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, addr),
                daemon=True
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("Shutting down server.")
    
    finally:
        server_socket.close()

# def response_message(message):
#     if message[0] == "R":
#         123
#         return 123

#     elif message[0] == "G":
#         123
#         return 123

#     elif message[1] == "P":
#         123
#         return 123
#     else:
#         return "Error"

def process_message(message):
    body = message[4:]

    command = body[0]

    if message[0] == "R":
        key = body[2:]
        return command, key, None

    elif message[0] == "G":
        key = body[2:]
        return command, key, None

    elif message[0] == "P":
        parts = body.split(" ", 2)
        
        key = parts[1]
        value = parts[2]
        return command, key, value
    
    else:
        return None, None, None


if __name__ == "__main__":
    start_server()


