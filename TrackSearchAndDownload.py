from SpotifyTrack import SpotifyTrack
from config import base_youtube_search_url
import requests
import pytube
import os


def get_video_id_of_spotify_track(track: SpotifyTrack) -> str:
    url = ''
    track_name = track.get_name().replace('&', 'and') # '&' has special meaning in search URL
    url += base_youtube_search_url + track_name.replace(' ', '+') + '+by+'
    for i in range(len(track.get_artists())):
        artist_name = track.get_artists()[i].replace('&', 'and')
        url += f'{artist_name.replace(" ", "+")}' if i - 1 == len(track.get_artists()) else f'{artist_name.replace(" ", "+")}+and+'
    print(url)
    response = requests.get(url=url).text # contains links for several resulted videos
    start_index = response.index('watch?v=') + 8 # selecting the 1st video
    end_index = start_index + 11
    video_id = response[start_index : end_index]
    return video_id

def get_video_download_link(video_id: str) -> str:
    return 'https://www.youtube.com/watch?v=' + video_id

def download_video(video_url: str, output_path: str):
    if not os.path.exists(output_path):
        raise Exception("Selected path does NOT exist!")
    if not os.path.isdir(output_path):
        raise Exception('Path can ONLY be a directory!')
    yt = pytube.YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True)[0]
    file_path = audio_stream.download(output_path=output_path)