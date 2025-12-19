from InquirerPy.utils import color_print
import ctypes, os, traceback, signal, sys

from src.startup import Startup
from src.config.app_config import default_config

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

def signal_handler(sig, frame):
    color_print([("Yellow", "\n\nExiting 2XKO-RPC...")])
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    color_print([("Cyan", f"""
    ██████╗ ██╗  ██╗██╗  ██╗ ██████╗ 
    ╚════██╗╚██╗██╔╝██║ ██╔╝██╔═══██╗
     █████╔╝ ╚███╔╝ █████╔╝ ██║   ██║
    ██╔═══╝  ██╔██╗ ██╔═██╗ ██║   ██║
    ███████╗██╔╝ ██╗██║  ██╗╚██████╔╝
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
"""), ("White", f"Discord Rich Presence {default_config['version']}\n")])
    try:
        app = Startup()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            os._exit(0)
        except:
            pass
    except Exception as e:
        user32.ShowWindow(hWnd, 1)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
        color_print([("Red bold", "CRITICAL ERROR:")])
        traceback.print_exc()
        input("Press Enter to close...")
        os._exit(1)