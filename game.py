import subprocess
import time
import platform

def start_server():
    """Starts the server in a new terminal with a custom name."""
    if platform.system() == "Windows":
        subprocess.Popen(["start", "cmd", "/k", "title Server & python server.py"], shell=True)
    elif platform.system() == "Linux":
        subprocess.Popen(["x-terminal-emulator", "-T", "Server", "-e", "python server.py"])
    elif platform.system() == "Darwin":  # MacOS
        subprocess.Popen(["osascript", "-e", 'tell app "Terminal" to do script "python server.py; exit" && set custom title "Server"'])

def start_client(client_number):
    """Starts a client in a new terminal with a custom name."""
    if platform.system() == "Windows":
        subprocess.Popen(["start", "cmd", "/k", f"title Client-{client_number} & python client.py"], shell=True)
    elif platform.system() == "Linux":
        subprocess.Popen(["x-terminal-emulator", "-T", f"Client-{client_number}", "-e", "python client.py"])
    elif platform.system() == "Darwin":  # MacOS
        subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "python client.py; exit" && set custom title "Client-{client_number}"'])

if __name__ == "__main__":
    print("Starting the game server...")
    start_server()
    time.sleep(2)  # Wait for the server to initialize

    print("Starting clients...")
    for i in range(1, 6):  # Change to the number of clients you want
        start_client(i)

    print("Setup complete! Check the opened terminals for interaction.")
