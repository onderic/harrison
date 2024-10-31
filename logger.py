import datetime
import requests

def log_activity(command, result, client_ip, port, data, username="", password="", location_data=None):
    with open("attack_logs.txt", "a") as log_file:
        # Log time in the specified format
        time_str = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        log_file.write(f"Time: {time_str}\n")
        log_file.write(f"IP: {client_ip}\n")
        log_file.write(f"Port: {port}\n")
        log_file.write(f"Command Executed: {command}\n")
        log_file.write(f"Command Result: {result}\n")
        log_file.write(f"Location Data: {location_data}\n") 
        log_file.write(f"Raw Data: {data}\n")
        log_file.write(f"Username: {username}\n")
        log_file.write(f"Password: {password}\n")
        
        log_file.write("======================================\n")
        
        log_file.write("\n" + "=" * 50 + "\n\n")

def get_geolocation(ip):
    # Check if the IP is in a private range
    if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.16.") or ip.startswith("172.31."):
        return "Private IP Address: Unable to determine location"

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
        
            print("Geolocation API response:", data)
            
            location_info = data
            return location_info
        else:
            print(f"Geolocation API error: Status code {response.status_code}")
            return "Location not available"
    except requests.RequestException as e:
        print(f"Geolocation API request failed: {e}")
        return "Error retrieving location data"
