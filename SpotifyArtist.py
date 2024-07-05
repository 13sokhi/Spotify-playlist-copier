class SpotifyArtist:
    def __init__(self, id: str, name: str):
        self.id: str = id
        self.name: str = name

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name