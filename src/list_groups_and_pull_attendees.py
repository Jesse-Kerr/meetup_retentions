from pymongo import MongoClient
import pandas as pd
import numpy as np
import requests
import json
import warnings
import time
from pprint import pprint
warnings.filterwarnings('ignore')
key = open('src/api.txt', 'r').read()

client = MongoClient()
db = client['meet-ups']
collection = db.groups
events_coll = db.events_two
attendees = db.attendees
categories = db.category_per_group

def create_list_of_groups_per_category():
    # find distinct categories in groups_per_category
    categories = db['category_per_group'].distinct('category_id')
    cat_group = []
    for category in categories:
        #find groups for said category
        cat_cursor = db['category_per_group'].find({'category_id': category}).limit(100)
        cat_group += [[category, group['group']] for group in cat_cursor]
    return cat_group
        
def pull_attendees_for_events_for_group(list_of_groups):
    '''
    For every group, we get all of their events. For every event, we get the list of attendees.
    We insert a document into the attendees collection with this information, as well as
    the date and time. 
    '''
    for group in list_of_groups:
        # If it's not already in there.
        if db.attendees.find_one({'urlname':group[1]}) is None:
            print('On Group:' + group[1])
            req = requests.get('https://api.meetup.com/{}/events?\
                                key={}&status=past&page=1&desc=true'.format(group[1], key))
            print(req.headers['X-RateLimit-Remaining'])
            if int(req.headers['X-Total-Count']) > 1:    
                events = events_coll.find({'group.urlname' : group[1]})
                print(events.count())
                for event in events:
                    # Only want events that people showed up to. The host doesn't count. 
                    if event['yes_rsvp_count'] > 1:
                        req = requests.get(
                            'https://api.meetup.com/{}/events/{}/rsvps?key={}&response=yes&only=member'\
                            .format(group[1], event['id'], key))
                        print(events.count())
                        time.sleep(0.25)
                        yeses = json.loads(req.text)
                        ids = [yes['member']['id'] for yes in yeses if yes['member']['event_context']['host'] != True]
                        attendees.insert_one({'group' : event['group']['id'],
                                              'urlname': group[1],
                                              'event' : event['id'],
                                              'date' : event['local_date'],
                                              'time' : event['local_time'],
                                             'attendees' : ids,
                                             'category_id' : group[0]})