# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import discord
import json
import leg03tents 
import leg04
import leg09
import os
from replit import db
from discord.ext import commands

# Initialize the bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
activityBot = discord.Activity(name = 'TAR is Gold',type = discord.ActivityType.playing)
client = commands.Bot(command_prefix='$', intents=intents, activity = activityBot)

with open('official-roles.json') as f:
  officialRoles = json.load(f)

###############################################
##               TAR is Gold                 ##
##             Friday Bot Codes              ##
###############################################

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  content = message.content
  channel = message.channel
  author = message.author
  guild = message.guild

  if content.startswith('$hello'):
      await channel.send('Hello!')

  if channel.id in [1065231788580012102] and content.startsWith('$'):
    command = content[1:]
    result = leg09.process_message(command, author)
    if result is None:
      return
    if isinstance(result, discord.Embed):  # Check if the result is an embed
      await channel.send(embed=result)
    else:
      await channel.send(result)

  if channel.id in [1170738186771763341, 1065231788580012102] and content.startswith('$'):
      command = content[1:]
      result = leg03tents.process_message(command, author)
      if result is None:
        return
      if isinstance(result, discord.Embed):  # Check if the result is an embed
        await channel.send(embed=result)
      else:
        await author.send(result)
        labs = client.get_channel(1065231788580012102)
        await labs.send(result)

  if channel.id in [1171784983602528307] and content.startswith('$'):
        command = content[1:]
        #call leg 04 content
        messageOutput = leg04.get_message(leg04.item_guess(command))
        messageOutput = f"**{author.display_name}**{messageOutput}"
        await channel.send(messageOutput)

#### TOKEN SETTING - DO NOT TOUCH ###########
try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
