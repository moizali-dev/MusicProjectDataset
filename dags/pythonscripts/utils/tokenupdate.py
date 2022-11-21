import requests
import os
import base64
import dotenv
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class TokenUpdate:
    """Updates the token (since it automatically expires in 1 hr"""

    def __init__(self, client_id:str, client_secret:str, start_time) -> None:
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.start_time = datetime.now()

    def update_token(self, time_diff:int=15, firsttime:str="No"):
        """Updates the token

        Args:
            time_diff (int): time in minutes before the token gets updated
        """

        # URLS
        AUTH_URL = 'https://accounts.spotify.com/authorize'
        TOKEN_URL = 'https://accounts.spotify.com/api/token'

        client_creds = f'{self.client_id}:{self.client_secret}'

        # Make a request to the /authorize endpoint to get an authorization code
        auth_code = requests.get(AUTH_URL, {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': 'https://open.spotify.com/collection/playlists'
        })

        auth_header = base64.b64encode(client_creds.encode())
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {auth_header.decode()}',
        }

        payload = {
            'grant_type': 'client_credentials',
            'code': auth_code,
            'redirect_uri': 'https://open.spotify.com/collection/playlists',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        # Update the token first time
        if firsttime == "Yes":

            # Make a request to the /token endpoint to get an access token
            access_token_request = requests.post(url=TOKEN_URL, data=payload, headers=headers)

            # convert the response to JSON
            access_token_response_data = access_token_request.json()

            # save the access token
            os.environ["SPOTIFY_TOKEN"] = access_token_response_data["access_token"]
            dotenv.set_key(dotenv_file, "SPOTIFY_TOKEN", os.environ["SPOTIFY_TOKEN"])


        elif firsttime == "No" and ((datetime.now() - self.start_time).total_seconds() / 60 > time_diff):

            # Make a request to the /token endpoint to get an access token
            access_token_request = requests.post(url=TOKEN_URL, data=payload, headers=headers)

            # convert the response to JSON
            access_token_response_data = access_token_request.json()

            print(access_token_response_data)

            # save the access token
            os.environ["SPOTIFY_TOKEN"] = access_token_response_data["access_token"]
            dotenv.set_key(dotenv_file, "SPOTIFY_TOKEN", os.environ["SPOTIFY_TOKEN"])

            # update starttime
            self.start_time = datetime.now()