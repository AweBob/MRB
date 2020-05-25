
#Imports for the discord interaction
from discord.ext import commands, tasks #for the discord bot itself
from discord import Game as activityType #maybe find better type later on

#Imports for supporting functions
from time import time, ctime
from json import dumps
from json import load as jsonLoad 
from os import getcwd

#==================================================================================================================================
#Define all my supporting functions

directPath = None #will be determined by initLog

def logEvent(eventType, eventStatus) : #be careful with this and strange characters, if you ever wanna read this log with code strange characters r gonna mess everything up. underscores r ok
    curTime = int(time()) #set the time so if this takes a while or starts at second .99 and ends at 1.01 it won't create confusion in the codes logic and logging process
    if (getConstants("LOG")=="True") : #If the setting is enabled
        global directPath #so it can be modified outside of it's scope.
        if(directPath==None) : #if the log hasn't been initialized
            directPath = getcwd() + "\logs\MRB" + str(curTime) + ".log" #Set direct path 
            openFile = open(directPath,"w+") #create the file
            openFile.write(str(dumps({'time':curTime, 'type':'starting_log', 'status':'' })) + "\n") #write initial message
            openFile.close() #save it
        openFile = open(directPath, 'a') #open it with append mode
        openFile.write(str(dumps({'time':curTime, 'type':str(eventType), 'status':str(eventStatus)})) + "\n")
        openFile.close() #save it
    print(str(ctime(curTime)) + " - " + str(eventType) + " - " + str(eventStatus)) #Do a printout as well

def getConstants(id) :
    try :
        openFile = open('settings.json','r')
    except :
        logEvent("getConstants ERROR","settings.json not found")
        raise ValueError("settings.json does not exist or cannot be read")
    data = jsonLoad(openFile)
    try :
        group = data[id]
    except :
        logEvent("getConstants ERROR",str(id) + " does not exist")
        raise ValueError(str(id) + " does not exist in settings.json")
    openFile.close()
    return(group)

#==================================================================================================================================

bot = commands.Bot(command_prefix='') #Define the bot  #no commands so no prefix

#==================================================================================================================================
#Add all the events to the bot

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): #supress if cmd isn't found because there aren't any commands anyways...
        return
    raise error

@bot.event
async def on_ready():
    await bot.change_presence(activity=activityType("https://github.com/AweBob/mrb"))
    logEvent(str(bot.user.display_name), "connected")

@bot.event
async def on_message_edit(messageBefore, messageAfter) : 
    if messageBefore.author != bot.user and messageBefore.content != messageAfter.content: #if it's not the bot and if the edit actually changed something
        if str(messageBefore.author) not in getConstants("EXCLUDED_USERS") and str(messageBefore.channel) not in getConstants("EXCLUDED_CHANNELS"):
            await bot.get_channel(getConstants("BOT_CHANNEL")).send('Message Edit Alert:\nAuthor: ' + str(messageAfter.author) + ' in channel: #' + str(messageBefore.channel) + " \nBefore: " + str(messageBefore.content) + "\nAfter: " + str(messageAfter.content))
            logEvent("edit"+str(messageAfter.id),"logged") #log it
    
@bot.event
async def on_raw_message_delete(messageIn) :
    message = messageIn.cached_message #the message is what's left over
    await deletedMessage(message) #has logging

@bot.event
async def on_raw_bulk_message_delete(messagesIn) :
    messages = messagesIn.cached_messages
    for message in messages :
        await deletedMessage(message) #has logging

async def deletedMessage(message) :
    if message != None :
        if message.author != bot.user :
            if str(message.author) not in getConstants("EXCLUDED_USERS") and str(message.channel) not in getConstants("EXCLUDED_CHANNELS"):
                await bot.get_channel(getConstants("BOT_CHANNEL")).send('Message Delete Alert:\nAuthor: '+str(message.author)+ ' in channel: #'+str(message.channel)+' at time: '+str(message.created_at)+"\nMessage: "+str(message.content))
                logEvent("delete"+str(message.id),"logged")

#==================================================================================================================================

bot.run(getConstants("DISCORD_TOKEN")) #Start the bot 

#==================================================================================================================================
