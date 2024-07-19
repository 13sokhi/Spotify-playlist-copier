import os
import config
import SpotifyAuthorization as auth
import SpotifyDataAccess as sp_access
import YouTubeDataAccess as yt_access
import YouTubeDataUpdate as yt_update
import TrackSearchAndDownload as downloader
from SpotifyPlaylist import SpotifyPlaylist
from SpotifyToken import SpotifyToken
from SpotifyTrack import SpotifyTrack
from YouTubePlaylist import YouTubePlaylist
import time
import json


# Global variables
token = None
channel_id = ''

# Functions to get the spotify access token and YouTube ChannelId
def get_spotify_access_token() -> SpotifyToken:
    data = None
    if os.path.exists('spotify_token.json'):
        with open('spotify_token.json', 'r') as in_file:
            data = json.loads(in_file.read()) # getting the saved string and converting it into dictionary
            token = SpotifyToken(access_token=data['access_token'], refresh_token=data['refresh_token'], expires_in=data['expires_in'])

    if not data or (time.time() > int(data['expires_in'])):
        if not data:
            authorization_code = auth.get_authorization_code(client_id=config.spotify_client_id, redirect_uri=config.spotify_redirect_uri)
            token = auth.get_token(client_id=config.spotify_client_id, client_secret=config.spotify_client_secret, authorization_code=authorization_code, redirect_uri=config.spotify_redirect_uri)
        elif time.time() > int(data['expires_at']):
            token = auth.refresh_token(client_id=config.spotify_client_id, client_secret=config.spotify_client_secret, refresh_token=data['refresh_token'])

        json_data = '{' + f'"access_token": "{token.get_access_token()}", "refresh_token": "{token.get_refresh_token()}", "expires_in": "{token.expires_in}", "expires_at": "{(round(time.time()) + int(token.get_expires_in()))}"' + '}'
        with open('spotify_token.json', 'w') as out_file:
            out_file.write(json_data)

    return token

def get_channel_id() -> str:
    channel_id = input('Enter YouTube ChannelID (settings -> Advanced settings): ')
    return channel_id

# basic functions to retrieve data or perform required actions
def set_spotify_token():
    global token
    token = get_spotify_access_token()

def set_channel_id():
    global channel_id
    channel_id = get_channel_id()

def get_spotify_playlists() -> list[SpotifyPlaylist]:
    user_id = sp_access.get_user_id(token)
    playlists_json = sp_access.get_playlists_json(user_id=user_id, token=token)
    spotify_playlists = sp_access.get_spotify_playlists(playlist_json=playlists_json)
    return spotify_playlists

def get_youtube_playlists(channel_id: str) -> list[YouTubePlaylist]:
    youtube_playlists_json = yt_access.get_playlists_json(channel_id, config.youtube_client_secret_json_path)
    youtube_playlists = yt_access.get_youtube_playlists(youtube_playlists_json)
    return youtube_playlists

def get_spotify_tracks(playlist: SpotifyPlaylist) -> list[SpotifyTrack]:
    playlist_item_json = sp_access.get_playlist_items_json(playlist=playlist, token=token)
    spotify_tracks = sp_access.get_spotify_tracks(playlist_item_json)
    return spotify_tracks

def get_youtube_playlist_items(playlist: YouTubePlaylist):
    playlist_items_json = yt_access.get_playlist_items_json(playlist, config.youtube_client_secret_json_path)
    youtube_playlist_items = yt_access.get_youtube_playlist_items(playlist_items_json)
    return youtube_playlist_items

def download_spotify_playlist(playlist: SpotifyPlaylist, output_path: str):
    if not os.path.exists(output_path):
        raise Exception("Selected path does NOT exist!")
    if not os.path.isdir(output_path):
        raise Exception('Path can ONLY be a directory!')

    spotify_playlist_tracks = get_spotify_tracks(playlist)
    new_playlist_path = os.path.join(output_path, playlist.get_name())
    os.mkdir(new_playlist_path)
    for spotify_track in spotify_playlist_tracks:
        video_id = downloader.get_video_id_of_spotify_track(spotify_track)
        downloader.download_video(downloader.get_video_download_link(video_id), new_playlist_path)
    print(f'"{playlist.get_name()}" downloaded at {new_playlist_path}')

def download_youtube_playlist(playlist: YouTubePlaylist, output_path: str):
    if not os.path.exists(output_path):
        raise Exception("Selected path does NOT exist!")
    if not os.path.isdir(output_path):
        raise Exception('Path can ONLY be a directory!')

    youtube_videos = get_youtube_playlist_items(playlist)
    new_playlist_path = os.path.join(output_path, playlist.get_title())
    os.mkdir(new_playlist_path)
    for video in youtube_videos:
        video_id = video.get_video_id()
        print(f'Downloading {video.get_title()}')
        downloader.download_video(downloader.get_video_download_link(video_id), new_playlist_path)
    print(f'"{playlist.get_title()}" downloaded at {new_playlist_path}')

def copy_spotify_playlist_to_youtube(playlist: SpotifyPlaylist):
    youtube_playlists = get_youtube_playlists(channel_id)
    for youtube_playlist in youtube_playlists: # if playlist with same name exists, we delete it
        if (youtube_playlist.get_title() == playlist.get_name()):
            yt_update.delete_playlist(playlist=youtube_playlist, oauth_json_path=config.youtube_client_secret_json_path)
    created_playlist = yt_update.create_playlist(oauth_json_path=config.youtube_client_secret_json_path, title=playlist.get_name(), description=f'{playlist.get_name()} copied from Spotify')
    spotify_tracks = get_spotify_tracks(playlist)
    print(f'\n{playlist.get_name()}')
    for i in range(len(spotify_tracks)):
        spotify_track = spotify_tracks[i]
        video_id = downloader.get_video_id_of_spotify_track(spotify_track)
        print(f'\t{spotify_track.get_name()} copied')
        yt_update.add_playlist_item(YouTubePlaylist(created_playlist.get_id(), created_playlist.get_title(), i), video_id, config.youtube_api_key)
        time.sleep(0.2)
    print(f'\nPlaylist "{playlist.get_name()}" copied!')

