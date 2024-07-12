from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import schedule
import time
from fetch_rss_feeds import fetch_and_store_feeds
from fetch_youtube_videos import fetch_youtube_videos
from fetch_giphy_gifs import fetch_giphy_gifs

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['wakandan_app']

@app.route('/api/rss_feeds', methods=['GET'])
def get_rss_feeds():
    feeds = list(db.rss_feeds.find({}, {'_id': 0}))
    return jsonify(feeds)

@app.route('/api/youtube_videos', methods=['GET'])
def get_youtube_videos():
    videos = list(db.youtube_videos.find({}, {'_id': 0}))
    return jsonify(videos)

@app.route('/api/giphy_gifs', methods=['GET'])
def get_giphy_gifs():
    gifs = list(db.giphy_gifs.find({}, {'_id': 0}))
    return jsonify(gifs)

@app.route('/api/events', methods=['GET'])
def get_events():
    events = list(db.events.find({}, {'_id': 0}))
    return jsonify(events)

def job():
    fetch_and_store_feeds()
    fetch_youtube_videos()
    fetch_giphy_gifs()

schedule.every(15).minutes.do(job)

if __name__ == '__main__':
    app.run(debug=True)

while True:
    schedule.run_pending()
    time.sleep(1)
