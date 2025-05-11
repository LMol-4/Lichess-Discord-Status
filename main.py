import time
from pypresence import Presence
import json

from src.lichess import Lichess
from src.constants import (DISCORD_RPC_INTERVAL, DISCORD_APP_ID, CONFIG_FILE_PATH, ONLINE, PLAYING)

def main():
    # parse config file for username
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error config not found. Check path in constants.py")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file: {e}")
    
    # set up lichess api integration
    lichess = Lichess(config.get("lichessUsername"))

    # connect to discord api
    rpc = Presence(DISCORD_APP_ID)
    rpc.connect()

    while True:
        # reset for each loop
        status_updated = False

        # update data and status
        lichess.update_data()
        player_status = lichess.get_player_status()

        if player_status is PLAYING:
            lichess.display_playing(rpc)
            updated = True

        if player_status is ONLINE:
            lichess.display_online(rpc)
            updated = True

        # if you have quit lichess
        if not status_updated:
            rpc.clear()

        time.sleep(DISCORD_RPC_INTERVAL)

if __name__ == '__main__':
    main()