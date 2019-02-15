from pymongo import MongoClient
import requests
import json

key = open('src/api.txt', 'r').read()

client = MongoClient()
db = client['meet-ups']
collection = db.groups

#Meetup only allows 200 requests at a time.
def get_groups_for_category(number, groups):
    number_of_groups = [entry[1] for entry in groups if entry[0] == number] 
    offsets = list(range(int(number_of_groups[0]/200) + 1))
    for offset in offsets:
        req = requests.get('https://api.meetup.com/find/groups?key={}\
                            &category={}&radius=global&\
                            &offset={}&page=200'.format(key, number, offset))
        json_data = json.loads(req.text)
        collection.insert_many(json_data)

