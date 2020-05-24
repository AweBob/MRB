
from time import time, ctime
from json import dumps
from json import load as jsonLoad 

#==================================================================================================================================

directPath = None #will be determined by initLog

def logEvent(eventType, eventStatus) : #be careful with this and strange characters, if you ever wanna read this log with code strange characters r gonna mess everything up. underscores r ok
    global directPath #so it can be modified outside of it's scope.
    curTime = int(time()) #set the time so if this takes a while or starts at second .99 and ends at 1.01 it won't create confusion in the codes logic and logging process
    if(directPath==None) : #if the log hasn't been initialized
        directPath = "\\logs\\MRB" + str(curTime) + ".log" #Set direct path 
        openFile = open(directPath,"w+") #create the file
        openFile.write(str(dumps({'time':curTime, 'type':'starting_log', 'status':'' })) + "\n") #write initial message
        openFile.close() #save it
    openFile = open(directPath, 'a') #open it with append mode
    openFile.write(str(dumps({'time':curTime, 'type':str(eventType), 'status':str(eventStatus)})) + "\n")
    openFile.close() #save it
    print(str(ctime(curTime)) + " - " + str(eventType) + " - " + str(eventStatus)) #Do a printout as well

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

