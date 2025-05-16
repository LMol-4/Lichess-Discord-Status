import time
import sys
from pypresence import Presence
import json

from src.lichess import Lichess
from src.constants import (DISCORD_RPC_INTERVAL, DISCORD_APP_ID, CONFIG_FILE_PATH, ONLINE, PLAYING)

# get config from json
def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)
        print("Config loaded successfully.\n")
        return config
    except FileNotFoundError:
        print(f"Error: Config file not found at {CONFIG_FILE_PATH}. Check path in constants.py")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file: {e}")
        sys.exit(1)

# main loop
def main():
    print("\nLichess-Discord-Status by LMol-4\n")
    print("Loading config file....\n")

    # Parse config file
    config = load_config()
    
    # Get debug mode
    debug_mode = config.get("debugMode", False)

    # Set up lichess API integration
    lichess = Lichess(config.get("lichessUsername"), debug_mode)

    # Connect to Discord API with error handling
    try:
        rpc = Presence(DISCORD_APP_ID)
        rpc.connect()
        if debug_mode: 
            print("RPC set up successfully.")
    except Exception as e:
        print(f"Failed to connect to Discord: {e}")
        sys.exit(1)

    update_number = 0
    last_status = None  # Track last status -> avoid unnecessary updates

    while True:
        try:
            if debug_mode:
                update_number += 1
                print(f"Status refresh: {update_number}\n")

            # Update data
            lichess.update_data()
            current_status = lichess.get_player_status()
            
            # Update Discord status if change
            if current_status != last_status:
                if current_status == PLAYING:
                    lichess.display_playing(rpc)
                elif current_status == ONLINE:
                    lichess.display_online(rpc)
                else:
                    rpc.clear()
                
                last_status = current_status
                if debug_mode:
                    print(f"Status updated to: {current_status}")
            elif debug_mode:
                print("Status unchanged, skipping Discord update.")
                
            time.sleep(DISCORD_RPC_INTERVAL)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(DISCORD_RPC_INTERVAL)  # Keep trying even after errors

if __name__ == '__main__':
    main()