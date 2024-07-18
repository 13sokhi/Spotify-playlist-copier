class YouTubePlaylistItem:
    def __init__(self, title: str, playlist_id: str, video_id: str):
        self.title = title
        self.playlist_id: str = playlist_id
        self.video_id: str = video_id

    def get_title(self) -> str:
        return self.title

    def set_title(self, title: str):
        self.title = title

    def get_playlist_id(self) -> str:
        return self.playlist_id

    def set_playlist_id(self, playlist_id: str):
        self.playlist_id = playlist_id

    def get_video_id(self) -> str:
        return self.video_id

    def set_video_id(self, video_id: str):
        self.video_id = video_id