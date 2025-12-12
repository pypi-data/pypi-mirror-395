import logging
import queue
import threading
import tkinter as tk
from tkinter import simpledialog

# EPAM Colors
COLOR_GRAVEL = "#464547"
COLOR_SCOOTER = "#39c2d7"
COLOR_WHITE = "white"

_root = None


def set_root(root):
    global _root
    _root = root


class WarningWindow:
    def __init__(self, root):
        self.root = root
        self.window = None
        self.is_visible = False

    def show(self):
        if self.is_visible:
            return

        # Schedule GUI update on main thread
        self.root.after(0, self._show_impl)

    def _show_impl(self):
        if self.window:
            return  # Already exists

        try:
            self.window = tk.Toplevel(self.root)
            self.window.overrideredirect(True)  # Frameless
            self.window.attributes("-topmost", True)
            self.window.configure(bg=COLOR_GRAVEL)

            # Dimensions and Position
            width = 450
            height = 120
            screen_width = self.window.winfo_screenwidth()
            # Position top-right, with some padding
            x = screen_width - width - 20
            y = 20
            self.window.geometry(f"{width}x{height}+{x}+{y}")

            # Side Strip (Scooter color)
            strip = tk.Frame(self.window, bg=COLOR_SCOOTER, width=10)
            strip.pack(side="left", fill="y")

            # Label
            label = tk.Label(
                self.window,
                text="VPN DISCONNECTED!\nAccessing Windows App from unauthorized region.",
                fg=COLOR_WHITE,
                bg=COLOR_GRAVEL,
                font=("Segoe UI", 12, "bold"),
            )
            label.pack(side="left", fill="both", expand=True, padx=10)

            self.is_visible = True
            logging.info("Warning Window Shown (Tkinter)")
        except Exception as e:
            logging.error(f"Failed to show warning window: {e}")

    def hide(self):
        if not self.is_visible:
            return
        self.root.after(0, self._hide_impl)

    def _hide_impl(self):
        if self.window:
            try:
                self.window.destroy()
            except Exception as e:
                logging.error(f"Error destroying window: {e}")
            self.window = None
        self.is_visible = False
        logging.info("Warning Window Hidden")

    def start(self):
        pass

    def stop(self):
        self.hide()


def get_input(title, prompt, default=""):
    if not _root:
        logging.error("GUI root not set, cannot ask for input.")
        return None

    # If we are in main thread, just call it
    if threading.current_thread() is threading.main_thread():
        return simpledialog.askstring(title, prompt, initialvalue=default, parent=_root)

    # If in another thread, we need to ask main thread and wait
    q = queue.Queue()

    def task():
        res = simpledialog.askstring(title, prompt, initialvalue=default, parent=_root)
        q.put(res)

    _root.after(0, task)
    try:
        return q.get(timeout=60)  # Wait up to 60s
    except queue.Empty:
        logging.error("Input dialog timed out")
        return None
