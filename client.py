import socket
import threading
import sys
import time
import platform

# Check the OS at runtime
if platform.system() == 'Windows':
    import msvcrt  # Windows-only
else:
    import select
    import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stop_event = threading.Event()

def close_client():
    if not stop_event.is_set():
        stop_event.set()
        try:
            client.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            client.close()
        except:
            pass

def handle_receive(connection):
    while not stop_event.is_set():
        try:
            data = connection.recv(2048)
            if not data:
                print("Server disconnected.")
                close_client()
                break
            if data.decode().lower() == 'exit':
                print("Server is shutting down.")
                close_client()
                break
            print(f"Received from server: {data.decode()}")
        except Exception:
            close_client()
            break

# Connect to the server
try:
    client.connect(('localhost', 12345))
except Exception as e:
    print(f"Error connecting to server: {e}")
    sys.exit(1)

print('Connected to server.')
print("Type messages (or 'exit' to quit):")

# Start the receive thread
receive_thread = threading.Thread(target=handle_receive, args=(client,), daemon=True)
receive_thread.start()

# Cross-platform input handling
buffer = ''

while not stop_event.is_set():
    if platform.system() == 'Windows':  # For Windows
        if msvcrt.kbhit():
            char = msvcrt.getwche()  # getwche() gets the character
            if char in ['\r', '\n']:  # Enter pressed
                message = buffer.strip()
                buffer = ''
                if message.lower() == 'exit':
                    try:
                        client.send(message.encode())
                    except:
                        pass
                    print("Closing connection.")
                    close_client()
                    break
                elif message:
                    try:
                        client.send(message.encode())
                    except:
                        close_client()
                        break
                print("", end='', flush=True)
            elif char == '\b':  # Handle backspace
                buffer = buffer[:-1]
            else:
                buffer += char
    else:  # For Linux or any other system
        ready, _, _ = select.select([sys.stdin], [], [], 0.1)
        if ready:
            char = sys.stdin.read(1)  # Read a single character
            if char == '\n':  # Enter pressed
                message = buffer.strip()
                buffer = ''
                if message.lower() == 'exit':
                    try:
                        client.send(message.encode())
                    except:
                        pass
                    print("Closing connection.")
                    close_client()
                    break
                elif message:
                    try:
                        client.send(message.encode())
                    except:
                        close_client()
                        break
                print("", end='', flush=True)
            elif char == '\b':  # Handle backspace
                buffer = buffer[:-1]
            else:
                buffer += char

    time.sleep(0.1)

# Wait for the receive thread to finish
receive_thread.join()
