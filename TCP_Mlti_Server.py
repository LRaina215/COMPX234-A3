import socket
import threading
import sys

tuple_space = {}
lock = threading.Semaphore(1)

stats = {
    "clients": 0,
    "operations": 0,
    "reads": 0,
    "gets": 0,
    "puts": 0,
    "errors": 0
}

def handle_client(client_socket, addr):
    print(f"New client connected from {addr}")

    try:
        while True:
            message = recv_message(client_socket)
            
            if message is None:
                break

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
    if len(sys.argv) != 2:
        print("Usage: python3 TCP_Mlti_Server.py <port>")
        return
    
    host = 'localhost'
    port = int(sys.argv[1])

    if port < 50000 or port > 59999:
        print("Port must be between 50000 and 59999.")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server is running and ready to accept multiple client.")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            lock.acquire()
            try:
                stats["clients"] += 1
            finally:
                lock.release()
                
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
    try:
        stats["operations"] += 1

        if command == "R":
            stats["reads"] += 1
            if key in tuple_space:
                stored_value = tuple_space[key]
                return f"OK ({key}, {stored_value}) read"
            else:
                stats["errors"] += 1
                return f"ERR {key} does not exist"

        elif command == "G":
            stats["gets"] += 1
            if key in tuple_space:
                stored_value = tuple_space[key]
                del tuple_space[key] # delete key in space
                return f"OK ({key}, {stored_value}) removed"
            else:
                stats["errors"] += 1
                return f"ERR {key} does not exist"

        elif command == "P":
            stats["puts"] += 1
            if key in tuple_space:
                stats["errors"] += 1
                return f"ERR {key} already exists"
            else:
                tuple_space[key] = value
                return f"OK ({key}, {value}) added"

        else:
            stats["errors"] += 1
            return f"ERR invalid command"
    finally:
        lock.release()
    
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

def recv_exact(sock, n):
    data = b""

    while len(data) < n: # we need n bytes data, if not enouth, continue receiving until has receive n bytes
        chunk = sock.recv(n - len(data))

        if not chunk:
            return None
        
        data += chunk

    return data

def recv_message(sock):
    header = recv_exact(sock, 3)
    
    if header is None:
        return None
    
    totoal_length = int(header.decode('utf-8')) # Convert the length into integer

    rest  = recv_exact(sock, totoal_length - 3) # Receive data (length is `total_length`)

    if rest is None:
        return None
    
    return (header + rest).decode('utf-8')


if __name__ == "__main__":
    start_server()


