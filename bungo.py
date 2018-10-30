#!/usr/bin/env python3
# Work with Python 3.6

import discord
import datetime
import bottools
from apikeys import discordkey

TOKEN = discordkey.token 

client = discord.Client()




@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!stories'):
        for line in bottools.getDailies():
            msg = f'**{line[0]}**\n{line[1]}\n\n'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!nightfall'):
        for line in bottools.getNightfalls():
            msg = f'**{line[0]}**\n{line[1]}\n\n'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!modifiers'):
        msg = f'Strike Modifiers as of {datetime.datetime.now()} are:'
        await client.send_message(message.channel, msg)
        for line in bottools.getModifiers():
            msg = f'**{line}**\n'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!gambit'):
        if '{0.author.nick}'.format(message) == 'None':
            name = '{0.author.name}'.format(message)
        else:
            name = '{0.author.nick}'.format(message)
        msg = f'{name}, your gambit stats for your {message.content.split()[1]} are:'
        await client.send_message(message.channel, msg)
#        for k,v in bottools.getMotesLost(name).items():
        print(message.content.split())
        for k,v in bottools.getGambitStat(name,message.content.split()[1]).items():
            msg = f'{k} {v}'
            await client.send_message(message.channel, msg)

#    if message.content.startswith('!helpgambit'):
#        msg = f'''Gambit options that can be checked include: 
#            blockerKills, highValueKills, invaderKills, invaderDeaths,
#            invasionKills, mobKills, motesDeposited, primevalDamage,
#            primevalHealing, smallBlockersSent, mediumBlockersSent, largeBlockersSent'''
#        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!help'):
        msg = f'''
        Hello, my options include:
            **!modifiers** - Get the daily modifiers
            **!stories**   - Get the daily stories available
            **!nightfall** - Get the weekly nightfalls available
            **!matches**   - Get your total count for gambit matches

            **!gambit [option]**
            **!leaderboard [option] [statistic]**

            Gambit options that can be checked include:
                blockerKills, highValueKills, invaderKills, invaderDeaths, invasionKills, 
                mobKills, motesDeposited, primevalDamage, primevalHealing, smallBlockersSent, 
                mediumBlockersSent, largeBlockersSent
            
            Gambit statistics are either:
            max   - This is your personal best for all matches
            total - This is the total over all gambit matches
            '''
        await client.send_message(message.channel, msg)

    if message.content.startswith('!leaderboard'):
        if message.content.split()[2] == 'total':
            mod = 'sum'
        else:
            mod = message.content.split()[2]
        msg = f'The Leaderboard for {message.content.split()[1]} are:'
        await client.send_message(message.channel, msg)
        for k,v in bottools.getLeaderboard(message.content.split()[1],mod).items():
            msg = f'{k:25} : {v}'
            await client.send_message(message.channel, msg)
        
    if message.content.startswith('!valor'):
        msg = f''' 
```
    | Rank 0,|Rank 1,|Rank 2,|Rank 3,|Rank 4,|Rank 5
    | Grdian |Brave  |Heroic |Fabled |Mythic |Legend
L   | +10    | +10   | +10   | +10   | +10   | +10
1W  | +12    | +12   | +15   | +17   | +20   | +22
2W  | ?      | +17   | +20   | +22   | +25   | +27
3W  | ?      | +22   | +25   | +27   | +30   | +32
4W  | ?      | +27   | +30   | +32   | +35   | +37
5W  | ?      | +32   | +35   | +37   | +40   | +42
6W  | N/A    | +12   | +15   | +17   | +20   | +22
    | 0      | 50    | 350   | 700   | 1150  | 1800
```
'''
        await client.send_message(message.channel, msg)

    if message.content.startswith('!ep'):
        msg = f'''
```
Boss                        | Weekly Reset      |SG SMG SR
Bok Litur, Hunger of Xol    | 23rd of October   |X  X   X
Nur Abath, Crest of Xol     | 30th of October   |X  -   -
Kathok, Roar of Xol         | 6th of November   |-  X   -
Damkath, The Mask           | 13th of November  |-  -   X
Naksud, the Famine          | 20th of November  |X  X   X
Bok Litur, Hunger of Xol    | 27th of November  |X  X   X
Nur Abath, Crest of Xol     | 4th of December   |X  -   -
```
'''
        await client.send_message(message.channel,msg)














@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
