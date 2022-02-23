# Server Side

import socket
import os
import pickle
import sys
from threading import Thread
import math

# This function is here just if we would like to search in all computer's files
# However, the default is searching for the image in the current location
def Search(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


host = socket.gethostname()                                      # get local machine name
port = 5115                                                      # The port that the client is going to connect to


class Server(Thread):                                            # Server's class
    def __init__(self, ip, port, socket):
        Thread.__init__(self)                                    # Assigned Thread
        self.ip = ip                                             # Server's ip
        self.port = port                                         # Server's port
        self.socket = socket                                     # Server's socket
        print("New Thread for " +ip+ ":" +str(port))             # Announcing a connection

    def run(self):
        AllData = []                                             # a list to occupy all the data parts
        FileName,id,NoThread = self.socket.recv(1024).decode('ascii').split(",") # receiving file name, id and client connections' number
        id = int(id)                                             # converting id to integer since it was string
        NoThread = int(NoThread)                                 # converting client connections' number to integer since it was string
        # Path = Search(FileName, "C:\\")                        # Search function, mentioned above
        NewImage = open(FileName,'rb')                           # opening the file with its given name
        iid = 0                                                  # creating ID parameter for data's arrangement
        while True:                                              # a loop to read data parts
            Data = NewImage.readline(1024)                       # read every line from the image
            AllData.append([iid,Data])                           # assign that read part with an id for arrangement then add it to the list
            iid += 1                                             # incrementing the data's ID
            if not Data:                                         # a condition to check if it finished reading the image
                break                                            # then it breaks
        NewImage.close()                                         # close the image after reading all its data
        chunk = int(math.ceil(len(AllData)/float(NoThread)))     # assigning a chunk size proportional to the data size and the amount of client's connections
        AllData = AllData[chunk*id:chunk*(id+1)]                 # divide the data for every chunk
        FileSize = sys.getsizeof(pickle.dumps(AllData))          # Serialize the data size for usage in receiving
        self.socket.send(str(FileSize).encode('ascii'))          # sending the image size to client so he can use it
        dataToSend = pickle.dumps(AllData)                       # Serialize the data chunk so it will be able for transmission
        self.socket.send(dataToSend)                             # transmit serialized data
        print("Yay! Chunk has been sent\n")                      # announce the transmission success
        self.socket.close()                                      # close connection with that thread



threads = []                                                     # a list of assigned threads
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object
serversocket.bind( (host, port) )                                # establishing connection given IP & Port


#=======================================================================================================

connections = 50
for conn in range(connections):
    serversocket.listen()                                            # waiting for clients to connect
    print("Waiting for Client to connect ...")
    clientsocket, (ip, port) = serversocket.accept()                 # accept clients connection whenever there is

    newThread = Server(ip, port, clientsocket)                       # assigning a thread for every connection
    newThread.start()                                                # start that thread
    threads.append(newThread)                                        # add that thread to the threads list

for t in threads:                                                    # looping over all assigned threads
    t.join()                                                         # join the data from those threads when they are done

print("Transmitting Image is Done")                                  # success announcement


#=======================================================================================================
#=======================================================================================================