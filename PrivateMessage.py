import remindrrCommands as rmdr
import Constants
import datetime

async def handleMessage(username, command, args, message):
    if command == "help":
        await message.author.send(Constants.DMHELP)

    elif command.startswith(Constants.ADD_TASK):
        try:
            components = args.split(",")
            date = components[1].strip()
            taskName = components[0].strip()
            await message.author.send(rmdr.addTask(str(message.author), taskName, date))
        except:
            await message.author.send(Constants.getWrongFormatMessage(Constants.ADD_TASK)
                                      + "\n**Note** Avoid the use of slashes ('/') and commas(',') in your taskname")

    elif command.startswith(Constants.MY_TASKS):
        await message.author.send(rmdr.myTask(username))

    elif command.startswith(Constants.DELETE_TASK):
        # delete by index
        try:
            assert command == Constants.DELETE_TASK, "Incorrect format"
            index = int(args)
            await message.author.send(rmdr.deleteTask(username, index))
        except:
            await message.author.send(Constants.getWrongFormatMessage(Constants.DELETE_TASK))

    elif command.startswith(Constants.SET_REMINDER):
        try:
            assert command == Constants.SET_REMINDER
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
            await message.author.send(Constants.getWrongFormatMessage(Constants.SET_REMINDER))

    elif command == "timenow":
        await message.author.send(rmdr.getTime(username))

    elif command == Constants.OFF_ALARM:
        await message.author.send(rmdr.setAlarmOff(username))

    elif command.startswith(Constants.SET_TIMER):
        try:
            time_in_seconds = int(args)
            await message.author.send(await rmdr.setTimeout(username, time_in_seconds))
        except:
            await message.author.send(Constants.getWrongFormatMessage(Constants.SET_TIMER))

    else:
        await message.author.send("Sorry but I don't understand what you want!\n\n"
                                   "Type !help for assistance! :sweat_smile:")
