# Constants
TASKS = "Tasks"

CommandsToFormat = {
       # Individual
       "addtask": "!addTask taskname, dd/mm/yyyy",
       "deletetask": "!deleteTask taskname",
       "mytasks": "!myTasks",
       "setreminder": "!setReminder time_in_24hr_format",
       "offalarm": "!offAlarm",
       "settimer": "!setTimer time-in-seconds",
       # Group
       "addgrptask": "!addGrpTask taskname, dd/mm/yyyy",
       "deletegrptask": "!deleteGrpTask taskname",
       "grptasks": "",
       "setgrpreminder": "!setGrpReminder time_in_24hr_format",
       "offgrpalarm": "",
       "setgrptimer": "!setGrpTimer time-in-seconds"
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