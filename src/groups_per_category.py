from pymongo import MongoClient
import requests
import json
key = open('src/api.txt', 'r').read()
client = MongoClient()
db = client['meet_up']

def get_ids_of_categories():
    # This creates a list of dictionaries, with name, sort_name, id, and shortname. 
    dict_categories = json.loads(requests.get('https://api.meetup.com/2/categories?key={}'.format(key)).text)['results']
    # make list of ids 
    ids = [item['id'] for item in dict_categories]
    ids.sort()
    return [ids, dict_categories]

def get_count_of_category(dictionary, number):
    req_count = requests.get('https://api.meetup.com/find/groups?key={}&radius=global&category={}'.format(key, number))\
                        .headers['X-Total-Count']
    cat_name = next(item['name'] for item in dictionary if item["id"] == number)
    return [number, int(req_count), cat_name]
