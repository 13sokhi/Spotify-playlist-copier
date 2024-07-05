from config import youtube_client_secret_json_path

from YouTubePlaylistItem import YouTubePlaylistItem
from YouTubePlaylist import YouTubePlaylist

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def get_playlists_json(channel_id: str, oauth_json_path: str) -> list[str]:
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = oauth_json_path

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=100
    )
    response = request.execute()
    return list([response])


def get_youtube_playlists(playlist_json: str) -> list[YouTubePlaylist]:
    youtube_playlists: list[YouTubePlaylist] = list([])
    playlists = playlist_json['items']

    for playlist in playlists:
        playlist_id = playlist['id']
        playlist_title = playlist['snippet']['title']
        playlist_size = playlist['contentDetails']['itemCount']
        youtube_playlists.append(YouTubePlaylist(playlist_id, playlist_title, playlist_size))

    return youtube_playlists


def get_playlist_items_json(playlist: YouTubePlaylist, oauth_json_path: str) -> str:
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = oauth_json_path

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=1000,
        playlistId=playlist.get_id()
    )
    response = request.execute()
    return response


def get_youtube_playlist_items(playlist_items_json: str) -> list[YouTubePlaylistItem]:
    youtube_playlist_items: list[YouTubePlaylistItem] = list([])
    items = playlist_items_json['items']

    for item in items:
        id = item['id']
        playlist_id = item['playlistId']
        video_id = item['resourceId']['videoId']
        youtube_playlist_items.append(YouTubePlaylistItem(id, playlist_id, video_id))

    return youtube_playlist_items