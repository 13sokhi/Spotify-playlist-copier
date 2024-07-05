class SpotifyTrack:
    def __init__(self, id: str, name: str, artist_ids: list[str]):
        self.id: str = id
        self.name: str = name
        self.artist_ids: list[str] = artist_ids

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_artist_ids(self) -> list[str]:
        return self.artist_ids

    def set_artist_ids(self, artist_ids: list):
        self.artist_ids = artist_ids