import json
import requests
import os
import time

from typing import List

from pythonscripts.utils.track import Track
from pythonscripts.utils.playlist import Playlist
from pythonscripts.utils.categories import Categories

class SpotifyClient:
    """Performs operation using the Spotify API"""

    def __init__(self, authorization_token:str, user_id:str) -> None:
        """_summary_

        Args:
            authorization_token (str): Spotify API token
            user_id (str): Spotify user id
        """

        self._authorization_token = authorization_token
        self._user_id = user_id

    def get_last_played_tracks(self, limit=10):
        """Get the last n tracks played by a user
        :param limit (int): Number of tracks to get. Should be <= 50
        :return tracks (list of Track): List of last played tracks
        """
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for
                  track in response_json["items"]]
        return tracks

    def get_playlist_tracks(self, playlist_id:str):
        """Returns a list of tracks

        Args:
            playlist_id (str): _description_
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks" 
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for
                  track in response_json["items"]]
        return tracks

    
    def get_track_features(self, track_id:str):
        """Get the features of the track

        Args:
            id (str): _description_
        """
        url = f"https://api.spotify.com/v1/audio-features/{track_id}" 
        response = self._place_get_api_request(url)
        response_json = response.json()
        
        return response_json

    def get_track_recommendations(self, seed_tracks, limit=50):
        """Get a list of recommended tracks starting from a number of seed tracks.
        :param seed_tracks (list of Track): Reference tracks to get recommendations. Should be 5 or less.
        :param limit (int): Number of recommended tracks to be returned
        :return tracks (list of Track): List of recommended tracks
        """
        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                  track in response_json["tracks"]]
        return tracks

    def create_playlist(self, name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        data = json.dumps({
            "name": name,
            "description": "Recommended songs",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()

        # create playlist
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def populate_playlist(self, playlist, tracks):
        """Add tracks to a playlist.
        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        return response_json

    def get_user_info(self, user_id):

        url = f"https://api.spotify.com/v1/users/{user_id}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        print(response_json)


    def get_user_playlists(self, user_id):

        url = f"https://api.spotify.com/v1/users/{user_id}/playlists?offset=0&limit=50"
        response = self._place_get_api_request(url)
        response_json = response.json()
        with open('data.json', 'w') as f:
            json.dump(response_json, f)
        print(response_json)

    def get_user_saved_tracks(self, user_id):

        url = f"https://api.spotify.com/v1/users/{user_id}/albums"
        response = self._place_get_api_request(url)
        response_json = response.json()
        with open('data.json', 'w') as f:
            json.dump(response_json, f)
        print(response_json)

    def get_owner_id(self, user_id):
        url = f"https://api.spotify.com/v1/{user_id}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        print(response_json)

    def get_categories(self):
        url = f"https://api.spotify.com/v1/browse/categories?limit=50"
        response = self._place_get_api_request(url)
        response_json = response.json()
        categories = [Categories(categories["name"], categories["id"]) for
                  categories in response_json["categories"]["items"]]
        
        return categories

    def get_categories_playlist(self, category_id, limit = 50):
        url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists?limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        playlists = [Playlist(playlist["name"], playlist["id"], playlist["tracks"]["total"]) for
                  playlist in response_json["playlists"]["items"]]
        return playlists

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )

        if response.status_code == 429:
            print(f"Sleeping for {response.headers['Retry-After']} seconds")
            time.sleep(int(response.headers['Retry-After']))

        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response


    def _set_authorization_token(self, token):

        self._authorization_token = token

    