from SpotifyTrack import SpotifyTrack
from config import base_youtube_search_url
import requests
# import pytube
import os
import yt_dlp


def get_video_id_of_spotify_track(track: SpotifyTrack) -> str:
    url = ''
    track_name = track.get_name().replace('&', 'and') # '&' has special meaning in search URL
    url += base_youtube_search_url + track_name.replace(' ', '+') + '+by+'
    for i in range(len(track.get_artists())):
        # print(track.get_artists()[i])
        artist_name = track.get_artists()[i].replace('&', 'and')
        url += f'{artist_name.replace(" ", "+")}' if (i + 1) == len(track.get_artists()) else f'{artist_name.replace(" ", "+")}+and+'
    # print(url)
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
    # following code not working now due to some bug in pytube library
    # yt = pytube.YouTube(video_url)
    # audio_stream = yt.streams.filter(only_audio=True)
    # file_path = audio_stream.download(output_path=output_path)

    # The following code will be used to download until pytube is not fixed
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,  # This suppresses output
        'no_warnings': True,  # This suppresses warning messages
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
        except yt_dlp.utils.DownloadError as e:
            pass

