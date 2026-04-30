import socket
import threading
import sys
tuple_space = {}
lock = threading.Semaphore(1)

def handle_client(client_socket, addr):
    print(f"New client connected from {addr}")

    try:
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Client says: {message}")

        command, key, value = process_message(message)
        print(f"Reveived command from Client = {command}, key={key}, value={value}")
        
        response = response_message(command, key, value)
        print(f"Response body: {response}")

        full_response = full_response_message(response)
        client_socket.sendall(full_response.encode('utf-8'))

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

# use to process message that sends back to Client as a feedback
def response_message(command, key, value):
    lock.acquire()

    if command[0] == "R":
        if key in tuple_space:
            stored_value = tuple_space[key]
            lock.release()
            return f"OK {key}, {stored_value} read"
        else:
            lock.release()
            return f"ERR {key} doesn't exist"

    elif command[0] == "G":
        if key in tuple_space:
            stored_value = tuple_space[key]
            del tuple_space[key] # delete key in space
            lock.release()
            return f"OK ({key}, {stored_value}) removed"
        else:
            lock.release()
            return f"ERR {key} does not exist"

    elif command[1] == "P":
        if key in tuple_space:
            lock.release()
            return f"ERR {key} already exists"
        else:
            tuple_space[key] = value
            lock.release()
            return f"OK ({key}, {value}) added"

    else:
        lock.release()
        return f"ERR invalid command"
    
# use to process command send from client to derive command, key and value(if has)
def process_message(message):
    body = message[4:]

    command = body[0]

    if body[0] == "R":
        key = body[2:]
        return command, key, None

    elif body[0] == "G":
        key = body[2:]
        return command, key, None

    elif body[0] == "P":
        parts = body.split(" ", 2)
        
        key = parts[1]
        value = parts[2]
        return command, key, value
    
    else:
        return None, None, None
    
# add length of response message
def full_response_message(response):
    total_length = len(response) + 4
    return f"{total_length:03d} {response}"


if __name__ == "__main__":
    start_server()


