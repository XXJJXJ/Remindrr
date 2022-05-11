import remindrrCommands as rmdr
import Constants
import datetime

async def handleMessage(username, command, args, message):
    if command == "help":
        await message.author.send(Constants.DMHELP)

    elif command.startswith("addtask"):
        try:
            components = args.split(",")
            date = components[1].strip()
            taskName = components[0].strip()
            await message.author.send(rmdr.addTask(str(message.author), taskName, date))
        except:
            await message.author.send(Constants.getWrongFormatMessage("addtask")
                                      + "\n**Note** Avoid the use of slashes ('/') and commas(',') in your taskname")

    elif command.startswith("mytasks"):
        await message.author.send(rmdr.myTask(username))

    elif command.startswith("deletetask"):
        # delete by name easy --> next time add a delete by index
        try:
            assert command == "deletetask", "Incorrect format"
            taskName = args
            await message.author.send(rmdr.deleteTask(username, taskName))
        except:
            await message.author.send(Constants.getWrongFormatMessage("deletetask"))

    elif command.startswith("setreminder"):
        try:
            assert command == "setreminder"
            time = args
            # this chunk below can be cleaner
            now = datetime.datetime.utcnow()
            remindTime = datetime.datetime(now.year, now.month, now.day, int(time[0:2]), int(time[2:]),
                                           0) - datetime.timedelta(hours=8)
            timeToWait = remindTime - now
            oneDay = 60 * 60 * 24
            if timeToWait.total_seconds() < 0:
                timeToWait = timeToWait.total_seconds() + oneDay  # next day
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
                await rmdr.wait(oneDay)
        except:
            await message.author.send(Constants.getWrongFormatMessage("setReminder"))

    elif command == "timenow":
        await message.author.send(rmdr.getTime(username))

    elif command == "offalarm":
        await message.author.send(rmdr.setAlarmOff(username))

    elif command.startswith("settimer"):
        try:
            time_in_seconds = int(args)
            await message.author.send(await rmdr.setTimeout(username, time_in_seconds))
        except:
            await message.author.send(Constants.getWrongFormatMessage("setTimer"))

    else:
        await message.author.send("Sorry but I don't understand what you want!\n\n"
                                   "Type !help for assistance! :sweat_smile:")
