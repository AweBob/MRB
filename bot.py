
#===========================================================================================================================================================================================================

#Python 3.8.3
#Message Recording Bot - MRB
#By: AweBob#6221

#===========================================================================================================================================================================================================

#Modules

from discord.ext import commands, tasks
from discord import Game as activityType 
from json import load as jsonLoad 
import logging

#===========================================================================================================================================================================================================

#Define constants from settings.json (throw proper errors if need be) : Open File -> Load Json -> Grab Each Variable & Check Type : Throw error & log at any failure point

try :
    openFile = open('settings.json','r') #from current directory
except :
    logging.critical("settings.json not found in working directory or cannot be read")
    raise ValueError("settings.json not found in working directory or cannot be read")

try :
    data = jsonLoad(openFile)
except :
    logging.critical("settings.json could not be converted to json (possibly improper json format)")
    raise OSError("settings.json could not be converted to json")

try :
    DISCORD_TOKEN = data["DISCORD_TOKEN"]
except :
    logging.critical("settings.json doesn't contain DISCORD_TOKEN")
    raise ValueError("settings.json doesn't contain DISCORD_TOKEN")
if not type(DISCORD_TOKEN) == type(str()) :
    logging.critical(f"DISCORD_TOKEN from settings.json is {type(DISCORD_TOKEN)}, but must be {type(str())}")
    raise ValueError(f"DISCORD_TOKEN from settings.json is {type(DISCORD_TOKEN)}, but must be {type(str())}")

try :
    BOT_CHANNEL = data["BOT_CHANNEL"]
except :
    logging.critical("settings.json doesn't contain BOT_CHANNEL")
    raise ValueError("settings.json doesn't contain BOT_CHANNEL")
if not type(BOT_CHANNEL) == type(int()) :
    logging.critical(f"BOT_CHANNEL from settings.json is {type(BOT_CHANNEL)}, but must be {type(int())}")
    raise ValueError(f"BOT_CHANNEL from settings.json is {type(BOT_CHANNEL)}, but must be {type(int())}")

try :
    EXCLUDED_CHANNELS = data["EXCLUDED_CHANNELS"]
except :
    logging.critical("settings.json doesn't contain EXCLUDED_CHANNELS")
    raise ValueError("settings.json doesn't contain EXCLUDED_CHANNELS")
if not type(EXCLUDED_CHANNELS) == type(list()) :
    logging.critical(f"EXCLUDED_CHANNELS from settings.json is {type(EXCLUDED_CHANNELS)}, but must be {type(list())}")
    raise ValueError(f"EXCLUDED_CHANNELS from settings.json is {type(EXCLUDED_CHANNELS)}, but must be {type(list())}")
for excludedChannel in EXCLUDED_CHANNELS :
    if not type(excludedChannel) == type(str()) :
        logging.critical(f"{excludedChannel} in EXCLUDED_CHANNELS from settings.json is {type(excludedChannel)}, but must be {type(str())}")
        raise ValueError(f"{excludedChannel} in EXCLUDED_CHANNELS from settings.json is {type(excludedChannel)}, but must be {type(str())}")

try :
    EXCLUDED_USERS = data["EXCLUDED_USERS"]
except :
    logging.critical("settings.json doesn't contain EXCLUDED_USERS")
    raise ValueError("settings.json doesn't contain EXCLUDED_USERS")
if not type(EXCLUDED_USERS) == type(list()) :
    logging.critical(f"EXCLUDED_USERS from settings.json is {type(EXCLUDED_USERS)}, but must be {type(list())}")
    raise ValueError(f"EXCLUDED_USERS from settings.json is {type(EXCLUDED_USERS)}, but must be {type(list())}")
for excludedUser in EXCLUDED_USERS :
    if not type(excludedUser) == type(str()) :
        logging.critical(f"{excludedUser} in EXCLUDED_USERS from settings.json is {type(excludedUser)}, but must be {type(str())}")
        raise ValueError(f"{excludedUser} in EXCLUDED_USERS from settings.json is {type(excludedUser)}, but must be {type(str())}")

#===========================================================================================================================================================================================================

#Define the bot (bot has no commands so doesn't take a prefix)

bot = commands.Bot( command_prefix=str() ) 

#===========================================================================================================================================================================================================

#Add all the events to the bot

#Supress CommandNotFound error because there aren't any commands in this message recording bot (additonally, this might happen a lot because the command_prefix is a clear string)
@bot.event
async def on_command_error(ctx, error): 
    if not isinstance(error, commands.CommandNotFound): #if error is not a subclass of CommandNotFound error
        raise error #reraise the error
    #else (if error is a subcless of CommandNotFound error) then do nothing (causing error to not get raised)

#When bot logs in
@bot.event
async def on_ready():
    await bot.change_presence( activity=activityType("https://github.com/AweBob/mrb") ) #set bot's activity to a link to this github repo
    logging.info(f"{bot.user.display_name} connected") #log that the bot is connected as info

#When an editted message is detected
@bot.event
async def on_message_edit(messageBefore, messageAfter) : 
    if (messageBefore.author != bot.user) and (messageBefore.content != messageAfter.content) and (str(messageBefore.author) not in EXCLUDED_USERS) and (str(messageBefore.channel) not in EXCLUDED_CHANNELS) :  #if it's not the bot and if the edit actually changed something and the author isn't excluded and the message is not in an excluded channel
        await bot.get_channel(BOT_CHANNEL).send(f"Message Edit Alert:\nAuthor: {messageAfter.author} in channel: #{messageBefore.channel} \nBefore: {messageBefore.content}\nAfter: {messageAfter.content}")
        logging.info(f"edit detected in {messageAfter.id}") 
    
#When a single message is deleted
@bot.event
async def on_raw_message_delete(messageIn) :
    await deletedMessage( messageIn.cached_message ) #Call function to process the message

#When multiple messages are deleted
@bot.event
async def on_raw_bulk_message_delete(messagesIn) :
    for message in messagesIn.cached_messages : #for every message
        await deletedMessage( message ) #call function to process message

#Process a deleted message (Not a bot event)
async def deletedMessage(message) :
    if (message != None) and (message.author != bot.user) and (str(message.author) not in EXCLUDED_USERS) and (str(message.channel) not in EXCLUDED_CHANNELS) : #if message exists and message isn't by the bot and message isnt by an excluded user and message isnt from an excluded channel
        await bot.get_channel(BOT_CHANNEL).send(f"Message Delete Alert:\nAuthor: {message.author} in channel: #{message.channel} at time: {message.created_at}\nMessage: {message.content}")
        logging.info(f"deletion detected in {message.id}")

#===========================================================================================================================================================================================================

#Start the bot

bot.run(DISCORD_TOKEN) 

#===========================================================================================================================================================================================================
