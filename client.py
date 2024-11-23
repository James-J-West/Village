import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def start_client():
    """Connect to the server and interact."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print("Connected to the game server.")

        # Handle server messages
        def receive_messages():
            while True:
                try:
                    message = client.recv(1024).decode()
                    if not message:
                        break
                    print(message.strip())
                except ConnectionResetError:
                    print("Disconnected from server.")
                    break

        # Start receiving messages in a separate thread
        threading.Thread(target=receive_messages, daemon=True).start()

        # Send commands to the server
        while True:
            command = input("Enter your command: ")
            if command.lower() == "quit":
                print("Exiting game.")
                break
            client.sendall(command.encode())

if __name__ == "__main__":
    start_client()
