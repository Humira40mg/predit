import os

def get_full_path(path:str):
    if path.startswith("~"):
        return os.path.expanduser(path)
    elif path.startswith("."):
        return os.path.abspath(path)
    return path

def check_if_exist(*args):
    for arg in args:
        if not os.path.exists(arg) : return False
    return True
