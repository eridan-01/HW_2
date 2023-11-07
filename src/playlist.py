import json
import os

from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_info = self.youtube.playlists().list(id=playlist_id, part='snippet', ).execute()
        self.playlist_video = self.youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=50,
            ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        print(json.dumps(self.playlist_info, indent=2, ensure_ascii=False))
