import socket
import threading
import time
import sys

def client_task(name, port, value):
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', port))

        message = value
        client_socket.sendall(message.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Reveive: {response}")

    except Exception as e:
        print(f"Error for {name}: {e}")

    finally:
        if client_socket:
            client_socket.close()

# def READ(k):
#     123
#     return 123

# def GET(k):
#     123
#     return 123

# def PUT(k, v):
#     123
#     return 123

def file_command2protocol_message(line):
    parts = line.split(" ", 2) # command from file is splited by " " at most 2 times
    operation = parts[0]

    # We have three operations, then we need to process four situations(include input invalid)
    if operation == "READ":
        # if the 
        if len(parts) != 2:
            return None
    
        key = parts[1]
        body = f"R {key}"

    elif operation == "GET":
        if len(parts) != 2:
            return None
        
        key = parts[1]
        body = f"G {key}"

    elif operation == "PUT":
        if len(parts) != 3:
            return None
        
        key = parts[1]
        value = parts[2]
        body = f"P {key} {value}"

    else:
        return None
    
    # calculate the length and construct a full message
    total_length = len(body) + 4
    message = f"{total_length:03d} {body}" # Here use :03d let output like, 001 002 003
    
    return message
         


def main():
    if len(sys.argv) != 4:
        print("Using input type: python3 TCP_Mlti_Client.py <hostname> <port> <request_file>")
        return
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]

    print(f"Receive the Host: {host}")
    print(f"Receive the Port: {port}")

    with open(request_file, "r", encoding='utf-8') as f:
        for line in f:
            ori_line = line.strip()

            if ori_line == "":
                continue

            print(f"Finally Read Line: {ori_line}")

            message  = file_command2protocol_message(ori_line)

            if message is None:
                print(f"{ori_line}: invalid request")
                continue

            print(f"Finally Protocal Message: {message}")

            client_task("Test", port, message)
            
if __name__ == "__main__":
    main()