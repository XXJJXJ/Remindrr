import discord
import remindrrCommands as rmdr

TOKEN = open('Token', "r").read() # to be hidden before pushing

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    # to prevent chatbot from running infinitely to its own messages
    if message.author == client.user:
        return
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    if not user_message.startswith("!"):
        return
    else:
        user_message = user_message[1:]

    channel = str(message.channel.name)
    # somewhat a logger to log in the console
    print(f'{username}: {user_message} ({channel})')

    # all command logic do here: ########################################
    if message.channel.name == "general":
        if user_message.lower() == 'hello':
            await message.channel.send(f'Hello {username}!')
            return
        elif user_message.lower() == 'bye':
            await message.channel.send(f'See ya later {username}!')
            return
        elif user_message.startswith("help"):
            await message.channel.send('Help function under development')
            return
        elif user_message.startswith("addTask"):
            # can modify to account for duplicates and give a response without
            #
            try:
                components = user_message.split(" ")
                priority = components[3]
                date = components[2]
                taskName = components[1]
                rmdr.addTask(str(message.author), taskName, date, priority)
                # get message
                await message.channel.send(f'Task added:\n\nTask: {taskName}\nDeadline: {date}\nPriority: {priority}')
                await message.channel.send('addTask Function under development')
            except:
                await message.channel.send('''Format for addTask command is: E.g.\n\n!addTask taskname ddmmyyyy priority(1 for highest, larger numbers for lower priority)''')

        elif user_message.startswith("myTasks"):
            rmdr.myTask(str(message.author))
            await message.channel.send('myTasks Function under development')

        elif user_message.startswith("deleteTask"):
            # delete by name easy --> next time add a delete by index
            await message.channel.send('deleteTask Function under development')

        elif user_message.startswith("setReminder"):
            await message.channel.send('setReminder Function under development')

        elif user_message.startswith("timeNow"):
            await message.channel.send(rmdr.getTime())

        else:
            await message.channel.send("Sorry but I don't understand what you want! :sweat_smile:")


client.run(TOKEN)