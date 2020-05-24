
from discord import Client as discordClient
from discord.ext import commands#, tasks

from json import load as jsonLoad 
from json import dump as jsonDump

from log import logEvent #For printouts and logging of events

#==================================================================================================================================

def getConstants(id=None) :
    try :
        openFile = open('settings.json','r')
    except :
        logEvent("getConstants ERROR","settings.json not found")
        raise ValueError("settings.json does not exist or cannot be read")
    data = jsonLoad(openFile)
    if(id==None) :
        group = [data["DISCORD_TOKEN"],data["ACCESS_ROLE"],data["BOT_CHANNEL"],data["PREFIX"]]
        openFile.close()
        return(group[0],group[1],group[2],group[3])
    else :
        group = data[id]
        openFile.close()
        return(group)

#==================================================================================================================================  

async def purge_own_messages(channel_to):
    for message in await bot.get_channel(channel_to).history(limit=100).flatten():
        if message.author == bot.user:
            await message.delete()

async def purge_commands(channel_to):
    for message in await bot.get_channel(channel_to).history(limit=100).flatten():
        if message.content.startswith(getConstants("PREFIX")):
            await message.delete()

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

#on message edit

#on message delete

#==================================================================================================================================

bot = commands.Bot(command_prefix=getConstants("PREFIX"))
client = discordClient()
