import argparse
import datetime
import logging
import os
import sys
import threading
import tkinter as tk
import winreg

from . import gui, monitor, tray

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ALLOWED_COUNTRY = os.environ.get("ALLOWED_COUNTRY", "HU")
APP_NAME = "VPNMonitor"


def install_startup():
    """Registers the application to run at startup."""
    exe_path = sys.executable
    logging.info(f"Registering startup: {exe_path}")
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        print(f"Successfully registered {APP_NAME} for startup.")
    except Exception as e:
        print(f"Failed to register startup: {e}")


def remove_startup():
    """Removes the application from startup."""
    logging.info("Removing startup registration")
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        print(f"Successfully removed {APP_NAME} from startup.")
    except FileNotFoundError:
        print(f"{APP_NAME} was not registered for startup.")
    except Exception as e:
        print(f"Failed to remove startup: {e}")


class VPNMonitorApp:
    """Main application class for VPN Monitor."""

    def __init__(self, root):
        """Initialize the VPN Monitor application."""
        self.root = root
        gui.set_root(root)

        self.allowed_country = ALLOWED_COUNTRY
        self.snooze_until = None
        self.warning_window = gui.WarningWindow(root)
        self.tray_icon = tray.TrayIcon(
            on_exit=self.on_exit,
            on_snooze=self.on_snooze,
            on_unsnooze=self.on_unsnooze,
            on_set_country=self.on_set_country,
            show_set_country=not monitor.has_allowed_ips_file(),
        )

    def on_exit(self):
        """Handle exit action."""
        logging.info("Exiting...")
        self.warning_window.stop()
        self.tray_icon.stop()
        # Schedule root destroy on main thread
        self.root.after(0, self.root.quit)

    def on_snooze(self, minutes):
        """Handle snooze action."""
        self.snooze_until = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        logging.info(f"Snoozed until: {self.snooze_until}")
        self.warning_window.hide()
        self.tray_icon.update_menu(is_snoozed=True)

    def on_unsnooze(self):
        """Handle unsnooze action."""
        self.snooze_until = None
        logging.info("Snooze cancelled")
        self.tray_icon.update_menu(is_snoozed=False)

    def on_set_country(self):
        """Handle set country action."""
        # This runs in tray thread, gui.get_input handles thread safety
        new_country = gui.get_input(
            "Set Allowed Country",
            "Enter 2-letter Country Code (e.g. US, DE):",
            self.allowed_country,
        )
        if new_country:
            self.allowed_country = new_country.upper()
            logging.info(f"Allowed Country updated to: {self.allowed_country}")

    def monitor_loop(self):
        """Main monitoring loop."""
        while True:
            if self.snooze_until and datetime.datetime.now() < self.snooze_until:
                pass  # Snoozed
            else:
                is_safe = monitor.check_safety(self.allowed_country)
                if not is_safe:
                    self.warning_window.show()
                else:
                    self.warning_window.hide()

            threading.Event().wait(5)

    def run(self):
        """Start the application."""
        logging.info(f"Starting VPN Monitor. Allowed Country: {self.allowed_country}")

        # Start Monitor Thread
        monitor_thread = threading.Thread(target=self.monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()

        # Start Tray Thread
        # pystray run() blocks, so we put it in a thread
        tray_thread = threading.Thread(target=self.tray_icon.run)
        tray_thread.daemon = True
        tray_thread.start()

        logging.info("App running. Check system tray.")

        # Run Tkinter Main Loop (Blocking)
        self.root.mainloop()


def main():
    """Entry point for the VPN Monitor application."""
    parser = argparse.ArgumentParser(description="VPN Monitor")
    parser.add_argument(
        "--install-startup", action="store_true", help="Register to run at Windows startup"
    )
    parser.add_argument("--remove-startup", action="store_true", help="Remove from Windows startup")
    args = parser.parse_args()

    if args.install_startup:
        install_startup()
        return
    if args.remove_startup:
        remove_startup()
        return

    # Initialize Tkinter Root
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    app = VPNMonitorApp(root)
    app.run()


if __name__ == "__main__":
    main()
