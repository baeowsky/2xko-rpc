import os
import time
import re
from collections import deque

class LogReader:
    PATTERNS = {
        'mode_main_menu': re.compile(r'Starting Mode\.MainMenu'),
        'mode_game': re.compile(r'Starting Mode\.Game'),
        'mode_game_end': re.compile(r'Ending Mode\.Game'),
        
        'game_started': re.compile(r'game started \[game-id: ([^\]]+)\]'),
        'series_idle': re.compile(r'Update state \[State:ELionSeriesState::Idle\]'),
        'match_end_requested': re.compile(r'ProcessEndGame.*Result:ELionOutcomeResult::'),
        
        'widget_main_menu': re.compile(r'WBP_MainMenu(?!.*TeachingFight)'),
        'widget_play_screen': re.compile(r'WBP_MainMenu_Play'),
        'widget_learn_menu': re.compile(r'WBP_LearnMenu(?!Wrapper)'),
        
        'widget_teaching_fight': re.compile(r'WBP_TeachingFightMenu'),
        'widget_gameplay': re.compile(r'WBP_GameplayMenusOverlay'),
        
        'loading_finished': re.compile(r'Loading finished\. Starting game'),
        'level_spawner': re.compile(r'Spawning lion level in stage'),
        
        'champion_select': re.compile(r'champion.?select|character.?select', re.IGNORECASE),
        
        'chat_connected': re.compile(r"Chat session state for '([^']+)' has been set to connected"),
    }

    def __init__(self):
        self.log_path = self._find_log_path()
        self.current_state = "lobby"
        self.current_game_id = None
        self.current_nickname = None
        self.last_lines = deque(maxlen=50)
        
        if self.is_log_available():
             self._scan_for_nickname_at_start()
        
        self.last_position = 0
        if self.is_log_available():
            file_size = os.path.getsize(self.log_path)
            self.last_position = max(0, file_size - 50000)
    
    def _scan_for_nickname_at_start(self):
        try:
            with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    match = self.PATTERNS['chat_connected'].search(line)
                    if match:
                        if match.groups():
                            self.current_nickname = match.groups()[0]
                            return
                    if i > 20000: 
                        break
        except:
            pass
            
    def _find_log_path(self):
        appdata = os.getenv('LOCALAPPDATA')
        log_path = os.path.join(appdata, 'Lion', 'Saved', 'Logs', 'Lion.log')
        
        if os.path.exists(log_path):
            return log_path
        return None
    
    def is_log_available(self):
        return self.log_path and os.path.exists(self.log_path)
    
    def read_new_lines(self):
        if not self.is_log_available():
            return []
        
        try:
            with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(self.last_position)
                
                new_lines = f.readlines()
                
                self.last_position = f.tell()
                
                return new_lines
        except Exception as e:
            return []
    
    def analyze_line(self, line):
        events = []
        
        for event_name, pattern in self.PATTERNS.items():
            match = pattern.search(line)
            if match:
                events.append({
                    'event': event_name,
                    'match': match.group(0),
                    'groups': match.groups() if match.groups() else None,
                    'line': line.strip()
                })
        
        return events
    
    def detect_state(self):
        new_lines = self.read_new_lines()
        all_events = []
        
        for line in new_lines:
            self.last_lines.append(line)
            events = self.analyze_line(line)
            all_events.extend(events)
            
            for event in events:
                self._update_state(event)
        
        return self.current_state, all_events, len(new_lines)
    
    def _update_state(self, event):
        event_name = event['event']
        
        if event_name in ['mode_main_menu', 'series_idle']:
            self.current_state = "lobby"
            self.current_game_id = None
        
        elif event_name == 'game_started':
            self.current_state = "loading"
            if event['groups']:
                self.current_game_id = event['groups'][0]
        
        elif event_name in ['loading_finished', 'level_spawner']:
            self.current_state = "inGame"
        
        elif event_name in ['mode_game', 'widget_teaching_fight', 'widget_gameplay']:
            self.current_state = "inGame"
        
        elif event_name in ['mode_game_end', 'match_end_requested']:
            self.current_state = "lobby"
            self.current_game_id = None
        
        elif event_name == 'champion_select':
            self.current_state = "champion_select"
            
        elif event_name == 'chat_connected':
            if event['groups']:
                self.current_nickname = event['groups'][0]
    
    def get_state_info(self):
        return {
            'state': self.current_state,
            'game_id': self.current_game_id,
            'nickname': self.current_nickname,
            'log_available': self.is_log_available(),
            'log_path': self.log_path,
        }
    
    def reset_position(self):
        self.last_position = 0
    
    def seek_to_end(self):
        if self.is_log_available():
            self.last_position = os.path.getsize(self.log_path)