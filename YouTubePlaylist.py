class YouTubePlaylist:
    def __init__(self, id: str, title: str, size: int):
        self.id: str = id
        self.title: str = title
        self.size: int = size

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_title(self) -> str:
        return self.title

    def set_title(self, title: str):
        self.title = title

    def get_size(self) -> int:
        return self.size

    def set_size(self, size: int):
        self.size = size
