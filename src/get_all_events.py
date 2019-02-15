from pymongo import MongoClient
import numpy as np
import requests
import json
import warnings
warnings.filterwarnings('ignore')
key = open('src/api.txt', 'r').read()

f = open('groups_not_done.txt', 'r')
groups_not_done = f.read().replace("'", '').replace(" ", '').split(',')
f.close()

client = MongoClient('localhost', 27017)
db = client['meet-ups']
events_coll = db.events

def get_all_events(collection):
        
    ''' 
    Download the events for a particular group. If there are more than 200 events, split the request by the dates of 
    event. Save into meetups.events
    '''

    for urlname in groups_not_done:
        try:
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
        except:
            print("Something went wrong!")