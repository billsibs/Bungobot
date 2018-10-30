#/usr/bin/env python3

import requests
import sys
import json
import os
import bungotools
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gambit.settings")
django.setup()

from django.db import models
from django.db.models import Sum,Max
from gambitapp.models import gambitStats,GuardianId,GuardianClass


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

def getClanGuardianList():
    classes = []
    for guardian in getClanList():
        for g in getGuardianClasses(guardian):
            classes.append(g)
    return classes

def getClanList():
    return bungotools.getdbListValues(GuardianId.objects.filter(active=1).values('guardianId'),'guardianId')

def getMotesLost(user):
    statsMod = ['Max','Sum']
    stat = 'motesLost'
    modResponse = {'Max': 0, 'Sum':0}
    gid = getGuardianId(user)
    for cid in getGuardianClasses(gid):
        for statMod in statsMod:
            matchCount = gambitStats.objects.filter(guardianId=cid).aggregate(eval(statMod)(stat))
            #print(matchCount)
            if matchCount[stat+f'__{statMod.lower()}'] != None:
                if matchCount[stat+f'__{statMod.lower()}'] > modResponse[statMod]:
                    modResponse.update( {statMod : matchCount[stat+f'__{statMod.lower()}'] } )
    return modResponse

def checkStat(statistic):
    statsList = [
        'blockerKills',
        'highValueKills',
        'invaderKills',
        'invaderDeaths',
        'invasionKills',
        'largeBlockersSent',
        'mediumBlockersSent',
        'mobKills',
        'motesDeposited',
        'primevalDamage',
        'primevalHealing',
        'smallBlockersSent',
        'motesLost',
    ]
    for s in statsList:
        if statistic.lower() == s.lower():
            stat = s
            break
        else:
            stat = ''
    return stat

def getGambitStat(user, stat):
    temp_stat = ''
    statsMod = ['Max','Sum']
    gid = getGuardianId(user)
    modResponse = { 'Sorry' : 'No data found' }
    temp_stat = checkStat(stat)
    print(temp_stat)
    if temp_stat:
        modResponse = {'Max': 0, 'Sum':0}
        for cid in getGuardianClasses(gid):
            for statMod in statsMod:
               matchCount = gambitStats.objects.filter(guardianId=cid).aggregate(eval(statMod)(temp_stat))
               if matchCount[temp_stat+f'__{statMod.lower()}'] != None:
                    if matchCount[temp_stat+f'__{statMod.lower()}'] > modResponse[statMod]:
                        modResponse.update( {statMod : matchCount[temp_stat+f'__{statMod.lower()}'] } )
    elif stat.lower() == 'matches':
        matchCount = 0
        for cid in getGuardianClasses(gid):
            matchCount += gambitStats.objects.filter(guardianId=cid).count()
            modResponse =( {'Count' : matchCount }) 
    return modResponse

def getGuardianId(name):
    gid = GuardianId.objects.filter(guardianName=name).values('guardianId')
    return gid[0]['guardianId']

def getGuardianClasses(gid):
    return bungotools.getdbListValues(GuardianClass.objects.filter(guardianId=gid).values('guardianClassId'),'guardianClassId')

def getGuardianNameByClass(cid):
    gid = bungotools.getdbListValues(GuardianClass.objects.filter(guardianClassId=cid).values('guardianId'),'guardianId')
    name = getGuardianName(gid[0])
    return name

def getGuardianName(gid):
    name = GuardianId.objects.filter(guardianId=gid).values('guardianName')
    return name[0]['guardianName']


def getLeaderboard(stat, mod):
    tempResponse = {}
    modResponse = {}
    temp_stat = checkStat(stat)
    statsMod = ['max','sum']
    if mod.lower() in statsMod:
        for cid in getClanGuardianList():
            matchCount = gambitStats.objects.filter(guardianId=cid).aggregate(eval(mod.title())(temp_stat))
            if matchCount[temp_stat+f'__{mod.lower()}'] != None:
                tempResponse.update( { cid : matchCount[temp_stat+f'__{mod.lower()}'] } )
        s = [(k, tempResponse[k]) for k in sorted(tempResponse, key=tempResponse.get, reverse=True)]
        for k,v in s[:5]:
            modResponse.update( {getGuardianNameByClass(int(k)): v} )
    return modResponse
                

