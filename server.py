import socket
import commands
import logger
from decouple import config

# Simple user credentials for demonstration
USER_CREDENTIALS = {
    "admin": "12345", 
}

# ASCII Art for Linux Logo (Tux)
LINUX_LOGO = r"""
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/        
"""

HACKER_EMOJI = "🕶️"

def start_server(host="0.0.0.0", port=2000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[INFO] Honeypot listening on {host}:{port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        client_ip = config('IP')
        print(f"[INFO] Connection established from {client_ip}")

        # Fetch geolocation data
        location_data = logger.get_geolocation(client_ip)
        print(f"[INFO] Geolocation data for {client_ip}: {location_data}")
        
        # Send logo and welcome message to the client
        client_socket.sendall((LINUX_LOGO + "\n" + f"{HACKER_EMOJI} Welcome to Kali Linux 2024! {HACKER_EMOJI}\n").encode())
        client_socket.send(b"Enter your credentials below:\n")
        
        # Login loop
        username = ""
        password = ""
        
        # Get username
        while not username:
            client_socket.send(b"Username: ")
            username = client_socket.recv(1024).decode().strip()
            print(f"[INFO] Received username: {username}")

        # Get password
        while not password:
            client_socket.send(b"Password: ")
            password = client_socket.recv(1024).decode().strip()
            print(f"[INFO] Received password for user: {username}")

        # Check credentials
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            client_socket.send(b"Login successful!\n")
            print(f"[INFO] Login successful for user: {username}")
            logger.log_activity("", "", client_ip, port, "", username, password, location_data)
        else:
            client_socket.send(b"Login failed!\n")
            print(f"[WARNING] Login failed for user: {username} from {client_ip}")
            logger.log_activity("", "", client_ip, port, "", username, password, location_data)
            client_socket.close()
            continue
        
        print(f"[INFO] User {username} is now interacting with the system.")
        
        while True:
            try:
                client_socket.send(b"kali@kali:~$ ")
                command = client_socket.recv(1024).decode().strip()
                print(f"[INFO] User {username} executed command: {command}")
                
                result = commands.simulate_command(command)
                logger.log_activity(command, result, client_ip, port, "", username=username, password=password, location_data=location_data)

                # Send result to the client
                client_socket.send(result.encode() + b"\n")
                print(f"[INFO] Command result sent to {username}: {result.strip()}")
                
            except (ConnectionResetError, BrokenPipeError):
                print(f"[INFO] {client_ip} disconnected.")
                break
        
        client_socket.close()
        print(f"[INFO] Connection with {client_ip} closed.")

if __name__ == "__main__":
    start_server()
