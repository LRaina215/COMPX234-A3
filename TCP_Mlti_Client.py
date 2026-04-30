import socket
import threading
import time
import sys

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
         
# use to deriver the data length and receive correct and valid message from Server 
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
    
    total_length = int(header.decode('utf-8')) # Convert the length into integer

    rest  = recv_exact(sock, total_length - 3) # Receive data (length is `total_length`)

    if rest is None:
        return None
    
    return (header + rest).decode('utf-8')

def main():
    if len(sys.argv) != 4:
        print("Using input type: python3 TCP_Mlti_Client.py <hostname> <port> <request_file>")
        return
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]

    print(f"Receive the Host: {host}")
    print(f"Receive the Port: {port}")

    cilent_socket = None

    try:
        cilent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cilent_socket.connect((host, port))

        with open(request_file, "r", encoding='utf-8') as f:
            for line in f:
                ori_line = line.strip()

                if ori_line == "":
                    continue

                message  = file_command2protocol_message(ori_line)

                if message is None:
                    print(f"{ori_line}: invalid request")
                    continue
                
                print(f"Finally Read Line: {ori_line}")
                print(f"Finally Protocal Message: {message}")

                cilent_socket.sendall(message.encode('utf-8'))

                response = recv_message(cilent_socket)

                if response is None:
                    print("Server closed connection.")
                    break

                response_body = response[4:]
                print(f"{ori_line}: {response_body}")

    except Exception as e:
        print(f"Cilent error: {e}")

    finally:
        if cilent_socket:
            cilent_socket.close()

if __name__ == "__main__":
    main()