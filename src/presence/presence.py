from pypresence import Presence as PyPresence
from pypresence.exceptions import InvalidPipe
from InquirerPy.utils import color_print
import time
import os
import datetime

from ..config.app_config import Config
from ..utilities.processes import Processes
from ..utilities.log_reader import LogReader
from .states import startup, menu, ingame, lobby, champion_select

DEBUG = False

class Presence:
    def __init__(self):
        self.game_start_time = None
        self.current_state = None
        self.log_reader = LogReader()
        
        client_id = Config.get_value("client_id")
        
        if client_id == "TWOJE_DISCORD_APP_ID_TUTAJ" or not client_id:
            raise Exception("Discord Application ID not set! Edit src/config/app_config.py")
        
        try:
            self.rpc = PyPresence(client_id=str(client_id))
            self.rpc.connect()
            color_print([("LimeGreen", "Connected to Discord!")])
        except InvalidPipe as e:
            raise Exception(f"Discord is not running: {e}")
    
    def update_presence(self, state_type, **kwargs):
        states = {
            "startup": startup,
            "menu": menu,
            "lobby": lobby,
            "inGame": ingame,
            "ingame": ingame,
            "champion_select": champion_select,
            "loading": startup,
        }
        
        if state_type in states:
            states[state_type].presence(
                self.rpc,
                game_running=Processes.is_game_running(),
                elapsed_time=self.game_start_time,
                **kwargs
            )
            self.current_state = state_type
    
    def main_loop(self):
        refresh_interval = Config.get_value("presence_refresh_interval") or 3
        
        if DEBUG:
            color_print([("Yellow bold", "\n" + "="*60)])
            color_print([("Yellow bold", "  2XKO-RPC - GAME LOG MONITORING")])
            color_print([("Yellow bold", "="*60)])
            
            log_info = self.log_reader.get_state_info()
            if log_info['log_available']:
                color_print([("LimeGreen", f"✓ Logs found: {log_info['log_path']}")])
            else:
                color_print([("Red", f"✗ Logs not found! Start 2XKO.")])
            
            color_print([("White", f"Refresh interval: {refresh_interval}s")])
            color_print([("Cyan", "Monitoring game logs in real-time.\n")])
        else:
            color_print([("Cyan", "Monitoring game integration...")])
        
        
        while True:
            try:
                game_running = Processes.is_game_running()
                
                if game_running:
                    if self.game_start_time is None:
                        self.game_start_time = int(time.time())
                        color_print([("LimeGreen bold", "\n>>> 2XKO DETECTED! <<<")])
                    
                    state, events, new_lines = self.log_reader.detect_state()
                    
                    if DEBUG and events:
                        print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] "
                              f"New events ({len(events)}):")
                        for event in events:
                            color_print([("Cyan", f"  → {event['event']}: "),
                                        ("White", f"{event['match']}")])
                    
                    if DEBUG:
                        state_colors = {
                            "lobby": "Yellow",
                            "inGame": "LimeGreen",
                            "champion_select": "Magenta",
                            "loading": "Cyan",
                        }
                        color = state_colors.get(state, "White")
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] "
                              f"State: ", end="")
                        color_print([(color, state.upper())])
                        
                        if self.log_reader.current_nickname:
                            color_print([("Magenta", f"Nick: {self.log_reader.current_nickname}")])
                    
                    self.update_presence(state, nickname=self.log_reader.current_nickname)
                    
                else:
                    if self.game_start_time is not None:
                        color_print([("Yellow", "\n>>> 2XKO CLOSED <<<")])
                        self.game_start_time = None
                        self.log_reader.seek_to_end()
                    
                    if DEBUG:
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] "
                              f"Waiting for 2XKO...")
                    
                    self.update_presence("startup")
                
                time.sleep(refresh_interval)
                
            except KeyboardInterrupt:
                color_print([("Yellow", "\nClosing...")])
                break
    
    def init_loop(self):
        try:
            color_print([("Cyan", "Starting Rich Presence...")])
            self.update_presence("startup")
            self.main_loop()
        except Exception as e:
            color_print([("Red", f"Presence Error: {e}")])
            raise
