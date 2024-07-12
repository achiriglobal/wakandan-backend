import requests
from pymongo import MongoClient

def fetch_eventbrite_events():
    api_key = 'HWO7JCFNVKCPCQTX65ZB'  # Your Eventbrite API key
    locations = ['Africa', 'USA', 'Europe']  # Example locations

    client = MongoClient('mongodb://localhost:27017/')
    db = client['wakandan_app']
    db.eventbrite_events.drop()  # Clear existing events

    for location in locations:
        url = f'https://www.eventbriteapi.com/v3/events/search/?q=African+diaspora&location.address={location}&token={api_key}'
        response = requests.get(url).json()

        for event in response['events']:
            if event['logo']:
                db.eventbrite_events.insert_one({
                    'name': event['name']['text'],
                    'url': event['url'],
                    'description': event['description']['text'],
                    'logo': event['logo']['url'],
                    'start': event['start']['local'],
                    'end': event['end']['local'],
                    'location': location
                })

if __name__ == "__main__":
    fetch_eventbrite_events()
