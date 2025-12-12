import platform
import os
import ctypes

def get_platform():
    return platform.system().lower()

def is_admin():
    system = get_platform()
    try:
        if system == "windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False
