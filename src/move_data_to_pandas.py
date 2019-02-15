import pymongo
import pandas as pd
from pymongo import MongoClient
client = MongoClient()
db = client['meet-ups']
collection = db['returns_per_group']
data = pd.DataFrame(list(collection.find()))