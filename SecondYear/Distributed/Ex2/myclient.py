# Open a terminal(command prompt) window and run the server:
#   python3 ./myserver.py localhost 8090
# Open another terminal and run the client:
#   python3 ./myclient.py localhost 8090
# When in gui write help to see all the available commands and their usage
# Afterwards, register a username then open another client on new terminal window and register another user
# Call the command LIST to see all the connected users
# Use command MESSAGE to send a message to everyone
# Use DM to send a message to specific user only

import sys
import tkinter
from tkinter import scrolledtext

from ex2utils import Client
from tkinter import *


class IRCClient(Client):

    def __init__(self):
        super(IRCClient, self).__init__()
        self.done = False

    def onMessage(self, socket, message):
        global gui
       
        print(message)
        message += '\n\n'
        gui.chatBox["state"] = NORMAL
        gui.chatBox.insert(END, message)
        gui.chatBox["state"] = DISABLED
        return True

    def onDisconnect(self, socket):
        global gui
        print("Disconnected from the server")



def closing():
    global gui, client

    gui.root.destroy()
    client.stop()


class GUI:

    def __init__(self):
        self.text = None
        self.sendMessage = None
        self.chatBox = None

        self.client = None
        self.ip = None
        self.port = None

        self.scrollableFrame = None
        self.scrollbar = None
        self.canvas = None

        self.container = None
        self.name = None

        self.root = Tk()
        self.root.title("Communication System for Healthcare Professionals")
        self.setClient()


    def setClient(self):
        global client

        self.ip = sys.argv[1]
        self.port = int(sys.argv[2])
        client = IRCClient()
        client.start(self.ip, self.port)


    def setUp(self):

        self.chatBox = scrolledtext.ScrolledText(self.root, height=30, width=90)
        self.chatBox.grid(column=1, columnspan=5, row=1, padx=10, pady=10, sticky=N + S + E + W)
        self.chatBox["state"] = NORMAL
        self.chatBox.insert(END, "Type \"HELP\" to see list of commands\n\n")
        
        self.chatBox["state"] = DISABLED
        self.text = Text(self.root, height=2, width=1)
        self.text.grid(column=1, row=2, columnspan=4, sticky=N + S + E + W)

        self.sendMessage = Button(self.root, text="Send", command=self.send)
        self.sendMessage.grid(column=5, row=2, sticky=N + S + E + W)
        
        self.root.bind("<Return>", self.send)
        self.root.protocol("WM_DELETE_WINDOW", closing)
        self.root.mainloop()

    def send(self, e=None):
        global client
        #Retrieves the text entered into a text widget named text that is a member variable of the self instance. 
        #The text is retrieved from the first character in the widget (line 1, column 0) to the end of the widget minus one character (END + "-1c").
        input = self.text.get("1.0", tkinter.END + "-1c")

        print(input)

        if input.upper().strip() == "CLOSE":
            closing()

        else:
            client.send(input.encode())
            input += '\n'
            self.chatBox["state"] = NORMAL
            self.chatBox.insert(END, input)
            self.chatBox["state"] = DISABLED
            self.text.delete('1.0', END)


client = None
gui = GUI()
gui.setUp()
