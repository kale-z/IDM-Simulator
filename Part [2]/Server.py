# Server Side

import socket
import os
import pickle
import sys

# This function is here just if we would like to search in all computer's files
# However, the default is searching for the image in the current location
def Search(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object
host = socket.gethostname()                                      # get local machine name
port = 5115                                                      # The port that the client is going to connect to
serversocket.bind( (host, port) )                                # establishing connection given IP & Port
serversocket.listen(1)                                           # waiting for clients to connect
print("Waiting for Client to connect ...")

#=======================================================================================================

id = 0                                                           # Identifying Data by assigning ID numbers to each
AllData = []                                                     # List going to contain the Data with its ID
recieved = False                                                 # Checker for the socket whether it works or not
clientsocket, addr = serversocket.accept()                       # accept clients connection whenever there is
while not recieved:
    try:
        print("The following Client has connected to the Server:",addr)
        print("Waiting for Client's request ...")
        # try:
        FileName = clientsocket.recv(1024).decode('ascii')       # receive file name from client

        # Path = Search(FileName, "C:\\")                        # Search function, mentioned above
        NewImage = open(FileName,'rb')                           # We can replace the variable 'FileName' with 'Path'
        clientsocket.send("OK".encode('ascii'))                  # confirming finding the file


        while True:                                              # looping over Image's data
            Data = NewImage.readline(128)                        # Dividing the Image into chunks [128, 512, 1024]
            AllData.append([id,Data])
            id += 1                                              # Incrementing ID
            if not Data:                                         # if lines are finished, break the loop
                break
        NewImage.close()                                         # close the image means done transmitting its data
        FileSize = sys.getsizeof(pickle.dumps(AllData))          # Measuring the size of the Serialized Data after Identifying them
        clientsocket.send(str(FileSize).encode('ascii'))         # sending the file size
        clientsocket.send(pickle.dumps(AllData))                 # Serializing the Data then send them
        print("Yay! Image has been sent")
        recieved = True
        exit()                                                   # close the connection
        break
    except:
        if not recieved:
            clientsocket.send("Nothing".encode('ascii'))         # if image doesn't exist, inform client
            print ("Unfortunately, the Image doesn't exist.\nTry again!")
            exit()                                               # close the connection


#=======================================================================================================
#=======================================================================================================