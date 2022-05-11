# Constants
TASKS = "Tasks"

CommandsToFormat = {
       # Individual
       "addTask": "!addTask taskname, dd/mm/yyyy",
       "deleteTask": "!deleteTask taskname",
       "myTasks": "!myTasks",
       "setReminder": "!setReminder time_in_24hr_format",
       "offAlarm": "!offAlarm",
       "setTimer": "!setTimer time-in-seconds",
       # Group
       "addGrpTask": "!addGrpTask taskname, dd/mm/yyyy",
       "deleteGrpTask": "!deleteGrpTask taskname",
       "grpTasks": "",
       "setGrpReminder": "!setGrpReminder time_in_24hr_format",
       "offGrpAlarm": "",
       "setGrpTimer": "!setGrpTimer time-in-seconds"
}

DMHELP = "**Individual Features** available are:\n\n" \
       f"1. {CommandsToFormat.get('addTask')}\n" \
       f"2. {CommandsToFormat.get('deleteTask')}\n" \
       f"3. !myTasks\n" \
       f"4. {CommandsToFormat.get('setReminder')}\n" \
       f"5. !offAlarm\n" \
       f"6. {CommandsToFormat.get('setTimer')}\n\n"

HELP = "**Individual Features** available are:\n\n" \
       f"1. {CommandsToFormat.get('addTask')}\n" \
       f"2. {CommandsToFormat.get('deleteTask')}\n" \
       f"3. !myTasks\n" \
       f"4. {CommandsToFormat.get('setReminder')}\n" \
       f"5. !offAlarm\n" \
       f"6. {CommandsToFormat.get('setTimer')}\n\n" \
       "**Group Features** available are:\n\n" \
       f"1. {CommandsToFormat.get('addGrpTask')}\n" \
       f"2. {CommandsToFormat.get('deleteGrpTask')}\n" \
       f"3. !grpTasks\n" \
       f"4. {CommandsToFormat.get('setGrpReminder')}\n" \
       f"5. !offGrpAlarm\n" \
       f"6. {CommandsToFormat.get('setGrpTimer')}"

def getWrongFormatMessage(command):
       return f"Wrong input format for {command}! :woozy_face:\n" \
              f"Format for {command} command is:\n\n" \
              f"{CommandsToFormat.get(command)}"