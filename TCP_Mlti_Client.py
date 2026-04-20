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

def main():
    clients = []
    for i in range(3):
        t = threading.Thread(target=client_task, args=(f"Clinet-{i+1}", ))
        clients.append(t)
        t.start()

        time.sleep()
    
    for t in clinets:
        t.join()

if __name__ == "__main__":
    main()