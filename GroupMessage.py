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
        elif command.startswith(Constants.ADD_GROUP_TASK):
            try:
                components = args.split(",")
                date = components[1].strip()
                taskName = components[0].strip()
                await message.channel.send(rmdr.addGrpTask(group_name, taskName, date))
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")  # for debugging
                await message.channel.send(Constants.getWrongFormatMessage(Constants.ADD_GROUP_TASK)
                                           + "\n**Note** Avoid the use of slashes ('/') and commas(',') in your taskname")

        elif command == Constants.GROUP_TASKS:
            await message.channel.send(rmdr.grpTask(group_name))

        elif command.startswith(Constants.DELETE_GROUP_TASK):
            # delete by name easy --> next time add a delete by index
            try:
                assert command == Constants.DELETE_GROUP_TASK, "Incorrect format"
                index = int(args)
                await message.channel.send(rmdr.deleteGrpTask(group_name, index))
            except:
                await message.channel.send(Constants.getWrongFormatMessage(Constants.DELETE_GROUP_TASK))

        elif command.startswith(Constants.SET_GROUP_REMINDER):
            try:
                assert command == Constants.SET_GROUP_REMINDER
                time = args
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
                await message.channel.send(Constants.getWrongFormatMessage(Constants.SET_GROUP_REMINDER))

        elif command == Constants.OFF_GROUP_ALARM:
            await message.channel.send(rmdr.setGrpAlarmOff(group_name))

        elif command.startswith(Constants.SET_GROUP_TIMER):
            try:
                time_in_seconds = int(args)
                await message.channel.send(await rmdr.setGrpTimeout(group_name, time_in_seconds))
            except:
                await message.channel.send(Constants.getWrongFormatMessage(Constants.SET_GROUP_TIMER))

        # "Individual" Features, can be replaced with PrivateMessage.handleMessage if send privately,
        # current implementation, replies to the group
        elif command.startswith(Constants.ADD_TASK):
            try:
                components = args.split(",")
                date = components[1].strip()
                taskName = components[0].strip()
                await message.channel.send(rmdr.addTask(username, taskName, date))
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")  # for debugging
                await message.channel.send(Constants.getWrongFormatMessage(Constants.ADD_TASK)
                                           + "\n**Note** Avoid the use of slashes ('/') and commas(',') in your taskname")

        elif command == Constants.MY_TASKS:
            await message.channel.send(rmdr.myTask(username))

        elif command.startswith(Constants.DELETE_TASK):
            # delete by index
            try:
                assert command == Constants.DELETE_TASK, "Incorrect format"
                index = int(args)
                await message.channel.send(rmdr.deleteTask(username, index))
            except:
                print("Oops!", sys.exc_info()[1], "occurred.")  # for debugging
                await message.channel.send(Constants.getWrongFormatMessage(Constants.DELETE_TASK))

        elif command.startswith(Constants.SET_REMINDER):
            try:
                assert command == Constants.SET_REMINDER
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
                await message.channel.send(Constants.getWrongFormatMessage(Constants.SET_REMINDER))

        elif command == Constants.OFF_ALARM:
            await message.channel.send(rmdr.setAlarmOff(username))

        elif command.startswith(Constants.SET_TIMER):
            try:
                time_in_seconds = int(args)
                await message.channel.send(await rmdr.setTimeout(username, time_in_seconds))
            except:
                await message.channel.send(Constants.getWrongFormatMessage(Constants.SET_TIMER))

        # Easter egg features
        elif command == "timenow":
            await message.channel.send(rmdr.getTime(username))

        elif command == "rstatus":
            await message.channel.send(rmdr.getReminderStatus(username))

        elif command == "rgrpstatus":
            await message.channel.send(rmdr.getGrpReminderStatus(group_name))

        else:
            await message.channel.send("Sorry but I don't understand what you want!\n\n"
                                       "Type !help for assistance! :sweat_smile:")
