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
HELP = "Features available are:\n\n" \
       "1. !addTask taskname, dd/mm/yyyy\n" \
       "2. !deleteTask taskname\n" \
       "3. !myTasks\n" \
       "4. !setTimer timeInSeconds"


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
            "deadline": date # might have error, try later
        }
    )
    return f"Adding:\n\nTask: {taskname}\nDeadline: {deadline}\n\nDone! :white_check_mark:" #should be a message to be sent by bot


def myTask(user):
    docs = database_user.document(user).collection(TASKS).get()
    count = 1
    msg = ""
    for d in docs:
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