# methods that main loop will call:
def view_spotify_playlists():
    spotify_playlists = get_spotify_playlists()
    print('\nAll Spotify Playlists')
    for i, spotify_playlist in enumerate(spotify_playlists, 1):
        print(f'\t{i}. {spotify_playlist.get_name()}')

def view_youtube_playlists():
    youtube_playlists = get_youtube_playlists(channel_id)
    print('\nAll YouTube Playlists')
    for i, youtube_playlist in enumerate(youtube_playlists, 1):
        print(f'\t{i}. {youtube_playlist.get_title()}')

def view_spotify_tracks():
    spotify_playlists = get_spotify_playlists()
    print('\n' + '-'*10 + 'Tracks in Spotify Playlists' + '-'*10)
    for spotify_playlist in spotify_playlists:
        spotify_tracks = get_spotify_tracks(spotify_playlist)
        print('\n' + spotify_playlist.get_name())
        for spotify_track in spotify_tracks:
            print('\t' + spotify_track.get_name())

def view_youtube_videos():
    youtube_playlists = get_youtube_playlists(channel_id)
    print('\n' + '-'*10 + 'Videos in YouTube Playlists' + '-'*10)
    for youtube_playlist in youtube_playlists:
        youtube_playlist_items = get_youtube_playlist_items(youtube_playlist)
        print('\n' + youtube_playlist.get_title())
        for youtube_playlist_item in youtube_playlist_items:
            print('\t' + youtube_playlist_item.get_title())

def download_all_spotify_playlists():
    output_path = input("Enter path to download all Spotify Playlists: ")
    spotify_playlists = get_spotify_playlists()
    for spotify_playlist in spotify_playlists:
        download_spotify_playlist(spotify_playlist, output_path)

def download_all_youtube_playlists():
    output_path = input("Enter path to download all YouTube Playlists: ")
    youtube_playlists = get_youtube_playlists(channel_id)
    for youtube_playlist in youtube_playlists:
        download_youtube_playlist(youtube_playlist, output_path)

def download_specific_spotify_playlist():
    view_spotify_playlists()
    spotify_playlists = get_spotify_playlists()
    playlist_num = int(input('\nPress Playlist number to download it: '))
    if playlist_num>len(spotify_playlists) or playlist_num<1:
        raise Exception("Requested playlist does NOT exist!")
    output_path = input("Enter path to download Spotify Playlist: ")
    download_spotify_playlist(spotify_playlists[playlist_num-1], output_path)

def download_specific_youtube_playlist():
    view_youtube_playlists()
    youtube_playlists = get_youtube_playlists(channel_id)
    playlist_num = int(input('\nPress Playlist number to download it: '))
    if playlist_num>len(youtube_playlists):
        raise Exception(f"{playlist_num} Playlist does NOT exist!")
    output_path = input("Enter path to download Spotify Playlist: ")
    download_youtube_playlist(youtube_playlists[playlist_num-1], output_path)

def copy_all_spotify_playlists():
    spotify_playlists = get_spotify_playlists()
    for spotify_playlist in spotify_playlists:
        copy_spotify_playlist_to_youtube(spotify_playlist)

def copy_specific_spotify_playlist():
    spotify_playlists = get_spotify_playlists()
    view_spotify_playlists()
    playlist_num = int(input('Enter playlist number to copy: '))
    if playlist_num<1 or playlist_num>len(spotify_playlists):
        raise Exception(f'{playlist_num} playlist does not exist!')
    copy_spotify_playlist_to_youtube(spotify_playlists[playlist_num - 1])

def start_program():
    run_main_loop()

def run_main_loop():
    while True:
        inp = input('Change current user/ re-authenticate (y/n): ').lower()
        match inp:
            case 'y':
                if os.path.exists('token.json'):
                    os.remove('token.json')
                if os.path.exists('spotify_token.json'):
                    os.remove('spotify_token.json')
                break
            case 'n':
                break
            case _:
                print('Invalid Input')

    set_spotify_token()
    set_channel_id()

    while True:
        print('\n' + '-'*50)
        print('0  -> Exit')
        print('1  -> view Spotify Playlists')
        print('2  -> view YouTube Playlists')
        print('3  -> view Spotify Tracks')
        print('4  -> view YouTube Videos')
        print('5  -> copy all Spotify Playlists in YouTube')
        print('6  -> copy Spotify Playlist in YouTube')
        print('7  -> download all Spotify Playlists')
        print('8  -> download all YouTube Playlists')
        print('9  -> download Spotify Playlist')
        print('10 -> download YouTube Playlist')

        try:
            selection = int(input('Selection: '))

            match selection:
                case 0:
                    break
                case 1:
                    view_spotify_playlists()
                case 2:
                    view_youtube_playlists()
                case 3:
                    view_spotify_tracks()
                case 4:
                    view_youtube_videos()
                case 5:
                    copy_all_spotify_playlists()
                case 6:
                    copy_specific_spotify_playlist()
                case 7:
                    download_all_spotify_playlists()
                case 8:
                    download_all_youtube_playlists()
                case 9:
                    download_specific_spotify_playlist()
                case 10:
                    download_specific_youtube_playlist()
                case _:
                    print('Invalid Selection!')
        except ZeroDivisionError:
            print('Invalid Input Format!')
        except Exception as e:
            print(e)