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


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
