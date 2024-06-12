import sys
import im
import time
import urllib.error

class Server:
    def __init__(self):
        try:
            #Initialising server
            self.server = im.IMServerProxy('https://web.cs.manchester.ac.uk/j80841pg/comp28112_ex1/IMserver.php')
            
            self.server['message'] = ''.encode('UTF-8')

            #print(self.server['status'])
            
            #Checking possible server statuses
            if self.server['status'].decode().strip() == 'one':
                self.server['status'] = 'two'.encode('UTF-8')
                self.server['received'] = '0'.encode('UTF-8')
                self.status = "wait"

            elif self.server['status'].decode().strip() == 'two':
                print("Server already in use")
                sys.exit()
            else:
                self.server['status'] = 'one'.encode('UTF-8')
                self.status = "send"

            while self.server['status'].decode().strip() != "two":
                print(f"Searching for second user", end='\r')
                time.sleep(1)
            print("connected")
            self.service()
            
        #Catching Keyboard exception and server errors
        except KeyboardInterrupt:
            print("\nClosing Connection")
            self.server.clear()
            self.server['status'] = "off".encode('UTF-8')
            sys.exit()

        except urllib.error.URLError or urllib.error.HTTPError:
            print("Cannot connect to server :( \nAre you connected to Eduroam/GlobalConnect VPN???")
            self.server.clear()
            self.server['status'] = "off".encode('UTF-8')
            sys.exit(1)
        

        
        
    
    def service(self):
        try:
            #Checking the status then calling apropriate functions based on the state of the user
            while self.server['status'].decode().strip() == 'two':
                if self.status == "send":
                    self.send()
                else:
                    self.wait()
            print("Other user left the conversation \n Closing the connection")       
            self.server.clear()
            self.server['status'] = "off".encode('UTF-8')
            sys.exit()

        except KeyboardInterrupt:
            print("\nClosing Connection")
            self.server.clear()
            self.server['status'] = "off".encode('UTF-8')
            sys.exit()
    
    def send(self):
        try: 
            #Making sure no empty message is sent
            message = input("Write message: \n")
            if message == '\n' or message == '':
                print("Error. No message to send...\n")
                # by returning nothing, it will end the function which is then called again in service(),
                # to then ask for the message again
                return
            
            self.server['message'] = message.encode('UTF-8')

            while self.server['received'].decode().strip() == '0':
                    print("message sending", end='\r')

            print("\nmessage sent")
            self.server['received'] = '0'.encode('UTF-8')
            self.status = "wait"

        except KeyboardInterrupt:
            print("\nClosing Connection")
            self.server.clear()
            self.server['status'] = "off".encode('UTF-8')
            sys.exit()

    def wait(self):
        try:
            if self.server['status'].decode().strip() == 'two':
                #Making sure the user is always notified when the other user is typing
                while self.server['message'].decode().strip() == '' and self.server['status'].decode().strip() == 'two':
                    print("Other user typing.", end='\r')
                    print("Other user typing..", end='\r')
                    print("Other user typing...", end='\r')
                    time.sleep(1)
                
                
                print("Received message: ", self.server['message'].decode().strip())
                self.server['received'] = '1'.encode('UTF-8')
                self.server['message'] = ''.encode('UTF-8')
                self.status = "send"

            else:
                print("Other user left the conversation \n Closing the connection")       
                self.server.clear()
                self.server['status'] = "off".encode('UTF-8')
                sys.exit()

        except KeyboardInterrupt:
            print("\nClosing Connection")
            self.server.clear()
            self.server['status'] = "off".encode('UTF-8')
            sys.exit()



s = Server()






        

