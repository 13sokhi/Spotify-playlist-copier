import config
from YouTubePlaylistItem import YouTubePlaylistItem
from YouTubePlaylist import YouTubePlaylist
import googleapiclient.discovery
import googleapiclient.errors
import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def create_playlist(oauth_json_path: str, title: str = 'Default title', description: str = 'Default description') -> YouTubePlaylist:
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        # Define the scope
        SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        # The path to your client_secret.json file
        CLIENT_SECRETS_FILE = oauth_json_path

        # Check if we have token.json to store the user's access and refresh tokens
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server()

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        # Create the YouTube API client
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": [
                        "sample playlist",
                        "API call"
                    ],
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        )
        response = request.execute()
        playlist_id = response['id']
        playlist_title = response['snippet']['title']
        return YouTubePlaylist(id=playlist_id, title=playlist_title, size=0)


def delete_playlist(playlist: YouTubePlaylist, oauth_json_path: str) -> None:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Define the scope
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # The path to your client_secret.json file
    CLIENT_SECRETS_FILE = oauth_json_path

    # Check if we have token.json to store the user's access and refresh tokens
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    request = youtube.playlists().delete(
        id=playlist.get_id()
    )
    request.execute()


def add_playlist_item(playlist: YouTubePlaylist, video_id: str, api_key: str) -> None:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Define the scope
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # The path to your client_secret.json file
    CLIENT_SECRETS_FILE = config.youtube_client_secret_json_path

    # Check if we have token.json to store the user's access and refresh tokens
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    api_service_name = "youtube"
    api_version = "v3"
    developer_key = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist.get_id(),
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    for i in range(3): # will try 3 times to add the video into playlist
        try:
            response = request.execute() # response has added video name in ['snippet']['title']
            return response
        except googleapiclient.errors.HttpError as e:
            print('\tRe-trying copying...')
            continue

