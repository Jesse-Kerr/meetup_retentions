from pymongo import MongoClient
import numpy as np
import requests
import json
import warnings
warnings.filterwarnings('ignore')
key = open('api.txt', 'r').read()

f = open('groups_not_done.txt', 'r')
groups_not_done = f.read().replace("'", '').replace(" ", '').split(',')
f.close()

client = MongoClient('localhost', 27017)
db = client['meet-ups']
collection = db.groups
events_coll = db.events