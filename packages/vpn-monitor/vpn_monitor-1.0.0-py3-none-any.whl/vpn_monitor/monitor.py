import ctypes
import logging
import os
import sys

import psutil
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TARGET_PROCESSES = ["msrdc.exe", "Windows365.exe"]


def is_target_running():
    """Checks if any of the target processes have a VISIBLE window."""
    user32 = ctypes.windll.user32

    # Set of PIDs that belong to target processes
    target_pids = set()
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] in TARGET_PROCESSES:
                target_pids.add(proc.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if not target_pids:
        return False

    # Check if any of these PIDs have a visible window
    found_visible = False

    def enum_windows_callback(hwnd, _):
        nonlocal found_visible
        if found_visible:
            return False  # Stop enumeration

        if user32.IsWindowVisible(hwnd):
            pid = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value in target_pids:
                # Double check it's not a zero-sized window or something
                # But IsWindowVisible is usually good enough for "user perceives it as open"
                logging.info(f"Visible window found for PID {pid.value}")
                found_visible = True
                return False  # Stop enumeration
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)

    return found_visible


def get_network_info():
    """Gets the current network info (IP, country) from ip-api.com."""
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        logging.error(f"Error checking IP: {e}")
        return None
    return None


def get_allowed_ips():
    """Reads allowed IPs from 'allowed_ips.txt' in the same directory as the executable."""
    # Determine the directory of the executable
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        # If running as script, use CWD or script dir.
        # Using CWD is safer for 'run.py' usage from root.
        exe_dir = os.getcwd()

    file_path = os.path.join(exe_dir, "allowed_ips.txt")

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r") as f:
            # Filter out empty lines and comments if any (though simple list is requested)
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Error reading allowed_ips.txt: {e}")
        return []


def has_allowed_ips_file():
    """Checks if 'allowed_ips.txt' exists."""
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.getcwd()

    file_path = os.path.join(exe_dir, "allowed_ips.txt")
    return os.path.exists(file_path)


def check_safety(allowed_country):
    """
    Returns:
        bool: True if SAFE (App not running OR Region is correct OR IP is allowed), False if UNSAFE.
    """
    if not is_target_running():
        return True

    network_info = get_network_info()

    if not network_info:
        # If we can't check region, we assume safe to avoid blocking legitimate use offline
        logging.warning("Could not verify network info. Assuming safe.")
        return True

    current_ip = network_info.get("query")
    current_region = network_info.get("countryCode")

    # 1. Check Allowed IPs (Precedence)
    allowed_ips = get_allowed_ips()
    if current_ip and current_ip in allowed_ips:
        logging.info(f"IP {current_ip} is in allowed list. Safe.")
        return True

    # 2. Check Region
    if current_region != allowed_country:
        logging.warning(f"UNSAFE! Current: {current_region}, Allowed: {allowed_country}")
        return False

    return True
