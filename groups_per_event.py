import numpy as np
import requests
key = open('src/api.txt', 'r').read()

f = open('new_groups.txt', 'r')
new_groups_done = f.read().replace('"', '').replace(",", "").splitlines()
f.close()

def number_events_per_group(list_of_urlnames):
    ''' 
    Count the events for a group. Save somehow.
    '''
    events_per_group = {}
    for urlname in list_of_urlnames:   
        try:     
            req = requests.get('https://api.meetup.com/{}/events?\
                                key={}&status=past&page=1&desc=true'.format(urlname, key))
            number_of_events = int(req.headers['X-Total-Count'])
            events_per_group[urlname] = number_of_events
            print('Inserted {} into events_per_group!'.format(urlname))
        except:
            print("Something went wrong!")
    
    f= open("events_per_group.txt","w+")
    f.write(str(events_per_group))

number_events_per_group(new_groups_done)

