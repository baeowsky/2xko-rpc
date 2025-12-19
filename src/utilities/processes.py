import psutil

from ..config.app_config import Config

class Processes:
    
    @staticmethod
    def is_game_running():
        process_names = Config.get_value("process_names")
        if not process_names:
            process_names = ["Lion.exe"]
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name']
                if proc_name and proc_name.lower() in [p.lower() for p in process_names]:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    
    @staticmethod
    def get_game_process():
        process_names = Config.get_value("process_names")
        if not process_names:
            process_names = ["Lion.exe"]
        
        for proc in psutil.process_iter(['name', 'pid', 'create_time']):
            try:
                proc_name = proc.info['name']
                if proc_name and proc_name.lower() in [p.lower() for p in process_names]:
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    
    @staticmethod
    def is_program_already_running():
        current_pid = psutil.Process().pid
        count = 0
        
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.cmdline()
                    if any('2xko-rpc' in arg.lower() or 'main.py' in arg.lower() for arg in cmdline):
                        if proc.info['pid'] != current_pid:
                            count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return count > 0
