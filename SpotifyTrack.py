class SpotifyTrack:
    def __init__(self, id: str, name: str, artists: list[str]):
        self.id: str = id
        self.name: str = name
        self.artists: list[str] = artists

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_artists(self) -> list[str]:
        return self.artists

    def set_artist_ids(self, artists: list):
        self.artists = artists
