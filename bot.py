
#from discord import Client as discordClient
from discord.ext import commands, tasks

from supporting_functions import logEvent, getConstants #For printouts and logging of events

#==================================================================================================================================

bot = commands.Bot(command_prefix=getConstants("PREFIX"))

#==================================================================================================================================

@bot.event
async def on_ready():
    logEvent(str(bot.user.display_name), "connected")
    for guild in bot.guilds:
        logEvent("in guild",f'{guild.name} - {guild.id}')
    #start event loop

@bot.command(name='mh', brief='message history')
@commands.has_role(getConstants("ACCESS_ROLE"))
async def mh(ctx, arg_num=None, *args) :
    foo = 'bar'

@bot.event
async def on_message(message) : #log message
    foo = message.author
    bar = message.content
    twothousand = message.id

@bot.event
async def on_message_edit(message) :
    print("Message Editted.")

@bot.event
async def on_message_deleted(message) :
    print("Message Deleted.")

#==================================================================================================================================

bot.run(getConstants("DISCORD_TOKEN"))

#==================================================================================================================================
