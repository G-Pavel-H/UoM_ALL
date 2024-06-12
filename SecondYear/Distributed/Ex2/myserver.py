import sys
import time

from ex2utils import Server


class MyServer(Server):

    def __init__(self):
        super(MyServer, self).__init__()
        self.users = {}
        self.numOfUsers = 0

    def onStart(self):
        print("Server running...")

    def onStop(self):
        print("\nServer ended")

    def onConnect(self, socket):
        self.numOfUsers += 1
        print("User connected, Current number of users: ", self.numOfUsers)
    
    def onDisconnect(self, socket):
        if socket in self.users.values():
            self.numOfUsers -= 1
            print("Disconnecting the follwoing user: ", list(self.users.keys())[list(self.users.values()).index(socket)], "\n", 
                  "Current number of users: ", self.numOfUsers)
            self.users.pop(list(self.users.keys())[list(self.users.values()).index(socket)])
        else:
            self.numOfUsers -= 1
            print("Disconnecting a user. Current number of users: ", self.numOfUsers)
        
    
    def onMessage(self, socket, message):
        #Getting the command and parameters from the message
        (comm, sep, parameter) = message.strip().partition(' ')
        print("Command: ", comm)
        print("Message: ", parameter)

        if comm == '' and parameter == '':
            pass

        elif comm.upper() == "LIST" and parameter == '':

            if socket in self.users.values():

                Sending = 'Online users:\n'
                for key, val in self.users.items():
                    if val == socket:
                        Sending += "You\n"
                    else:
                        Sending += f'{key}\n'

                socket.send(Sending.encode())

            else:

                Sending = "Register to see currently online users."
                socket.send(Sending.encode())

        elif comm.upper() == "HELP" and parameter == '':

            Sending = "\nCommands:\n" \
                     "REGISTER <username> - registers a username for user\n" \
                     "(N.B. Username must not contain spaces)\n" \
                     "LIST - shows a list of all online users\n" \
                     "MESSAGE <message> - sends a message to all users\n" \
                     "DM <user> <message> - sends a message to a specific user\n" \
                     "CLOSE - terminate connection to server\n" \
                     "HELP - provides a list of comms\n" \
                     "PS. You don't have to type the commands in upperacse letters\n"
            
            socket.send(Sending.encode())

      
        elif comm.upper() == "CLOSE" and parameter == '':

            Sending = "Thank You for using our service."
            socket.send(Sending.encode())
            socket.close()
           

        elif parameter == '':

            Sending = "Invalid command. Try again, ensuring the following format".encode() + \
                     " <COMMAND> <PARAMETER[S]> ".encode()
            socket.send(Sending)

        elif comm.upper() == "REGISTER":
            # parameter = parameter.upper()
            # Making sure no spaces in the name
            if parameter.count(' ') > 0:
                Sending = "Spaces are not allowed for username".encode()
                socket.send(Sending)
            #Checking if user exists
            elif self.users.get(parameter) is not None:

                if self.users.get(parameter) == socket:
                    Sending = f"Username already set to {parameter}".encode()
                    socket.send(Sending)
                else:
                    Sending = f"User already exists".encode()
                    socket.send(Sending)

            else:
                #If user already registered then update username
                if socket in list(self.users.values()):
                    oldUsername = list(self.users.keys())[list(self.users.values()).index(socket)]
                    self.users.pop(oldUsername)
                    Sending = f"Username changed to: {parameter}"
                #Otherwise register the new user
                else:
                    Sending = f"Username set: {parameter}"

                print(Sending)
                self.users[parameter] = socket
                socket.send(Sending.encode())

        elif comm.upper() == "MESSAGE":

            if socket in self.users.values():

                if self.numOfUsers != 1:
                    for key, val in self.users.items():
                        if val != socket:
                            Sending = f"Message from " +\
                                     f"{list(self.users.keys())[list(self.users.values()).index(socket)]}" +\
                                     f": {parameter}"
                            val.send(Sending.encode())

                else:

                    Sending = f"No other users currently online to send a message."
                    socket.send(Sending.encode())
            else:
                Sending = f"Register to send a message."
                socket.send(Sending.encode())

        elif comm.upper() == "DM":
            if socket in self.users.values():
                (DM, sep, msg) = parameter.strip().partition(' ')
                DM = DM.upper()
                if DM in self.users.keys():
                    receiver = self.users[DM]
                    if receiver != socket:
                        Sending = f"Message from " +\
                                 f"{list(self.users.keys())[list(self.users.values()).index(socket)]}" +\
                                 f": {msg}"
                        receiver.send(Sending.encode())
                    else:
                        Sending = "Error: Can't send a message to Yourself."
                        socket.send(Sending.encode())
                else:
                    Sending = f"User not found, incorrect username."
                    socket.send(Sending.encode())
            else:
                Sending = f"Register to send a message."
                socket.send(Sending.encode())

        else:
            print("Unknown command")
            Sending = "Invalid command: Try again, ensuring the following format".encode() + \
                     " <COMMAND> <PARAMETER[S]>".encode() + \
                     " separated by spaces E.g. REGISTER User1".encode()
            socket.send(Sending)

        return True




# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()
server.start(ip, port)
