import datetime

# use firebase for data storage
# firebase_admin for firestore
# firebase for authentication, cloud storage and firebase real time database (excluding firestore)
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("remindrr-firebase-adminsdk.json") #input is the path to file
firebase_admin.initialize_app(cred)
database = firestore.client()

database_user = database.collection("Users")
database_group = database.collection("Groups")

# Constants
TASKS = "Tasks"


def addTask(user, taskName, deadline, priority):
    # check for duplicates and give "error"
    doc = database_user.document(user).collection(TASKS).document(taskName).get()
    if doc.exists:
        return f"Task: {taskName} already exists!"
    # TODO: parse deadline into dateTime object...

    database_user.document(user).collection(TASKS).document(taskName).set(
        {
            "name": taskName,
            "deadline" : deadline,
            "priority" : priority
        }
    )

    return f"Adding:\n\nTask: {taskName}\nDeadline: {deadline}\nPriority: {priority}\n\nDone! :white_check_mark:" #should be a message to be sent by bot


def myTask(user):
    docs = database_user.document(user).collection(TASKS).get()
    count = 1
    msg = ""
    for d in docs:
        data = d.to_dict()
        # TODO: need a method to parse the time
        task = f'{count}. Task: {data["name"]}, Deadline: {data["deadline"]}, Priority: {data["priority"]}\n'
        msg += task
        count += 1
    print(msg)
    return msg #time currently in UTC, might need an option to account for timezone


def deleteTask(user, taskName):
    # check for match
    doc = database_user.document(user).collection(TASKS).document(taskName).get()

    if doc.exists:
        database_user.document(user).collection(TASKS).document(taskName).delete()
        print(f"Deleting Task: {taskName}")
        return f"Deleteing Task: {taskName} :white_check_mark:" #msg sent by bot
    else:
        return f"No task named: {taskName} found! Pls check again! :disappointed_relieved:"


def setReminder(user, reminderTime):
    print(f"Reminder set to: {reminderTime}")

def getTime():
    now = datetime.datetime.now()
    date_time = now.strftime("%d %b %Y, %H:%M")
    msg = f'The current date and time is: {date_time}'
    return msg


### Firestore (Writing Guide)
'''
# database_user.add({ "username" : "DummyUser Test"}) # random ID
database_user.document("DummyUser Tester").set({"username" : "DummyUser Test"}) # set ID to "DummyUser Tester", overwrites existing document
# database_group.add({ "Group Name" : "DummyGroup Test"}) # random ID
database_group.document("DummyGroup Tester").set({"Group Name" : "DummyGroup Test"}) # set ID to "DummyGroup Tester", overwrites existing document

## Merging
database_user.document("DummyUser Tester").set({"Gender" : "Nil"}, merge=True) # adds a "Gender" field to the DummyUser Document

## Adding (to) sub-collections
database_user.document("DummyUser Tester").collection("Tasks").document("DummyTask1").set({"deadline": "NIL", "priority": 1})
'''

### Firestore (Reading Guide):
## https://github.com/codefirstio/Cloud_Firestore_CRUD_Tutorials/blob/main/read_data.py
# Testing
# myTask("John") # note UTC time is 8hrs slower than GMT