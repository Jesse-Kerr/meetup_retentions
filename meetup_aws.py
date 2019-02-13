from pymongo import MongoClient
import numpy as np
import requests
import json
import warnings
warnings.filterwarnings('ignore')
key = open('api.txt', 'r').read()

client = MongoClient('localhost', 27017)
db = client.meet_up
collection = db.groups
events_coll = db.events

print('hello')
def get_all_events(collection):
    urlnames = [entry['urlname'] for entry in collection.find()]
    for urlname in urlnames[100000:]:
        # First, we need the total number of events for the group
        req = requests.get('https://api.meetup.com/{}/events?\
                            key={}&status=past&page=200&desc=true'.format(urlname, key))
        number_of_events = int(req.headers['X-Total-Count'])
        # Only deal with groups with no events
        if number_of_events != 0:
        # Insert the 200, then get the date of the last one.         
            while number_of_events > 200:
                json_data = json.loads(req.text)
                events_coll.insert_many(json_data)
                last_tmstp = "{}T{}".format(json_data[-1]['local_date'],json_data[-1]['local_time'])            
                req = requests.get('https://api.meetup.com/{}/events?\
                                key={}&status=past&page=200&desc=true&no_later_than={}'.format(urlname, key, last_tmstp))
                number_of_events -= 200
            # If less than 200, insert
            json_data = json.loads(req.text)
            events_coll.insert_many(json_data)
            print('Inserted {} into db.events!'.format(urlname))

get_all_events(collection)
