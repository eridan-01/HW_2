import json
import os
import datetime
import isodate

from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_info = self.youtube.playlists().list(id=playlist_id, part='contentDetails, snippet', ).execute()
        self.playlist_videos = self.youtube.playlistItems().list(
            playlistId=playlist_id,
            part='contentDetails, snippet',
            maxResults=50,
            ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(self.video_ids)
            ).execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        print(json.dumps(self.playlist_info, indent=2, ensure_ascii=False))
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration