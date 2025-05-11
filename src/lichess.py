import requests

from constants import (INGAME, LICHESS_API_URL, LICHESS_DETAILS, IMAGE, OFFLINE, ONLINE, ONLINE_STATE, PLAYING)

class Lichess():

    def __init__(self, username):
        self.username = username
        self.user_data = {}

    # api request structure
    def fetch_api_data(self, url):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        return None
    
    # get data from lichess api
    def update_data(self):
        user_profile = self.fetch_api_data(f'{LICHESS_API_URL}/user/{self.username}')
        user_status = self.fetch_api_data(f'{LICHESS_API_URL}/users/status?ids={self.username}')[0] # response is nested in array

        if user_profile is None or user_status is None:
            return {}
        
        self.user_data = {**user_status, **user_profile} # both variable amounts of keys as lots of data retured

    # update rich presence info
    def display_playing(self, rpc):
        profile_url = self.user_data['url']

        buttons = [
            {
                'label': 'Profile',
                'url': profile_url,
            }
        ]

        rpc.update(details=LICHESS_DETAILS, state=INGAME, large_image=IMAGE, buttons=buttons)

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

    # set player status
    def get_player_status(self):
        if ('playing' in self.user_data):
            return PLAYING
        if ('online' in self.user_data and self.user_data['online']):
            return ONLINE
        return OFFLINE