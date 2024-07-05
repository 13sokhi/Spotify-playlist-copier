class SpotifyPlaylist:
    def __init__(self, id: str, name: str, size: int):
        self.id: str = id
        self.name: str = name
        self.size: int = size

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_size(self) -> str:
        return self.size

    def set_size(self):
        return self.size