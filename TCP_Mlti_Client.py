import socket
import threading
import time
import sys

# def client_task(name, value):
#     client_socket = None
#     try:
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect(('localhost', 6666))

#         message = value
#         client_socket.sendall(message.encode('utf-8'))

#         response = client_socket.recv(1024).decode('utf-8')
#         print(f"Reveive: {response}")

#     except Exception as e:
#         print(f"Error for {name}: {e}")

#     finally:
#         if client_socket:
#             client_socket.close()

# def READ(k):
#     123
#     return 123

# def GET(k):
#     123
#     return 123

# def PUT(k, v):
#     123
#     return 123

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

if __name__ == "__main__":
    main()