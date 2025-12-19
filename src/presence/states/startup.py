from ...config.app_config import Config

def presence(rpc, game_running=False, nickname=None, **kwargs):
    texts = Config.get_value("texts")
    
    small_image = None
    small_text = None
    
    if nickname:
        small_image = "riotgames-2xko"
        small_text = nickname
        
    rpc.update(
        state=texts.get("loading", "Loading..."),
        large_image="game_icon",
        large_text="2XKO Rich Presence",
        small_image=small_image,
        small_text=small_text
    )