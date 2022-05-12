import datetime
from Constants import TASKS

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

def initialise(db, name):
    db.document(name).set({
        "name": name,
        "alarmOn": False
    })

def parseDate(deadline):
    dateComponents = deadline.split("/")
    day = int(dateComponents[0])
    month = int(dateComponents[1])
    year = int(dateComponents[2])
    date = datetime.datetime(year, month, day, 0, 0, 0)
    return date

# Private skeletal method for addTask and addGrpTask
def default_addTask(db, name, taskname, deadline):
    doc = db.document(name).collection(TASKS).document(taskname).get()
    if doc.exists:
        return f"Task: {taskname} already exists!"

    date = parseDate(deadline)
    db.document(name).collection(TASKS).document(taskname).set(
        {
            "name": taskname,
            "deadline": date
        }
    )
    return f"Adding:\n\nTask: {taskname}\nDeadline: {deadline}\n\nDone! :white_check_mark:"

def addTask(user, taskname, deadline):
    # check for duplicates and give "error"
    return default_addTask(database_user, user, taskname, deadline)

def addGrpTask(groupname, taskname, deadline):
    return default_addTask(database_group, groupname, taskname, deadline)



def default_listTask(db, name):
    docs = db.document(name).collection(TASKS).get()
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

def myTask(username):
    return default_listTask(database_user, username)

def grpTask(groupname):
    return default_listTask(database_group, groupname)



def default_deleteTask(db, name, taskName):
    # check for match
    doc = db.document(name).collection(TASKS).document(taskName).get()
    if doc.exists:
        db.document(name).collection(TASKS).document(taskName).delete()
        print(f"Deleting Task: {taskName}")
        return f"Deleting Task: {taskName} :white_check_mark:" #msg sent by bot
    else:
        return f"No task named: {taskName} found! Pls check again! :disappointed_relieved:\n" \
               f"Correct format: !deleteTask taskname"

def default_deleteByIndex(db, name, index):
    docs = db.document(name).collection(TASKS).get()
    if len(docs) == 0:
         return f"There are no tasks found!"

    sorted_docs = sorted(docs, key=lambda x: x.to_dict()["deadline"])
    try:
        assert index > 0, "Out of bounds!"
        target = sorted_docs[index - 1]
        target = target.to_dict()["name"]
        return default_deleteTask(db, name, target)
    except:
        return f"No task at index: {index}! :disappointed_relieved:\n" \
                "Pls check again!"

def deleteTask(username, index):
    return default_deleteByIndex(database_user, username, index)

def deleteGrpTask(groupname, index):
    return default_deleteByIndex(database_group, groupname, index)


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
    return f'Time is up! Your personal tasks are...\n\n' + myTask(user)

async def setGrpTimeout(groupname, seconds):
    await wait(seconds)
    return f'Time is up! Tasks for your group ({groupname}) are...\n\n' + grpTask(groupname)

def default_setAlarmOn(db, name, alarmTime):
    # used with setReminder
    data = db.document(name).get()
    if not data.exists:
        initialise(db, name)
    db.document(name).update({"alarmOn": True, "alarmTime": alarmTime})

def setAlarmOn(username, alarmTime):
    default_setAlarmOn(database_user, username, alarmTime)

def setGrpAlarmOn(groupname, alarmTime):
    default_setAlarmOn(database_group, groupname, alarmTime)

def default_setAlarmOff(db, name):
    # used as standalone command
    data = db.document(name).get()
    if not data.exists:
        initialise(name)
    db.document(name).update({"alarmOn": False})
    return f"Your alarm for {name} has successfully been switched offed"

def setAlarmOff(username):
    default_setAlarmOn(database_user, username)

def setGrpAlarmOff(groupname):
    default_setAlarmOn(database_group, groupname)

def default_isAlarmOn(db, name):
    data = db.document(name).get().to_dict()
    return data["alarmOn"]

def isAlarmOn(username):
    return default_isAlarmOn(database_user, username)

def isGrpAlarmOn(groupname):
    return default_isAlarmOn(database_group, groupname)

def default_getAlarmTime(db, name):
    data = db.document(name).get().to_dict()
    date_time = data["alarmTime"]
    # print(date_time) # 2022-05-20 00:35:00+00:00
    date = str(date_time).split(" ")[0].split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    time = str(date_time).split(" ")[1].split(":")
    deadline = datetime.datetime(year, month, day, int(time[0]), int(time[1]), 0)
    return deadline

def getAlarmTime(username):
    return default_getAlarmTime(database_user, username)

def getGrpAlarmTime(groupname):
    return default_getAlarmTime(database_group, groupname)


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

### Firestore Guide
## https://github.com/codefirstio/Cloud_Firestore_CRUD_Tutorials/
