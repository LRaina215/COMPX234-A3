import socket
import threading
import time

def client_task(name, value):
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('locahost', 6666))

        message = value
        client_socket.sendall(message.encode('utf-8'))

        response = client_socket.revc(1024).decode('utf-8')
        print(f"Reveive: {response}")

    except Exception as e:
        print(f"Error for {name}: {e}")

    finally:
        if client_socket:
            client_socket.close()