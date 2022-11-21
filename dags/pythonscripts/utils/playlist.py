class Playlist:
    """ Playlist of a spotify"""

    def __init__(self, name:str, id:int, tracks: int) -> None:
        """Constructor

        Args:
            name (str): name of the playlist
            id (int): id of the playlist
            tracks (int) : number of tracks in playlist
        """
        self.name = name
        self.id = id
        self.tracks = tracks

    def __str__(self) -> str:
        return f"Playlist: {self.name}, ID: {self.id}"
