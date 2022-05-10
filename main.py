import datetime
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
                await message.channel.send(rmdr.addTask(str(message.author), taskName, date))
            except:
                print("Oops!", sys.exc_info()[0], "occurred.") # for debugging
                await message.channel.send(
                    "Wrong input format for addTask! :woozy_face:\n"
                    "Format for addTask command is:\n\n"
                    "!addTask taskname, dd/mm/yyyy\n"
                    "**Note** Avoid the use of slashes ('/') and commas(',') in your taskname"
                )

        elif user_message.startswith("myTasks"):
            await message.channel.send(rmdr.myTask(username))

        elif user_message.startswith("deleteTask"):
            # delete by name easy --> next time add a delete by index
            try:
                args = user_message.split(" ", 1) # split at most 1 time
                assert args[0] == "deleteTask", "Incorrect format"
                taskName = args[1]
                await message.channel.send(rmdr.deleteTask(username, taskName))
            except:
                await message.channel.send(
                    "Wrong input format for deleteTask! :woozy_face:\n"
                    "Format for deleteTask command is:\n\n"
                    "!deleteTask taskname"
                )

        elif user_message.startswith("setReminder"):
            try:
                # Possible error, setReminder multiple times cannot remove... unless wait for 24hrs later
                args = user_message.split(" ")
                assert args[0] == "setReminder"
                time = args[1]
                # this chunk below can be cleaner
                now = datetime.datetime.utcnow()
                remindTime = datetime.datetime(now.year, now.month, now.day, int(time[0:2]), int(time[2:]), 0) - datetime.timedelta(hours=8)
                timeToWait = remindTime - now
                # method to set alarmOn
                await message.channel.send(rmdr.setReminder(username, remindTime))
                rmdr.setAlarmOn(username, remindTime)
                if timeToWait.total_seconds() < 0:
                    timeToWait = timeToWait.total_seconds() + 60*60*24 # next day
                    remindTime += datetime.timedelta(days=1)
                else:
                    timeToWait = timeToWait.total_seconds()

                # print(f"Time to wait: {timeToWait} seconds")
                await rmdr.wait(timeToWait)
                # wait first, then after waiting if it is still the same, remind
                while rmdr.isAlarmOn(username) and rmdr.getAlarmTime(username) == remindTime:
                    # Need to ensure this "thread" don't run infinitely
                    await message.channel.send(rmdr.myTask(username))
                    remindTime += datetime.timedelta(days=1)
                    rmdr.setAlarmOn(username, remindTime)
                    timeToWait = 60 * 60 * 24
                    await rmdr.wait(timeToWait)
            except:
                print("Oops!", sys.exc_info()[0], sys.exc_info()[1], "occurred.")  # for debugging
                await message.channel.send(
                    "Wrong input format for setReminder! :woozy_face:\n"
                    "Format for setReminder command is:\n\n"
                    "!setReminder time_in_24hr_format e.g. 2359"
                )

        elif user_message == "timeNow":
            await message.channel.send(rmdr.getTime(username))

        elif user_message == "offAlarm":
            await message.channel.send(rmdr.setAlarmOff(username))

        elif user_message.startswith("setTimer"):
            try:
                components = user_message.split(" ")
                time_in_seconds = int(components[1])
                await message.channel.send(await rmdr.setTimeout(username, time_in_seconds))
            except:
                await message.channel.send(
                    "Wrong input format for setTimer! :woozy_face:\n"
                    "Format for setTimer command is:\n\n"
                    "!setTimer time_in_seconds"
                )

        else:
            await message.channel.send("Sorry but I don't understand what you want!\n\n"
                                       "Type !help for assistance! :sweat_smile:")


client.run(TOKEN)
# when we activate the bot, need to re-activate all the Reminder for everyone (?) hmmmm
