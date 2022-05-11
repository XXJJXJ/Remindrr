import discord

import GroupMessage
import PrivateMessage

TOKEN = open('Token', "r").read()
client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    username = str(message.author)
    user_message = str(message.content).split(" ", 1)
    command = user_message[0].lower()
    args = user_message[1]

    if not user_message.startswith("!"):
        return
    else:
        user_message = user_message[1:]

    try:
        channel = str(message.channel.name) # will cause error if receive dm
        group_name = message.channel.guild
        # log in the console
        print(f'{username}: {user_message} ({group_name} : {channel})')
        await GroupMessage.handleMessage(username, group_name, command, args, message)
    except:
        # deal with DM functions
        print(f"DM received from {username} : {user_message}")
        await PrivateMessage.handleMessage(username, command, args, message)

client.run(TOKEN)
# when we activate the bot, need to re-activate all the Reminder for everyone (?) hmmmm
