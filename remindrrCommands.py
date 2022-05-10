import datetime

# use firebase for data storage
# firebase_admin for firestore
# firebase for authentication, cloud storage and firebase real time database (excluding firestore)
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from asyncio import sleep

cred = credentials.Certificate("remindrr-firebase-adminsdk.json") #input is the path to file
firebase_admin.initialize_app(cred)
database = firestore.client()

database_user = database.collection("Users")
database_group = database.collection("Groups")

# Constants
TASKS = "Tasks"
HELP = "Features available are:\n\n" \
       "1. !addTask taskname, dd/mm/yyyy\n" \
       "2. !deleteTask taskname\n" \
       "3. !myTasks\n" \
       "4. !setReminder time_in_24hr_format\n" \
       "5. !offAlarm\n" \
       "6. !setTimer time-in-seconds"

def initialiseUser(user):
    database_user.document(user).set({
        "name": user,
        "alarmOn": False
    })

def addTask(user, taskname, deadline):
    # check for duplicates and give "error"
    doc = database_user.document(user).collection(TASKS).document(taskname).get()
    if doc.exists:
        return f"Task: {taskname} already exists!"

    dateComponents = deadline.split("/")
    day = int(dateComponents[0])
    month = int(dateComponents[1])
    year = int(dateComponents[2])
    date = datetime.datetime(year, month, day, 0, 0, 0)
    database_user.document(user).collection(TASKS).document(taskname).set(
        {
            "name": taskname,
            "deadline": date
        }
    )
    return f"Adding:\n\nTask: {taskname}\nDeadline: {deadline}\n\nDone! :white_check_mark:" #should be a message to be sent by bot


def myTask(user):
    docs = database_user.document(user).collection(TASKS).get()
    sorted_docs = sorted(docs, key=lambda x:x.to_dict()["deadline"])
    count = 1
    msg = ""
    for d in sorted_docs:
        data = d.to_dict()
        # parse time
        components = str(data["deadline"]).split(" ")[0].split("-")
        year = int(components[0])
        month = int(components[1])
        day = int(components[2])
        deadline = datetime.date(year, month, day)
        task = f'{count}. Task: {data["name"]}, Deadline: {deadline.strftime("%d %b %Y")}\n'
        msg += task
        count += 1
    if msg == "":
        return "You do not have any tasks! Try adding some tasks with !addTask :smiley:"

    print(msg)
    return msg



def deleteTask(user, taskName):
    # check for match
    doc = database_user.document(user).collection(TASKS).document(taskName).get()
    if doc.exists:
        database_user.document(user).collection(TASKS).document(taskName).delete()
        print(f"Deleting Task: {taskName}")
        return f"Deleting Task: {taskName} :white_check_mark:" #msg sent by bot
    else:
        return f"No task named: {taskName} found! Pls check again! :disappointed_relieved:\n" \
               f"Correct format: !deleteTask taskname"

# NOTE: Currently only supports Singapore time
def setReminder(user, reminderTime):
    #TODO: Possible expansion, need to use user's timezone data,
    # need to send a message to ask them to set a timezone, else "error"
    msg = f"Reminder set to: {reminderTime + datetime.timedelta(hours=8)}"
    print(msg)
    return msg

async def wait(seconds):
    await sleep(seconds)

async def setTimeout(user, seconds):
    await wait(seconds)
    return f'Time is up! Your tasks are:\n\n' + myTask(user)

def setAlarmOn(user, alarmTime):
    # used with setReminder
    data = database_user.document(user).get()
    if not data.exists:
        initialiseUser(user)
    database_user.document(user).update({"alarmOn": True, "alarmTime": alarmTime})

def setAlarmOff(user):
    # used as standalone command
    data = database_user.document(user).get()
    if not data.exists:
        initialiseUser(user)
    database_user.document(user).update({"alarmOn": False})
    return "Your alarm has successfully been offed"

def isAlarmOn(user):
    data = database_user.document(user).get().to_dict()
    return data["alarmOn"]

def getAlarmTime(user):
    data = database_user.document(user).get().to_dict()
    date_time = data["alarmTime"]
    print(date_time) # 2022-05-20 00:35:00+00:00
    date = str(date_time).split(" ")[0].split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    time = str(date_time).split(" ")[1].split(":")
    deadline = datetime.datetime(year, month, day, int(time[0]), int(time[1]), 0)
    return deadline


def setTimezone(user, timezone):
    #TODO: write into user's profile their timezone and a !helpTz
    return "Development in progress"

def getTime(user):
    now = datetime.datetime.utcnow()
    # TODO: Store a timezone profile for users, then use it to determine offset
    #  If no timezone field detected, give warning and default UTC time given
    #  Ask user to set using !setTimezone, use !helpTz to get information of timezone
    timeDifference = datetime.timedelta(hours=8)
    now += timeDifference
    date_time = now.strftime("%d %b %Y, %H:%M")
    msg = f'The current date and time at Singapore is: {date_time}'
    return msg


### Firestore (Writing Guide)
### Firestore (Reading Guide):
## https://github.com/codefirstio/Cloud_Firestore_CRUD_Tutorials/blob/main/read_data.py
# Testing
