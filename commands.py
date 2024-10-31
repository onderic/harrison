# commands.py

# Initial working directory for the user
current_directory = "/home/kali"

def whoami():
    return "kali"

def uname():
    return "Linux kali 5.10.0-kali3-amd64 #1 SMP Debian 5.10.13-1kali1 (2021-02-08) x86_64 GNU/Linux"

def ls(path=""):
    """Simulate the directory structure of a Django project."""
    # Simulated Django project directory structure
    django_structure = {
        "/home/kali": ["manage.py", "myapp", "venv", "requirements.txt", "README.md"],
        "/home/kali/myapp": ["migrations", "__init__.py", "admin.py", "apps.py", "models.py", "tests.py", "views.py"],
        "/home/kali/myapp/migrations": ["__init__.py", "0001_initial.py"],
        "/home/kali/venv": ["bin", "lib", "include", "pyvenv.cfg"],
    }
    
    # If path is not provided, use the current directory
    if not path:
        path = current_directory

    # If path does not exist in the structure
    if path not in django_structure:
        return "ls: no such file or directory"
    
    # Return contents of the directory if it exists
    return "  ".join(django_structure.get(path, []))

def pwd():
    return current_directory

def cat(filename=""):
    # Simulate reading file contents
    if filename:
        return f"Contents of {filename}" 
    else:
        return "cat: missing file operand"

def mkdir(dirname=""):
    return f"Directory {dirname} created" if dirname else "mkdir: missing operand"

def touch(filename=""):
    return f"File {filename} created" if filename else "touch: missing operand"

def cd(dirname):
    global current_directory
    # Check if the directory exists
    if dirname == "..":
        # Simulate moving to the parent directory
        if current_directory != "/home/kali":
            current_directory = "/home/kali" 
        return f"Changed directory to {current_directory}"
    
    # Simulated directory change
    new_path = f"{current_directory}/{dirname}"
    if new_path in ["/home/kali/myapp", "/home/kali/venv"]:
        current_directory = new_path
        return f"Changed directory to {current_directory}"
    
    return f"cd: no such file or directory: {dirname}"

def simulate_command(command):
    """Map commands to functions."""
    commands = {
        "whoami": whoami,
        "uname": uname,
        "ls": ls,
        "pwd": pwd,
        "cat": cat,
        "mkdir": mkdir,
        "touch": touch,
        "cd": cd,  
    }
    
    parts = command.split()
    base_command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    
    return commands.get(base_command, lambda *args: "Command not found")(*args)

