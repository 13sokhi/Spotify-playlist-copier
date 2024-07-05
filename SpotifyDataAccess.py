from SpotifyArtist import SpotifyArtist
from SpotifyTrack import SpotifyTrack
from SpotifyPlaylist import SpotifyPlaylist
from SpotifyToken import SpotifyToken
from config import user_profile_endpoint
import requests

def get_user_id(access_token: SpotifyToken) -> str:
    header = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url=user_profile_endpoint, headers=header)
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

def get_artists_json(track: SpotifyTrack, token: SpotifyToken) -> list[str]:
    all_artist_json: list[str] = list([])
    artist_ids = track.get_artist_ids()
    access_token = token.get_access_token()

    for id in artist_ids:
        artist_endpoint = f'https://api.spotify.com/v1/artists/{id}'
        header = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url=artist_endpoint, headers=header).json()
        all_artist_json.append(response)

def get_spotify_playlists(playlist_json: str) -> list[SpotifyPlaylist]:
    spotify_playlists: list[SpotifyPlaylist] = list([])
    playlists = playlist_json['items']

    for playlist in playlists:
        id: str = playlist['id']
        name: str = playlist['name']
        size: int = playlist['tracks']['total']
        spotify_playlists.append(SpotifyPlaylist(id=id, name=name, size=size))
    return spotify_playlists

def get_spotify_tracks(playlist_item_json: str) -> list[SpotifyTrack]:
    spotify_tracks: list[SpotifyTrack] = list([])
    playlist_items = playlist_item_json['items']
    for playlist_item in playlist_items:
        id: str = playlist_item['track']['id']
        name: str = playlist_item['track']['name']
        artist_ids: list[str] = list([])
        for artist in playlist_items['track']['artists']:
            artist_ids.append(artist)['id']
        spotify_tracks.append(SpotifyTrack(id=id, name=name, artist_ids=artist_ids))
    return spotify_tracks

def get_spotify_artists(all_artists_json: list[str]) -> list[SpotifyArtist]:
    spotify_artists: list[SpotifyArtist] = list([])
    for artist_json in all_artists_json:
        id: str = artist_json['id']
        name: str = artist_json['name']
        spotify_artists.append(SpotifyArtist(id=id, name=name))
    return spotify_artists