# commands.py

# Initial working directory for the user
current_directory = "/home/kali"

# Simulated file contents
file_system = {
    "/home/kali/README.md": "This is a README file.\n",
    "/home/kali/requirements.txt": "django==3.2\n",
    "/home/kali/myapp/models.py": "# Models for the app\n",
}

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
    
    if not path:
        path = current_directory

    if path not in django_structure:
        return "ls: no such file or directory"
    
    return "  ".join(django_structure.get(path, []))

def pwd():
    return current_directory

def cat(filename=""):
    """Simulate reading file contents."""
    filepath = f"{current_directory}/{filename}" if filename else ""
    if filepath in file_system:
        return file_system[filepath]
    return f"cat: {filename}: No such file or directory"

def mkdir(dirname=""):
    return f"Directory {dirname} created" if dirname else "mkdir: missing operand"

def touch(filename=""):
    filepath = f"{current_directory}/{filename}" if filename else ""
    if filename:
        file_system[filepath] = ""  # Create an empty file
        return f"File {filename} created"
    return "touch: missing operand"

def cd(dirname):
    global current_directory
    if dirname == "..":
        if current_directory != "/home/kali":
            current_directory = "/home/kali"
        return f"Changed directory to {current_directory}"
    
    new_path = f"{current_directory}/{dirname}"
    if new_path in ["/home/kali/myapp", "/home/kali/venv"]:
        current_directory = new_path
        return f"Changed directory to {current_directory}"
    
    return f"cd: no such file or directory: {dirname}"

def open_file(filename=""):
    filepath = f"{current_directory}/{filename}" if filename else ""
    if filename:
        if filepath in file_system:
            return f"File {filename} opened. Current contents:\n{file_system[filepath]}"
        return f"open_file: {filename}: No such file or directory"
    return "open_file: missing file operand"

def write_file(filename="", content=""):
    filepath = f"{current_directory}/{filename}" if filename else ""
    if filename:
        if filepath in file_system:
            file_system[filepath] += content + "\n"
            return f"Written to {filename}."
        return f"write_file: {filename}: No such file or directory"
    return "write_file: missing file operand"

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
        "open_file": open_file,
        "write_file": write_file,
    }
    
    parts = command.split(" ", 1)
    base_command = parts[0]
    args = parts[1].split(" ", 1) if len(parts) > 1 else []
    
    return commands.get(base_command, lambda *args: "Command not found")(*args)
