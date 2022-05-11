# Constants
TASKS = "Tasks"
ADDTASK = "addtask"
DELETE_TASK = "deltask"


CommandsToFormat = {
       # Individual
       "addtask": "!addTask taskname, dd/mm/yyyy",
       "deltask": "!delTask taskname",
       "mytasks": "!myTasks",
       "setreminder": "!setReminder time_in_24hr_format",
       "offalarm": "!offAlarm",
       "settimer": "!setTimer time_in_seconds",
       # Group
       "addgrptask": "!addGrpTask taskname, dd/mm/yyyy",
       "delgrptask": "!delGrpTask taskname",
       "grptasks": "",
       "setgrpreminder": "!setGrpReminder time_in_24hr_format",
       "offgrpalarm": "",
       "setgrptimer": "!setGrpTimer time_in_seconds"
}

DMHELP = "**Individual Features** available are:\n\n" \
       f"1. {CommandsToFormat.get('addtask')}\n" \
       f"2. {CommandsToFormat.get('deltask')}\n" \
       f"3. !myTasks\n" \
       f"4. {CommandsToFormat.get('setreminder')}\n" \
       f"5. !offAlarm\n" \
       f"6. {CommandsToFormat.get('settimer')}\n\n"

HELP = "**Individual Features** available are:\n\n" \
       f"1. {CommandsToFormat.get('addtask')}\n" \
       f"2. {CommandsToFormat.get('deltask')}\n" \
       f"3. !myTasks\n" \
       f"4. {CommandsToFormat.get('setreminder')}\n" \
       f"5. !offAlarm\n" \
       f"6. {CommandsToFormat.get('settimer')}\n\n" \
       "**Group Features** available are:\n\n" \
       f"1. {CommandsToFormat.get('addgrptask')}\n" \
       f"2. {CommandsToFormat.get('delgrptask')}\n" \
       f"3. !grpTasks\n" \
       f"4. {CommandsToFormat.get('setgrpreminder')}\n" \
       f"5. !offGrpAlarm\n" \
       f"6. {CommandsToFormat.get('setgrptimer')}"

def getWrongFormatMessage(command):
       return f"Wrong input format for {command}! :woozy_face:\n" \
              f"Format for {command} command is:\n\n" \
              f"{CommandsToFormat.get(command)}"