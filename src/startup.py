from InquirerPy.utils import color_print
import time
import ctypes
import cursor
import os

from .utilities.killable_thread import Thread
from .utilities.processes import Processes
from .utilities.systray import Systray
from .config.app_config import Config
from .presence.presence import Presence

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class Startup:
    def __init__(self):
        if Processes.is_program_already_running():
            color_print([("Red", "2XKO-RPC is already running!")])
            time.sleep(3)
            os._exit(1)
        
        ctypes.windll.kernel32.SetConsoleTitleW(f"2XKO-RPC {Config.get_value('version')}")
        
        color_print([("Cyan", "Connecting to Discord...")])
        
        try:
            self.presence = Presence()
        except Exception as e:
            color_print([("Red", f"Error: {e}")])
            color_print([("Yellow", "\nMake sure:")])
            color_print([("White", "  1. Discord is running")])
            color_print([("White", "  2. You set Discord Application ID in src/config/app_config.py")])
            input("\nPress Enter to close...")
            os._exit(1)
        
        self.run()
    
    def run(self):
        
        self.systray = Systray(on_exit_callback=self.on_exit)
        self.systray_thread = Thread(target=self.systray.run)
        self.systray_thread.start()
        
        self.presence_thread = Thread(target=self.presence.init_loop, daemon=True)
        self.presence_thread.start()
        
        color_print([("LimeGreen bold", "\n2XKO-RPC started successfully!")])
        color_print([("Yellow", "Window will remain open.")])
        color_print([("Gray", "To close: Ctrl+C or use System Tray icon.\n")])
        
        self.systray_thread.join()
        self.presence_thread.stop()
    
    def on_exit(self):
        if hasattr(self, 'presence_thread'):
            self.presence_thread.stop()
