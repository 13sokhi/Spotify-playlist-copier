from YouTubePlaylistItem import YouTubePlaylistItem
from YouTubePlaylist import YouTubePlaylist
import googleapiclient.discovery
import os

def create_playlist(api_key: str, title: str = 'Default title', description: str = 'Default description') -> None:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    developer_key = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": [
                    "copied playlist"
                ],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    request.execute()


def delete_playlist(playlist: YouTubePlaylist, api_key: str) -> None:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    developer_key = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

    request = youtube.playlists().delete(
        id=playlist.get_id()
    )
    request.execute()


def add_playlist_item(playlist: YouTubePlaylist, item: YouTubePlaylistItem, api_key: str) -> None:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    developer_key = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist.get_id(),
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": item.get_video_id()
                }
            }
        }
    )
    request.execute()