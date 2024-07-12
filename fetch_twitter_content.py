import tweepy
from pymongo import MongoClient

def fetch_and_store_tweets():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wakandan_app']

    consumer_key = 'your_consumer_key'
    consumer_secret = 'your_consumer_secret'
    access_token = 'your_access_token'
    access_token_secret = 'your_access_token_secret'

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    db.twitter_posts.drop()  # Clear existing posts

    for tweet in tweepy.Cursor(api.search_tweets, q='African culture OR Black culture', lang='en').items(10):
        db.twitter_posts.insert_one({
            'text': tweet.text,
            'user': tweet.user.screen_name,
            'created_at': tweet.created_at
        })

if __name__ == "__main__":
    fetch_and_store_tweets()
