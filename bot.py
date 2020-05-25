
from discord.ext import commands, tasks #for the discord bot itself
from supporting_functions import logEvent, getConstants #For printouts and logging of events

#==================================================================================================================================

bot = commands.Bot(command_prefix=None) #no commands so no prefix
loggedMessages = {} #id: [message, author, channel]

#==================================================================================================================================

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
async def on_message_deleted(message) : #DOESN'T WORK
    foo = 'bar' #

#==================================================================================================================================

bot.run(getConstants("DISCORD_TOKEN"))

#==================================================================================================================================

#TODO: on_message_edit exclude messages from bots
#TODO: on_message_delete work
#TODO: Make a loop every so often to remove messages outside the time range
#TODO: Move supporting_functions.py to this same file for simplicity
