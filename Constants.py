# Constants
TASKS = "Tasks"

# Commands
ADD_TASK = "addtask"
DELETE_TASK = "deltask"
MY_TASKS = "mytasks"
SET_REMINDER = "setreminder"
OFF_ALARM = "offalarm"
SET_TIMER = "settimer"

ADD_GROUP_TASK = "addgrptask"
DELETE_GROUP_TASK = "delgrptask"
GROUP_TASKS = "grptasks"
SET_GROUP_REMINDER = "setgrpreminder"
OFF_GROUP_ALARM = "offgrpalarm"
SET_GROUP_TIMER = "setgrptimer"



CommandsToFormat = {
       # Individual
       ADD_TASK: "!addTask taskname, dd/mm/yyyy",
       DELETE_TASK: "!delTask index_of_task",
       MY_TASKS: "!myTasks",
       SET_REMINDER: "!setReminder time_in_24hr_format",
       OFF_ALARM: "!offAlarm",
       SET_TIMER: "!setTimer time_in_seconds",
       # Group
       ADD_GROUP_TASK: "!addGrpTask taskname, dd/mm/yyyy",
       DELETE_GROUP_TASK: "!delGrpTask index_of_task",
       GROUP_TASKS: "!grpTasks",
       SET_GROUP_REMINDER: "!setGrpReminder time_in_24hr_format",
       OFF_GROUP_ALARM: "!offGrpAlarm",
       SET_GROUP_TIMER: "!setGrpTimer time_in_seconds"
}

DMHELP = "**Individual Features** available are:\n\n" \
       f"1. {CommandsToFormat.get(ADD_TASK)}\n" \
       f"2. {CommandsToFormat.get(DELETE_TASK)}\n" \
       f"3. {CommandsToFormat.get(MY_TASKS)}\n" \
       f"4. {CommandsToFormat.get(SET_REMINDER)}\n" \
       f"5. {CommandsToFormat.get(OFF_ALARM)}\n" \
       f"6. {CommandsToFormat.get(SET_TIMER)}\n\n"

HELP = "**Individual Features** available are:\n\n" \
       f"1. {CommandsToFormat.get(ADD_TASK)}\n" \
       f"2. {CommandsToFormat.get(DELETE_TASK)}\n" \
       f"3. {CommandsToFormat.get(MY_TASKS)}\n" \
       f"4. {CommandsToFormat.get(SET_REMINDER)}\n" \
       f"5. {CommandsToFormat.get(OFF_ALARM)}\n" \
       f"6. {CommandsToFormat.get(SET_TIMER)}\n\n" \
       "**Group Features** available are:\n\n" \
       f"1. {CommandsToFormat.get(ADD_GROUP_TASK)}\n" \
       f"2. {CommandsToFormat.get(DELETE_GROUP_TASK)}\n" \
       f"3. {CommandsToFormat.get(GROUP_TASKS)}\n" \
       f"4. {CommandsToFormat.get(SET_GROUP_REMINDER)}\n" \
       f"5. {CommandsToFormat.get(OFF_GROUP_ALARM)}\n" \
       f"6. {CommandsToFormat.get(SET_GROUP_TIMER)}"

def getWrongFormatMessage(command):
       return f"Wrong input format for {command}! :woozy_face:\n" \
              f"Format for {command} command is:\n\n" \
              f"{CommandsToFormat.get(command)}"