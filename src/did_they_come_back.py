from pymongo import MongoClient
from collections import Counter

key = open('src/api.txt', 'r').read()

client = MongoClient()
db = client['meet-ups']
attendees = db.attendees

def did_they_come_back():
    
    # Get list of urlnames in db.attendees
    urlnames = db.attendees.distinct('urlname')
    for urlname in urlnames:
        category_id = db.attendees.find_one({'urlname':urlname})['category_id']
        events = db.attendees.find({'urlname':'The-Drawing-Circle-Valencia'})
        all_attendees_ever = [event['attendees'] for event in events]
        return length(all_attendees_ever)
        #turns list of lists into list.
        all_attendees_ever = [k for i in all_attendees_ever for k in i]
        
        #Counts number who have ever attended.
        all_attendees_ever_set = len(set(all_attendees_ever))
        
        #Counts their occurence, only keeps the returners.
        times_dict = Counter(all_attendees_ever)
        all_attendees_greater_than_1 = len([k for k, v in times_dict.items() if v > 1])
        percent_return = all_attendees_greater_than_1 / all_attendees_ever_set
        
        #Insert the data for each group into mongo
        db.returns_per_group.insert_one({'urlname' : urlname,
                                         'Percent_Return' : percent_return,
                                         'Category_ID': category_id})

did