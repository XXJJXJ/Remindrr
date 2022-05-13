# Remindrr Bot Developer Guide

## Introduction
Welcome to Remindrr Developer's guide! If you are here, you might be interested to contribute to this project by either
improving the functionalities or extending it by adding more features. This document covers how to get started doing so
as well as some ideas for you to try implementing to improve Remindrr.

## Set up guide

1. Fork this repository (To create a copy repo for yourself)
2. Git clone the forked repository into your PC
3. Go to the [Discord Developer webpage](https://discord.com/developers/applications)
   1. Click on "New Application" on the top right corner of the page.
   2. Give your "Test Bot" a name
   3. Click on "Add Bot" and your bot should be generated
   4. Click on "Reset Token" to obtain a fresh token
   5. Copy the Token and paste it in a file named "TOKEN" (without file extension) and put this TOKEN file in your working directory
   6. Under OAuth2 general tab, click "Add Redirect" and paste `https://discord.com/api/oauth2/authorize`
   7. Under OAuth2 url generator tab, select "bot" and the permissions required
   8. Scroll down and the link can be used to add the bot into your groups
4. Run `python main.py` at the project directory to start up this bot

## Hosting Guide

This bot is hosted on Heroku and a video tutorial can be found [here](https://youtu.be/BPvg9bndP1U).

## Potential Areas for improvement

1. Ask for user's timezone data, then responses catered to user's timezone.
2. Add miscellaneous features, play music and mini-activity.
