import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 12345))
server.listen(3)

stop_event = threading.Event()
client_counter = 0  # Counter to assign unique numbers to clients
client_lock = threading.Lock()  # Lock to ensure thread-safe increment
clients = []  # List to store active client connections
client_threads = []  # List to store active client threads


def close_client(connection):
    try:
        connection.close()
    except Exception as e:
        print(f"Error closing client connection: {e}")


def handle_client(connection, addr, client_number):
    print(f"Client #{client_number} connected from {addr}")
    while not stop_event.is_set():
        try:
            data = connection.recv(2048)
            if not data or data.decode().lower() == 'exit':
                print(f"Client #{client_number} disconnected.")
                with client_lock:
                    clients.remove(connection)
                close_client(connection)
                break
            print(f"Received from Client #{client_number} ({addr}): {data.decode()}")
        except Exception as e:
            if not stop_event.is_set():
                print(f"Error with Client #{client_number} ({addr}): {e}")
            with client_lock:
                if connection in clients:
                    clients.remove(connection)
            close_client(connection)
            break

def start_server():
    global client_counter
    print('Server is listening...')
    while not stop_event.is_set():
        try:
            connection, addr = server.accept()
            with client_lock:
                client_counter += 1
                client_number = client_counter
                clients.append(connection)
            client_thread = threading.Thread(
                target=handle_client,
                args=(connection, addr, client_number),
                daemon=True
            )
            client_threads.append(client_thread)
            client_thread.start()
        except Exception as e:
            if not stop_event.is_set():
                print(f"Error accepting connection: {e}")
                break


def server_input_handler():
    while not stop_event.is_set():
        command = input()
        if command.lower() == 'exit':
            print("Shutting down server...")
            stop_event.set()
            close_server()
            break
        else:
            with client_lock:
                for client in clients:
                    try:
                        client.sendall(command.encode())
                    except Exception as e:
                        print(f"Error sending message to a client: {e}")

def close_server():
    stop_event.set()
    with client_lock:
        for client in clients:
            close_client(client)
    for thread in client_threads:
        thread.join()
    server.close()
    print("Server closed.")


try:
    input_thread = threading.Thread(target=server_input_handler)
    input_thread.start()
    start_server()
except KeyboardInterrupt:
    print("Shutting down server...")
finally:
    close_server()
