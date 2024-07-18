from YouTubePlaylistItem import YouTubePlaylistItem
from YouTubePlaylist import YouTubePlaylist

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def verify_youtube_channel(channel_id: str, oauth_json_path: str) -> None:
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

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id="UC_x5XG1OV2P6uZZ5FSM9Ttw"
    )
    response = request.execute()
    if response['pageInfo']['totalResults'] == 0:
        raise Exception('Channel ID is invalid!')

def get_playlists_json(channel_id: str, oauth_json_path: str) -> str:
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = oauth_json_path

    # Define the scope
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # The path to your client_secret.json file

    # Check if we have token.json to store the user's access and refresh tokens
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=100
    )
    response = request.execute()
    return response


def get_youtube_playlists(playlist_json: str) -> list[YouTubePlaylist]:
    youtube_playlists: list[YouTubePlaylist] = list([])
    playlists = playlist_json['items']

    if len(playlists) == 0:
        raise Exception('No Playlists found!')

    for playlist in playlists:
        playlist_id = playlist['id']
        playlist_title = playlist['snippet']['title']
        playlist_size = playlist['contentDetails']['itemCount']
        youtube_playlists.append(YouTubePlaylist(playlist_id, playlist_title, int(playlist_size)))

    return youtube_playlists


def get_playlist_items_json(playlist: YouTubePlaylist, oauth_json_path: str) -> str:
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = oauth_json_path

    # Define the scope
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Check if we have token.json to store the user's access and refresh tokens
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

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

    if len(items) == 0:
        return youtube_playlist_items

    for item in items:
        title = item['snippet']['title']
        playlist_id = item['snippet']['playlistId']
        video_id = item['snippet']['resourceId']['videoId']
        youtube_playlist_items.append(YouTubePlaylistItem(title, playlist_id, video_id))

    return youtube_playlist_items