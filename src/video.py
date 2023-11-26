import json
import os

from googleapiclient.discovery import build


class Video:
    """Класс для видео с ютуб"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        try:
            self.video_id = video_id
            self.video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id
            ).execute()
            self.video_title: str = self.video_response['items'][0]['snippet']['title']
            self.url = f'https://www.youtube.com/watch?v={self.video_id}'
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            print('Invalid ID')
            self.video_response = Noneed
            self.video_title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_videos = self.youtube.playlistItems().list(
            playlistId=playlist_id,
            part='contentDetails',
            maxResults=50,
            ).execute()

