#!/usr/bin/python
# Wikki IRC Bot. Built for the #bukkitwiki channel for the Bukkit Community.
# Script by resba
# Shortened Version of Wikkit, only one command!
# Version: 1.0
# http://wiki.bukkit.org/IRC/Bots/Wikkit
# License: Do not remove this original copyright for fair use. 
# Give credit where credit is due!
# Requirements: Feedparser Python Library [http://www.feedparser.org/]
# For a base version of this bot, check out Sprokkit [https://www.github.com/resba/Sprokkit]
#
# NOTE: All commented lines of CODE are debug messages for when something goes wrong.

# Step 1: Import all the necessary libraries.
import socket, sys, string, time, feedparser

# Step 2: Enter your information for the bot. Incl Port of IRC Server, Nick that
# the Bot will take, host (IRC server), RealName, Channel that you want the bot
# to function in, and IDENT value.
port = 6667
nick = "Wikki"
host = 'optical.esper.net'
name =  "WikkiBot"
channel = '#bukkitwiki'
ident = 'Loveitwhenweletloose'
#Nickpasscheck: 1 - The nick requires a pass. 0 - The nick does NOT require a pass.
nickpasscheck = 1
#Nickpass: Password for Nick (If required.)
nickpass = 'changeme'

#botadmin: your nick is inputted for access to debug commands such as graceful shutdown and debug messages
botadmin = 'resba'
botadmin2 = 'chris'

#DebugSwitch: For use when debug is needed.
debug = 0

# Now we just initialize socket.socket and connect to the server, giving out
# the bot's info to the server.
woot = socket.socket()
woot.connect ( (host, port) )
woot.send ( 'NICK ' + nick + '\r\n' )
woot.send ( 'USER ' + ident + ' 0 * :BukkitBot\r\n' )
global nameslist
global sentmessage
global messageable
messageable = ''
lastUsed = time.time()

# Beginning the Loop here.
while 1:
    data = woot.recv ( 1204 )
    print(data)
    globalnullvalue = ""

# Feelin' up the channel.
    if data.find ( '376' ) != -1:
        woot.send( 'JOIN '+channel+'\r\n' )
    if data.find ( '353' ) != -1:
        nameslist = data
        if (debug == 1):
            woot.send( 'PRIVMSG '+channel+' :Found new NAMES Listing: %s\r\n' %nameslist )
    if data.find ( 'PING' ) != -1:
        woot.send( 'PONG ' + data.split() [1] + '\r\n');
    if (nickpasscheck == 1):
        if data.find ( 'NickServ!' ) != -1:
            woot.send ( 'PRIVMSG NickServ :IDENTIFY '+nick+' '+nickpass+'\r\n' )
            nickpasscheck = 0
    def filterResponse():
        sentmessage = data
        if (debug == 1):
            woot.send ( 'PRIVMSG '+channel+' :Loaded filterResponse Function with '+sentmessage+' as the trigger. \r\n' )
        #The command has been called. First check to see what type of command was called.
        if data.find ( ':!' ) != -1:
            global messageable 
            messageable = channel
            if (debug == 1):
                woot.send ( 'PRIVMSG '+channel+' :The command was an announement ! \r\n' )
            #The command was an announcement. now we check for privilages.
            mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            if (debug == 1):
                woot.send ( 'PRIVMSG '+channel+' :Last Message: %s\r\n'%mySubString )
            atsymbol = "@"
            voicesymbol = "+"
            #If the nameslist variable contains the user with some sort of privilage. The check ends and returns to the command.
            if nameslist.find(atsymbol+mySubString) != -1:           
                if (debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are an op \r\n' )
                #because this is a global filter, the messageable is named the channel because its an announcement.
                return 0
            elif nameslist.find(voicesymbol+mySubString) != -1:
                if (debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are voiced \r\n' )
                return 0
            else:
                #If the user is NOT privilidged, then they need to jump through a few more hoops.
                if(debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are not a privilidged user \r\n' )
                if(time.time() - lastUsed) > 10:
                    global lastUsed
                    lastUsed = time.time()
                    if (debug == 1):
                        woot.send ('PRIVMSG '+channel+' :lastUsed Check Passed, now returning to command \r\n' )
                    return 0
                else:
                    if (debug == 1):
                        woot.send ( 'PRIVMSG '+channel+' :Command Cooldown Active. Ignoring Command \r\n' )
                    return 1
        elif data.find ( ':^' ) != -1:
            #The Command was a Privmsg, so we send the privmsg.
            global readUserName
            readUserName = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            global messageable 
            messageable = readUserName
            return 0
# Beginning commands below. Parsed with feedparser.

# !wiki: Checks the recent changes RSS feed at wiki.bukkit.org
    if data.find ( 'bwiki' ) != -1:
        if (filterResponse() == 0):
            feedurl = feedparser.parse("http://wiki.bukkit.org/index.php?title=Special:RecentChanges&feed=atom")
            newest = feedurl['items'][0]
            e = feedurl.entries[0]
            threadurl = e.link
            title = e.title
            author = e.author
            timestamp = e.updated
            summary = e.summary
            summarya = summary.replace('<p>','')
            summaryb = summarya.replace('</p>','')
            woot.send ( 'PRIVMSG '+messageable+' :-- BukkitWiki Most Recent Edit [ http://wiki.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Most Recent Change: %s\r\n" % title)
            woot.send ("PRIVMSG "+messageable+" :Author: %s\r\n" % author)
            woot.send ("PRIVMSG "+messageable+" :Summary: %s\r\n" % summaryb)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % threadurl)
            woot.send ("PRIVMSG "+messageable+" :Timestamp: %s\r\n" % timestamp)
