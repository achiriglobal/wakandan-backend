import feedparser
from pymongo import MongoClient

def fetch_and_store_feeds():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wakandan_app']
    rss_feeds = [
        'https://news.ycombinator.com/rss',
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        # Add more RSS feed URLs here
    ]

    db.rss_feeds.drop()  # Clear existing feeds

    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            media_url = None
            if 'media_content' in entry:
                media_url = entry.media_content[0]['url']
            elif 'media_thumbnail' in entry:
                media_url = entry.media_thumbnail[0]['url']
            db.rss_feeds.insert_one({
                'title': entry.title,
                'link': entry.link,
                'description': entry.summary,
                'media': media_url
            })

if __name__ == "__main__":
    fetch_and_store_feeds()
