import os
import datetime

# use firebase for data storage
def addTask(user, taskName, deadline, priority):
    print("Developing")

def myTask(user):
    print("Getting user data")

def deleteTask(user, taskName):
    print("Deleting Task lololol")

def setReminder(user, reminderTime):
    print(f"Reminder set to: {reminderTime}")

def getTime():
    now = datetime.datetime.now()
    date_time = now.strftime("%d %b %Y, %H:%M")
    msg = f'The current date and time is: {date_time}'
    return msg

