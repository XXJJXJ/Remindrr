import Constants
# import PrivateMessage
import remindrrCommands as rmdr
import datetime
import sys

async def handleMessage(username, group_name, command, args, message):
    # Personal command logic do here: (copy this for group commands)
    if message.channel.name == "general":
        if command == "help":
            await message.channel.send(Constants.HELP)

        # "Group" Features
        # use startswith to account for cases where they forgot spaces
        elif command.startswith("addgrptask"):
            try:
                components = args.split(",")
                date = components[1].strip()
                taskName = components[0].strip()
                await message.channel.send(rmdr.addGrpTask(group_name, taskName, date))
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")  # for debugging
                await message.channel.send(Constants.getWrongFormatMessage("addgrptask")
                                           + "\n**Note** Avoid the use of slashes ('/') and commas(',') in your taskname")

        elif command == "grptasks":
            await message.channel.send(rmdr.grpTask(group_name))

        elif command.startswith("delgrptask"):
            # delete by name easy --> next time add a delete by index
            try:
                assert command == "delgrptask", "Incorrect format"
                taskName = args
                await message.channel.send(rmdr.deleteGrpTask(group_name, taskName))
            except:
                await message.channel.send(Constants.getWrongFormatMessage("delgrptask"))

        elif command.startswith("setgrpreminder"):
            try:
                assert command == "setgrpreminder"
                time = args
                # this chunk below can be cleaner
                now = datetime.datetime.utcnow()
                remindTime = datetime.datetime(now.year, now.month, now.day, int(time[0:2]), int(time[2:]), 0) - datetime.timedelta(hours=8)
                timeToWait = remindTime - now
                oneDay = 60 * 60 * 24
                if timeToWait.total_seconds() < 0:
                    timeToWait = timeToWait.total_seconds() + oneDay  # next day
                    remindTime += datetime.timedelta(days=1)
                else:
                    timeToWait = timeToWait.total_seconds()

                # method to set alarmOn
                await message.channel.send(rmdr.setReminder(group_name, remindTime))
                rmdr.setGrpAlarmOn(group_name, remindTime)
                # print(f"Time to wait: {timeToWait} seconds")
                await rmdr.wait(timeToWait)
                # wait first, then after waiting if it is still the same, remind
                while rmdr.isGrpAlarmOn(group_name) and rmdr.getGrpAlarmTime(group_name) == remindTime:
                    # Need to ensure this "thread" don't run infinitely
                    await message.channel.send(rmdr.grpTask(group_name))
                    remindTime += datetime.timedelta(days=1)
                    rmdr.setGrpAlarmOn(group_name, remindTime)
                    await rmdr.wait(oneDay)
            except:
                print("Oops!", sys.exc_info()[0], sys.exc_info()[1], "occurred.")  # for debugging
                await message.channel.send(Constants.getWrongFormatMessage("setgrpreminder"))

        elif command == "offgrpalarm":
            await message.channel.send(rmdr.setGrpAlarmOff(group_name))

        elif command.startswith("setgrptimer"):
            try:
                time_in_seconds = int(args)
                await message.channel.send(await rmdr.setGrpTimeout(group_name, time_in_seconds))
            except:
                await message.channel.send(Constants.getWrongFormatMessage("setgrptimer"))

        # "Individual" Features, can be replaced with PrivateMessage.handleMessage if send privately,
        # current implementation, replies to the group
        elif command.startswith("addtask"):
            try:
                components = args.split(",")
                date = components[1].strip()
                taskName = components[0].strip()
                await message.channel.send(rmdr.addTask(username, taskName, date))
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")  # for debugging
                await message.channel.send(Constants.getWrongFormatMessage("addtask")
                                           + "\n**Note** Avoid the use of slashes ('/') and commas(',') in your taskname")

        elif command == "mytasks":
            await message.channel.send(rmdr.myTask(username))

        elif command.startswith("deltask"):
            # delete by name easy --> next time add a delete by index
            try:
                assert command == "deltask", "Incorrect format"
                taskName = args
                await message.channel.send(rmdr.deleteTask(username, taskName))
            except:
                await message.channel.send(Constants.getWrongFormatMessage("deltask"))

        elif command.startswith("setreminder"):
            try:
                assert command == "setreminder"
                time = args
                # this chunk below can be cleaner
                now = datetime.datetime.utcnow()
                remindTime = datetime.datetime(now.year, now.month, now.day, int(time[0:2]), int(time[2:]), 0) - datetime.timedelta(hours=8)
                timeToWait = remindTime - now
                oneDay = 60 * 60 * 24
                if timeToWait.total_seconds() < 0:
                    timeToWait = timeToWait.total_seconds() + oneDay  # next day
                    remindTime += datetime.timedelta(days=1)
                else:
                    timeToWait = timeToWait.total_seconds()

                # method to set alarmOn
                await message.channel.send(rmdr.setReminder(username, remindTime))
                rmdr.setAlarmOn(username, remindTime)
                # print(f"Time to wait: {timeToWait} seconds")
                await rmdr.wait(timeToWait)
                # wait first, then after waiting if it is still the same, remind
                while rmdr.isAlarmOn(username) and rmdr.getAlarmTime(username) == remindTime:
                    # Need to ensure this "thread" don't run infinitely
                    await message.channel.send(rmdr.myTask(username))
                    remindTime += datetime.timedelta(days=1)
                    rmdr.setAlarmOn(username, remindTime)
                    await rmdr.wait(oneDay)
            except:
                print("Oops!", sys.exc_info()[0], sys.exc_info()[1], "occurred.")  # for debugging
                await message.channel.send(Constants.getWrongFormatMessage("setreminder"))

        elif command == "timenow":
            await message.channel.send(rmdr.getTime(username))

        elif command == "offalarm":
            await message.channel.send(rmdr.setAlarmOff(username))

        elif command.startswith("settimer"):
            try:
                time_in_seconds = int(args)
                await message.channel.send(await rmdr.setTimeout(username, time_in_seconds))
            except:
                await message.channel.send(Constants.getWrongFormatMessage("settimer"))

        else:
            await message.channel.send("Sorry but I don't understand what you want!\n\n"
                                       "Type !help for assistance! :sweat_smile:")
