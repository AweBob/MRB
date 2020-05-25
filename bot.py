
#Imports for the discord interaction
from discord.ext import commands, tasks #for the discord bot itself

#Imports for supporting functions
from time import time, ctime
from json import dumps
from json import load as jsonLoad 
from os import getcwd

#==================================================================================================================================
#Define all my supporting functions

directPath = None #will be determined by initLog

def logEvent(eventType, eventStatus) : #be careful with this and strange characters, if you ever wanna read this log with code strange characters r gonna mess everything up. underscores r ok
    global directPath #so it can be modified outside of it's scope.
    curTime = int(time()) #set the time so if this takes a while or starts at second .99 and ends at 1.01 it won't create confusion in the codes logic and logging process
    if(directPath==None) : #if the log hasn't been initialized
        directPath = getcwd() + "\logs\MRB" + str(curTime) + ".log" #Set direct path 
        openFile = open(directPath,"w+") #create the file
        openFile.write(str(dumps({'time':curTime, 'type':'starting_log', 'status':'' })) + "\n") #write initial message
        openFile.close() #save it
    openFile = open(directPath, 'a') #open it with append mode
    openFile.write(str(dumps({'time':curTime, 'type':str(eventType), 'status':str(eventStatus)})) + "\n")
    openFile.close() #save it
    print(str(ctime(curTime)) + " - " + str(eventType) + " - " + str(eventStatus)) #Do a printout as well

def getConstants(id=None) :
    try :
        openFile = open('settings.json','r')
    except :
        logEvent("getConstants ERROR","settings.json not found")
        raise ValueError("settings.json does not exist or cannot be read")
    data = jsonLoad(openFile)
    if(id==None) :
        group = [data["DISCORD_TOKEN"],data["BOT_CHANNEL"],data["HOLDING_TIME"]]
        openFile.close()
        return(group[0],group[1],group[2])
    else :
        group = data[id]
        openFile.close()
        return(group)

#==================================================================================================================================
#Define the bot

bot = commands.Bot(command_prefix=None) #no commands so no prefix
loggedMessages = {} #{id: [message, author, channel], id:[], }

#==================================================================================================================================
#Add all the events and loops

@bot.event
async def on_ready():
    logEvent(str(bot.user.display_name), "connected")

@bot.event
async def on_message(message) :
    if message.author != bot.user : #if it's not the bot
        loggedMessages[message.id] = [message.content, message.author, message.channel]
        logEvent("message" + str(message.id),"logged") #if it was an edit the id will remain the same and this will write over the old info

@bot.event
async def on_message_edit(messageBefore, messageAfter) : 
    if messageBefore.author != bot.user : #if it's not the bot
        await bot.get_channel(getConstants("BOT_CHANNEL")).send('Message Edit Alert:\nAuthor: ' + str(messageAfter.author) + ' in channel: #' + str(messageBefore.channel) + " \nBefore: " + str(messageBefore.content) + "\nAfter: " + str(messageAfter.content))
        loggedMessages[messageAfter.id] = [messageAfter.content, messageAfter.author, messageAfter.channel] #reset the records
        logEvent("edit"+str(messageAfter.id),"logged") #log it
    
@bot.event
async def on_message_deleted(message) :
    foo = 'bar' 

#==================================================================================================================================

bot.run(getConstants("DISCORD_TOKEN")) #Start the bot 

#==================================================================================================================================

#TODO: on_message_edit exclude messages from bots
#TODO: on_message_delete work
#TODO: Make a loop every so often to remove messages outside the time range
