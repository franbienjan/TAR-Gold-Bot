import json

with open('official-threads.json') as f:
    threads = json.load(f)

with open('official-roles.json') as f:
    roles = json.load(f)

#Function that adds a role to the author to view a private channel.
async def move_member(guild, channel, roleId, author):

    role = guild.get_role(roleId)
    await author.add_roles(role)
    await channel.send('You have been added to a new channel. Go and check it!')

#Shortcut, but redundant in function
async def add_role(guild, author, roleId):

    role = guild.get_role(roleId)
    await author.add_roles(role)

# Function that checks whether the channel's valid inputs.
def check_channel(channelId, targetChannelName):
    return channelId in (threads[targetChannelName]['id'],
                         threads['lab']['id'])

def is_admin(rolesList):
  return any(role.id == roles['Admin'] for role in rolesList)
