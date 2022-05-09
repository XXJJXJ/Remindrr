import discord
import remindrrCommands as rmdr
import sys

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
    username = str(message.author)
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

        elif user_message.lower() == 'bye':
            await message.channel.send(f'See ya later {username}!')

        elif user_message.lower() == "help":
            await message.channel.send(rmdr.HELP)

        elif user_message.startswith("addTask"):
            try:
                components = user_message.split(",")
                date = components[1].strip()
                taskName = components[0].split(" ", 1)[1].strip()
                msg = rmdr.addTask(str(message.author), taskName, date)
                # get message
                await message.channel.send(msg)
            except:
                print("Oops!", sys.exc_info()[0], "occurred.") # for debugging
                await message.channel.send(
                    f"Wrong input format for addTask! :woozy_face:\n"
                    f"Format for addTask command is:\n\n"
                    f"!addTask taskname, dd/mm/yyyy"
                )

        elif user_message.startswith("myTasks"):
            await message.channel.send(rmdr.myTask(username))

        elif user_message.startswith("deleteTask"):
            # delete by name easy --> next time add a delete by index
            position = user_message.find(" ") #find first space and the rest are the name
            if position < 0:
                await message.channel.send("Correct format:\n\n!deleteTask taskname :woozy_face:")
            else:
                taskName = user_message[position + 1:]
                await message.channel.send(rmdr.deleteTask(username, taskName))

        elif user_message.startswith("setReminder "):
            await message.channel.send('setReminder Function under development')

        elif user_message.startswith("timeNow"):
            await message.channel.send(rmdr.getTime())

        elif user_message.startswith("setTimer "):
            # time in seconds
            components = user_message.split(" ")
            time = int(components[1])
            await message.channel.send(await rmdr.setTimeout(username, time))

        else:
            await message.channel.send("Sorry but I don't understand what you want! :sweat_smile:")


client.run(TOKEN)