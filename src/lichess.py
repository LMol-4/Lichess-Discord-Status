import requests

from .constants import (INGAME, LICHESS_API_URL, LICHESS_DETAILS, IMAGE, OFFLINE, ONLINE, ONLINE_STATE, PLAYING)

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

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            if self.debugMode: print("API data retrieved succesfully.\n")
            return response.json()

        return None
    
    # get data from lichess api
    def update_data(self):
        user_profile = self.fetch_api_data(f'{LICHESS_API_URL}/user/{self.username}')
        user_status = self.fetch_api_data(f'{LICHESS_API_URL}/users/status?ids={self.username}')[0] # response is nested in array

        if user_profile is None or user_status is None:
            if self.debugMode: print("Retrieved data is empty.\n")
            return {}
        
        self.user_data = {**user_status, **user_profile} # both variable amounts of keys as lots of data retured
        if self.debugMode: print("user_data populated.\n")

    # update rich presence info
    def display_playing(self, rpc):
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

        rpc.update(details=LICHESS_DETAILS, state=INGAME, large_image=IMAGE, buttons=buttons)
        if self.debugMode: print("RPC updated to display playing.")

    # update rich presence info
    def display_online(self, rpc):
        profile_url = self.user_data['url']

        buttons = [
            {
                'label': 'Profile',
                'url': profile_url,
            }
        ]

        rpc.update(details=LICHESS_DETAILS, state=ONLINE_STATE, large_image=IMAGE, buttons=buttons)
        if self.debugMode: print("RPC updated to display online.")

    # set player status
    def get_player_status(self):
        if ('playing' in self.user_data):
            if self.debugMode: print("Player status is playing.")
            return PLAYING
        if ('online' in self.user_data and self.user_data['online']):
            if self.debugMode: print("Player status is online.")
            return ONLINE
        if self.debugMode: print("Player status is offline.")
        return OFFLINE