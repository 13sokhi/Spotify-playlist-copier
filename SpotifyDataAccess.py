from SpotifyTrack import SpotifyTrack
from SpotifyPlaylist import SpotifyPlaylist
from SpotifyToken import SpotifyToken
from config import user_profile_endpoint
import requests

def get_user_id(token: SpotifyToken) -> str:
    access_token = token.get_access_token()
    header = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url="https://api.spotify.com/v1/me", headers=header) #403 error here
    user_id = response.json()['id']
    return user_id

def get_playlists_json(user_id: str, token: SpotifyToken) -> str:
    user_playlists_endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    access_token = token.get_access_token()
    header = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url=user_playlists_endpoint, headers=header).json()
    return response

def get_playlist_items_json(playlist: SpotifyPlaylist, token: SpotifyToken) -> str:
    playlist_id: str = playlist.get_id()
    access_token = token.get_access_token()
    playlist_item_endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    header = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url=playlist_item_endpoint, headers=header).json()
    return response

def get_spotify_playlists(playlist_json: str) -> list[SpotifyPlaylist]:
    spotify_playlists: list[SpotifyPlaylist] = list([])
    playlists = playlist_json['items']

    if len(playlists) == 0:
        raise Exception('You have NO Spotify Playlists!')

    for playlist in playlists:
        id: str = playlist['id']
        name: str = playlist['name']
        size: int = playlist['tracks']['total']
        spotify_playlists.append(SpotifyPlaylist(id=id, name=name, size=size))
    return spotify_playlists

def get_spotify_tracks(playlist_item_json: str) -> list[SpotifyTrack]:
    spotify_tracks: list[SpotifyTrack] = list([])
    playlist_items = playlist_item_json['items']

    if len(playlist_items) == 0:
        raise Exception('Playlist has NO Tracks!')

    for playlist_item in playlist_items:
        id: str = playlist_item['track']['id']
        name: str = playlist_item['track']['name']
        artists = playlist_item['track']['artists']
        artist_names: list[str] = list([])
        for artist in artists:
            artist_names.append(artist['name'])
        spotify_tracks.append(SpotifyTrack(id=id, name=name, artists=artist_names))
    return spotify_tracks