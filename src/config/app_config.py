import json
import os

CLIENT_ID = "1451633969815752715"

default_config = {
    "version": "v1.0.0",
    "client_id": CLIENT_ID,
    "presence_refresh_interval": 5,
    

    "process_names": [
        "lion.exe",
        "Lion.exe",
    ],
    
    "show_github_link": False,
    "show_elapsed_time": True,
    
    "texts": {
        "loading": "Loading...",
        "in_menu": "Main Menu",
        "in_game": "In Game",
        "idle": "Idle",
    }
}

class Config:
    _config_path = None
    
    @staticmethod
    def get_config_folder():
        appdata = os.getenv('APPDATA')
        return os.path.join(appdata, "2xko-rpc")
    
    @staticmethod
    def get_config_path():
        return os.path.join(Config.get_config_folder(), "config.json")
    
    @staticmethod
    def fetch_config():
        try:
            config_path = Config.get_config_path()
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return Config.create_default_config()
        except:
            return default_config.copy()
    
    @staticmethod
    def modify_config(new_config):
        config_path = Config.get_config_path()
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(new_config, f, indent=2, ensure_ascii=False)
        return new_config
    
    @staticmethod
    def create_default_config():
        config = default_config.copy()
        Config.modify_config(config)
        return config
    
    @staticmethod
    def get_value(*keys):
        config = Config.fetch_config()
        value = config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                value = default_config
                for k in keys:
                    value = value.get(k, None) if isinstance(value, dict) else None
                return value
        return value