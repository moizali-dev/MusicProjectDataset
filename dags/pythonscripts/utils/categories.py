class Categories:
    """ Track represents a piece of music on Spotify"""

    def __init__(self, name : str, id : int) -> None:
        """
        :param name (str) : name of the track
        :param id (int) : Spotify track id
        :param artist (str) : name of the artist
        """

        self.name = name
        self.id = id

    def __str__(self) -> str:
        return f"{self.name} - {self.id}"
