import remindrrCommands as rmdr
import Constants
import datetime

async def handleMessage(username, user_message, message):
    if user_message.lower() == "help":
        await message.author.send(Constants.DMHELP)

    elif user_message.startswith("addTask"):
        try:
            components = user_message.split(",")
            date = components[1].strip()
            taskName = components[0].split(" ", 1)[1].strip()
            await message.author.send(rmdr.addTask(str(message.author), taskName, date))
        except:
            await message.author.send(Constants.getWrongFormatMessage("addTask")
                                      + "\n**Note** Avoid the use of slashes ('/') and commas(',') in your taskname")

    elif user_message.startswith("myTasks"):
        await message.author.send(rmdr.myTask(username))

    elif user_message.startswith("deleteTask"):
        # delete by name easy --> next time add a delete by index
        try:
            args = user_message.split(" ", 1)  # split at most 1 time
            assert args[0] == "deleteTask", "Incorrect format"
            taskName = args[1]
            await message.author.send(rmdr.deleteTask(username, taskName))
        except:
            await message.author.send(Constants.getWrongFormatMessage("deleteTask"))

    elif user_message.startswith("setReminder"):
        try:
            args = user_message.split(" ")
            assert args[0] == "setReminder"
            time = args[1]
            # this chunk below can be cleaner
            now = datetime.datetime.utcnow()
            remindTime = datetime.datetime(now.year, now.month, now.day, int(time[0:2]), int(time[2:]),
                                           0) - datetime.timedelta(hours=8)
            timeToWait = remindTime - now

            if timeToWait.total_seconds() < 0:
                timeToWait = timeToWait.total_seconds() + 60 * 60 * 24  # next day
                remindTime += datetime.timedelta(days=1)
            else:
                timeToWait = timeToWait.total_seconds()

            # method to set alarmOn
            await message.author.send(rmdr.setReminder(username, remindTime))
            rmdr.setAlarmOn(username, remindTime)
            # print(f"Time to wait: {timeToWait} seconds")
            await rmdr.wait(timeToWait)
            # wait first, then after waiting if it is still the same, remind
            while rmdr.isAlarmOn(username) and rmdr.getAlarmTime(username) == remindTime:
                # Need to ensure this "thread" don't run infinitely
                await message.author.send(rmdr.myTask(username))
                remindTime += datetime.timedelta(days=1)
                rmdr.setAlarmOn(username, remindTime)
                oneDay = 60 * 60 * 24
                await rmdr.wait(oneDay)
        except:
            await message.author.send(Constants.getWrongFormatMessage("setReminder"))

    elif user_message == "timeNow":
        await message.author.send(rmdr.getTime(username))

    elif user_message == "offAlarm":
        await message.author.send(rmdr.setAlarmOff(username))

    elif user_message.startswith("setTimer"):
        try:
            components = user_message.split(" ")
            time_in_seconds = int(components[1])
            await message.author.send(await rmdr.setTimeout(username, time_in_seconds))
        except:
            await message.author.send(Constants.getWrongFormatMessage("setTimer"))

    else:
        await message.author.send("Sorry but I don't understand what you want!\n\n"
                                   "Type !help for assistance! :sweat_smile:")
