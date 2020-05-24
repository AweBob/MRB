
from discord.ext import commands, tasks #for the discord bot itself
from supporting_functions import logEvent, getConstants #For printouts and logging of events

#==================================================================================================================================

bot = commands.Bot(command_prefix=getConstants("PREFIX"))
loggedMessages = {} #id: [message, author, channel]

#==================================================================================================================================

@bot.event
async def on_ready():
    logEvent(str(bot.user.display_name), "connected")

@bot.event
async def on_message(message) :
    loggedMessages[message.id] = [message.content, message.author, message.channel]
    logEvent("message" + str(message.id),"logged") #if it was an edit the id will remain the same and this will write over the old info

@bot.event
async def on_message_edit(messageBefore, messageAfter) : 
    bot.get_channel(getConstants("BOT_CHANNEL")).send('Message Edit"\nAuthor: ' + messageAfter.author + ' in channel: ' + messageBefore.channel + "\n" + messageBefore + "\n" + messageAfter)
    loggedMessages[messageAfter.id] = [messageAfter.content, messageAfter.author, messageAfter.channel] #reset the records
    logEvent("edit"+str(messageAfter.id),"logged") #log it
    
@bot.event
async def on_message_deleted(message) : #DOESN'T WORK
    foo = 'bar' #

#Have a looping command every so often checking for messages older then the limit and removing them

#==================================================================================================================================

bot.run(getConstants("DISCORD_TOKEN"))

#==================================================================================================================================
