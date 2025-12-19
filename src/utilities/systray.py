import pystray
from PIL import Image
import os
import sys

class Systray:
    def __init__(self, on_exit_callback=None):
        self.on_exit_callback = on_exit_callback
        self.icon = None
        
        self.icon_path = self._find_icon()
    
    def _find_icon(self):
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "icon.jpg"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "icon.png"),
            os.path.join(os.getcwd(), "assets", "icon.jpg"),
            os.path.join(os.getcwd(), "assets", "icon.png"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _create_image(self):
        if self.icon_path and os.path.exists(self.icon_path):
            img = Image.open(self.icon_path)
            img = img.resize((64, 64), Image.Resampling.LANCZOS)
            return img
        else:
            img = Image.new('RGB', (64, 64), color='red')
            return img
    
    def _on_exit(self, icon, item):
        icon.stop()
        if self.on_exit_callback:
            self.on_exit_callback()
        os._exit(0)
    
    def _on_restart(self, icon, item):
        icon.stop()
        python = sys.executable
        os.execl(python, python, *sys.argv)
    
    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem("2XKO-RPC", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Restart", self._on_restart),
            pystray.MenuItem("Exit", self._on_exit),
        )
        
        self.icon = pystray.Icon(
            name="2xko-rpc",
            icon=self._create_image(),
            title="2XKO Rich Presence",
            menu=menu
        )
        
        self.icon.run()
    
    def stop(self):
        if self.icon:
            self.icon.stop()
    
    @staticmethod
    def restart():
        python = sys.executable
        os.execl(python, python, *sys.argv)
