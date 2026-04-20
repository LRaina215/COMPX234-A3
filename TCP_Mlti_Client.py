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

def READ(k):
    123
    return 123

def GET(k):
    123
    return 123

def PUT(k, v):
    123
    return 123

def main():
    clients = []
    i = 0
    t = threading.Thread(target=client_task, args=(f"Clinet-{i+1}",READ("abcd")))
    clients.append(t)
    t = threading.Thread(target=client_task, args=(f"Clinet-{i+1}",GET("abcd")))
    clients.append(t)
    t = threading.Thread(target=client_task, args=(f"Clinet-{i+1}",PUT("abcd")))
    clients.append(t)

    for t in clients:
        t.start()

        time.sleep()

        t.join()

if __name__ == "__main__":
    main()