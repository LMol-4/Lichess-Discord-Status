import requests

from .constants import (LICHESS_API_URL, LICHESS_DETAILS, IMAGE, OFFLINE, ONLINE, INGAME, PLAYING, ONLINE_STATE)

class Lichess():

    def __init__(self, username, debugMode=0):
        self.username = username
        self.debugMode = debugMode
        self.user_data = {}

    # api request structure
    def fetch_api_data(self, url):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # raise exception for HTTP errors
            
            if self.debugMode: print("API data retrieved successfully.\n")
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if self.debugMode: print(f"API request failed: {e}")
            return None
    
    # get data from lichess api
    def update_data(self):
        try:
            user_profile = self.fetch_api_data(f'{LICHESS_API_URL}/user/{self.username}')
            status_response = self.fetch_api_data(f'{LICHESS_API_URL}/users/status?ids={self.username}')
            
            # check for empty responses
            if not user_profile or not status_response:
                if self.debugMode: print("Retrieved data is empty.\n")
                return
            
            user_status = status_response[0]  # response is nested in array
            
            self.user_data = {**user_status, **user_profile} # both variable amounts of keys as lots of data returned
            if self.debugMode: print("user_data populated.\n")

        except Exception as e:
            if self.debugMode: print(f"Error updating user data: {e}")
            self.user_data = {}  # reset data on error

    # update rich presence info
    def display_playing(self, rpc):
        # validate required data exists
        if 'url' not in self.user_data or 'playing' not in self.user_data:
            if self.debugMode: print("Cannot update playing status: missing required data.")
            return
            
        profile_url = self.user_data['url']
        watch_link = self.user_data['playing']

        buttons = [
            {
                'label': 'Spectate',
                'url': watch_link
            },
            {
                'label': 'Profile',
                'url': profile_url,
            }
        ]

        try:
            rpc.update(details=LICHESS_DETAILS, state=INGAME, large_image=IMAGE, buttons=buttons)
            if self.debugMode: print("RPC updated to display playing.")
        except Exception as e:
            if self.debugMode: print(f"Failed to update Discord RPC: {e}")

    # update rich presence info
    def display_online(self, rpc):
        # Validate required data exists
        if 'url' not in self.user_data:
            if self.debugMode: print("Cannot update online status: missing profile URL.")
            return
            
        profile_url = self.user_data['url']

        buttons = [
            {
                'label': 'Profile',
                'url': profile_url,
            }
        ]

        try:
            rpc.update(details=LICHESS_DETAILS, state=ONLINE_STATE, large_image=IMAGE, buttons=buttons)
            if self.debugMode: print("RPC updated to display online.")
        except Exception as e:
            if self.debugMode: print(f"Failed to update Discord RPC: {e}")

    # set player status
    def get_player_status(self):
        if not self.user_data:
            if self.debugMode: print("No user data available, considering offline.")
            return OFFLINE
            
        if ('playing' in self.user_data):
            if self.debugMode: print("Player status is playing.")
            return PLAYING
            
        if ('online' in self.user_data and self.user_data['online']):
            if self.debugMode: print("Player status is online.")
            return ONLINE
            
        if self.debugMode: print("Player status is offline.")
        return OFFLINE