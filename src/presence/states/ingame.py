from ...config.app_config import Config

def presence(rpc, game_running=False, elapsed_time=None, nickname=None, **kwargs):
    show_elapsed = Config.get_value("show_elapsed_time")
    
    small_image = "game_icon"
    small_text = "In Fight"
    details = "2XKO - 2v2 Tag Team"
    
    if nickname:
        small_image = "riotgames-2xko"
        small_text = nickname
    
    update_args = {
        "state": "In Game",
        "details": details,
        "large_image": "game_icon",
        "large_text": "2XKO by Riot Games",
        "small_image": small_image,
        "small_text": small_text
    }
    
    if show_elapsed and elapsed_time:
        update_args["start"] = elapsed_time
    
    rpc.update(**update_args)