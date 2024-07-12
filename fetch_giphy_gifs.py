import requests
from pymongo import MongoClient

def fetch_giphy_gifs():
    api_key = '5muKOG2tFxYco1KeM4TiGr942iXM2pCM'
    url = f'http://api.giphy.com/v1/gifs/search?q=black+african+culture&api_key={api_key}&limit=10'
    response = requests.get(url).json()
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wakandan_app']

    db.giphy_gifs.drop()  # Clear existing gifs

    for gif in response['data']:
        db.giphy_gifs.insert_one({
            'url': gif['images']['downsized_large']['url'],
            'title': gif['title']
        })

if __name__ == "__main__":
    fetch_giphy_gifs()
