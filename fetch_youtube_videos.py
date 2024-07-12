from googleapiclient.discovery import build
from pymongo import MongoClient

def fetch_youtube_videos():
    api_key = 'AIzaSyDZHdUQdoEyuAq-t4VPPTeSq9W8ZQ4TCwQ'
    youtube = build('youtube', 'v3', developerKey=api_key)
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wakandan_app']

    db.youtube_videos.drop()  # Clear existing videos

    request = youtube.search().list(
        q='Black culture African culture',
        part='snippet',
        maxResults=10,
        type='video'
    )
    response = request.execute()

    for item in response['items']:
        db.youtube_videos.insert_one({
            'videoId': item['id']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['high']['url']
        })

if __name__ == "__main__":
    fetch_youtube_videos()
