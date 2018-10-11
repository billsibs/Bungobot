#/usr/bin/env python3

import requests
import json

# A Collecting of API tools to gather data for the bungo bot project
# These tools go to the api and put together reset information from
# the bungie API

# Import the API key for access
from apikeys import bungie
HEADERS = bungie.APIKEY

#Common bungie URL. 
bungie_url='https://www.bungie.net/Platform'

# Get the list of hashes related to the bungie story.
# There appears to always be 5 stories daily and that information
# will be used to identify which section of the json will be used
# for this information
def getDailyStoryList():
    storyList = []
    milestone_url = bungie_url + f'/Destiny2/Milestones/'
    milestone = requests.get(milestone_url, headers=HEADERS)
    for mile1 in milestone.json()['Response']:
        if 'activities' in milestone.json()['Response'][str(mile1)]:
            if len(milestone.json()['Response'][str(mile1)]['activities']) == 5:
                for mile2 in milestone.json()['Response'][str(mile1)]['activities']:
                    if 'modifierHashes' in mile2:
                        #print(mile2.keys())
                        storyList.append(mile2['activityHash'])
    return storyList

def lookupActivityName(uid):
    hashIdentifier = uid
    entityType = 'DestinyActivityDefinition'
    stuff_url = bungie_url + f'/Destiny2/Manifest/{entityType}/{hashIdentifier}/'
    stuff = requests.get(stuff_url, headers=HEADERS)
    if 'selectionScreenDisplayProperties' in stuff.json()['Response']:
        details = stuff.json()['Response']['displayProperties']['name'] + ':' + stuff.json()['Response']['selectionScreenDisplayProperties']['description'].replace('\n',' ')
    else:
        details = stuff.json()['Response']['displayProperties']['name'] + ':' +  stuff.json()['Response']['displayProperties']['description']
    return details

def getDailies():
    stories = []
    for s in getDailyStoryList():
        name = lookupActivityName(s).split(':')
        stories.append(name[1:])
    return stories

def getNightfalls():
    storyList = []
    milestone_url = bungie_url + f'/Destiny2/Milestones/'
    milestone = requests.get(milestone_url, headers=HEADERS)
    for mile1 in milestone.json()['Response']:
        if 'activities' in milestone.json()['Response'][str(mile1)]:
                for mile2 in milestone.json()['Response'][str(mile1)]['activities']:
                    #print(mile2)
                    if 'modifierHashes' in mile2:
                        temp_name =lookupActivityName(mile2['activityHash'])
                        if 'Nightfall' in temp_name:
                            if temp_name.split(':')[1:] not in storyList:
                                storyList.append(temp_name.split(':')[1:])
    return storyList

def getModifierDetails(mid):
    modhash = mid
    moddef = 'DestinyActivityModifierDefinition'
    modifier_url = bungie_url + f'/Destiny2/Manifest/{moddef}/{modhash}/'
    moddies = requests.get(modifier_url, headers=HEADERS)
    return moddies.json()['Response']['displayProperties']['name']

def getModifiers():
    story = getDailyStoryList()[0]
    modList = []
    mods = []
    milestone_url = bungie_url + f'/Destiny2/Milestones/'
    milestone = requests.get(milestone_url, headers=HEADERS)
    for mile1 in milestone.json()['Response']:
        if 'activities' in milestone.json()['Response'][str(mile1)]:
            if story == milestone.json()['Response'][str(mile1)]['activities'][0]['activityHash']:
                for h in milestone.json()['Response'][str(mile1)]['activities'][0]['modifierHashes']:
                        modList.append(h)
    for m in modList:
        mods.append(getModifierDetails(m))
    return mods














getModifiers()
