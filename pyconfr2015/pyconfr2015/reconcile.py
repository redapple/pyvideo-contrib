import json

from fuzzywuzzy import fuzz
from prettytable import PrettyTable

with open('talks.json') as t:
    talks = json.load(t)

with open('videos.json') as v:
    videos = json.load(v)


def talk_string(data):
    return ' '.join((' '.join(data.get("speakers")), data.get('title')))


x = PrettyTable([
    'Video title',
    'Talk speakers',
    'Talk title',
    #'URL',
    'Match ratio'])
x.align = 'l'
cutlimit = 48
for video in videos:
    current_talk = video['title']
    ratios = []
    for t in talks:
        ratios.append((fuzz.ratio(current_talk, talk_string(t)), t))
    best_ratio, best_match = max(ratios)
    if best_ratio >= 80:
        try:
            x.add_row([
                video['title'][:cutlimit],
                "; ".join(best_match['speakers'])[:cutlimit],
                best_match['title'][:cutlimit],
                #video['videos'][0]['src'].replace('http://video-pyconfr2015.paulla.asso.fr/', ''),
                best_ratio
            ])
        except:
            raise
print x
