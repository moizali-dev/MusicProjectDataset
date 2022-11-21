class Track:
    """ Track represents a piece of music on Spotify"""

    def __init__(self, name : str, id : int , artist: str) -> None:
        """
        :param name (str) : name of the track
        :param id (int) : Spotify track id
        :param artist (str) : name of the artist
        """

        self.name = name
        self.id = id
        self.artist = artist


    def create_spotify_url(self):
        return f"spotify:track:{self.id}"

    def __str__(self) -> str:
        return f"{self.name} by {self.artist}"
