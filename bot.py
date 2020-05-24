
#from discord import Client as discordClient
from discord.ext import commands, tasks

from supporting_functions import logEvent, getConstants #For printouts and logging of events

#==================================================================================================================================

bot = commands.Bot(command_prefix=getConstants("PREFIX"))

#==================================================================================================================================

@bot.event
async def on_ready():
    logEvent(str(bot.user.display_name), "connected")
    #start event loop

@bot.event
async def on_message(message) : #log message
    foo = message.author
    bar = message.content
    twothousand = message.id
    logEvent(message,"")

@bot.event
async def on_message_edit(messageBefore, messageAfter) : 
    print("Message Editted.")
    #print(str(message) + "\n\n" + str(other))
    print(str(messageBefore.content))
    print(str(messageAfter.content))

@bot.event
async def on_message_deleted(message) : #DOESN'T WORK
    print("Message Deleted.")

#==================================================================================================================================

bot.run(getConstants("DISCORD_TOKEN"))

#==================================================================================================================================
