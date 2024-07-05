class SpotifyToken:
    def __init__(self, access_token: str, expires_in: int, refresh_token: str):
        self.access_token: str = access_token
        self.expires_in: int = expires_in
        self.refresh_token: str = refresh_token

    def get_access_token(self):
        return self.access_token

    def set_access_token(self, access_token: str):
        self.access_token = access_token

    def get_expires_in(self):
        return self.expires_in

    def set_expires_in(self, expires_in: int):
        self.expires_in = expires_in

    def get_refresh_token(self):
        return self.refresh_token

    def set_refresh_token(self, refresh_token):
        self.refresh_token = refresh_token