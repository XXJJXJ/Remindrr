# Remindrr User Guide

## Introduction

Remindrr is a Discord reminder bot that resembles the [SE-EDU Duke](https://nus-cs2103-ay1920s1.github.io/website/se-book-adapted/projectDuke/index.html) program.

This bot is designed for discord users to create a list of tasks either for themselves or for the group they are in.
This bot aims to provide regular task reminders to help users/groups keep track of their task at hand in order of the deadline.

**Note this bot is designed for users in timezone GMT+8. Support for other timezones will be developed in the future.


## Individual Features
All features listed in this section can be triggered from any chat with the bot,
i.e. it can be triggered on PMs or in any group users are in with the Bot.
Responses to these features will be sent to users through private messages.


### Add personal task: `!addTask`

Adds a task with a stipulated deadline. 

Format: `!addTask taskname, deadline`
 * taskname: Name of the task. Note, the name should not contain "/" or "," characters.
 * deadline: Date in dd/mm/yyyy format

### Delete personal task: `!deleteTask`

Deletes an existing task with matching task name.

Format: `!deleteTask taskname`
 * taskname: Name of the task. Note, the name should not contain "/" or "," characters.


### List out personal tasks: `!myTasks`

Lists out all existing tasks in chronological order of deadline.

Format: `!myTasks`


### Set personal reminder: `!setReminder`

Schedules a time for the bot to private message the user a reminder of all the tasks at hand daily.

Format: `!setReminder time_in_24hr_format`

E.g. `!setReminder 2300` - Sets reminder message to be sent 11pm daily.


### Switch reminder off: `!offAlarm`

Switches off the daily reminder if there exist an active reminder.

Format: `!offAlarm`


### Set personal timer: `!setTimer`

Schedules a once off reminder for the user.

Format: `!setTimer time_in_seconds`
E.g. `!setTimer 600` - Schedules a reminder private message in 10 minutes. 


## Group Features
All features in this section can be invoked by any users through the chat, inside the group's general channel.
Functionality and usage of features in this section is largely similar to their "individual" counterparts.

**Note: Responses will be sent to the group's general chat and the output is the same regardless of which user invoked it. 


### Add group task: `!addGrpTask`

Adds a task with a stipulated deadline for the group.


### Delete group task: `!deleteGrpTask`

Deletes an existing group task with matching task name.


### List out group tasks: `!grpTasks`

Lists out all existing group tasks in chronological order of deadline.


### Set group reminder: `!setGrpReminder`

Schedules a time for the bot to send a reminder of all the tasks at hand in this group chat daily.


### Switch group reminder off: `!offGrpAlarm`

Switches off the daily reminder if there exist an active reminder in this group chat.


### Set group timer: `!setGrpTimer`

Schedules a once off reminder for the group.
