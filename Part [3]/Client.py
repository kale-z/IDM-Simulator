# Client Side

import socket
import os
import pickle
from threading import Thread

host = socket.gethostname()                                 # get local machine name
port = 5115                                                 # The port that the server is connected to

#=======================================================================================================

threads = []                                                    # a list of established threads
totalData = []                                                  # a list for all received data
class Client(Thread):                                           # a class for Client methods
    def __init__(self, id, NoThred, FileName):
        Thread.__init__(self)                                   # initialized thread
        self.id = id                                            # initialized id
        self.NoThread = NoThred                                 # nomber of client connection
        self.FileName = FileName                                # file name

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = server.connect_ex((host, port))                   # checking if there is a connection in the given port
        while res != 0:                                         # if there is not connection, it will connect
            res = server.connect_ex((host, port))
        message = ",".join([self.FileName, str(self.id), str(self.NoThread)])
        server.send(message.encode('ascii'))

        FileSize = server.recv(1024)                            # receive the file size
        AllData = server.recv(int(FileSize))                    # Receiving Data Chunks
        DeSerialized = pickle.loads(AllData)                    # Deserializing the Data
        DeSerialized.sort(key=lambda x: x[0])                   # sort the data according ot its assigned ID
        totalData.extend(DeSerialized)                          # add the data to the list to be combined later


connections = 50                                                # the amount of TCP connections established (assigned threads)
FileName = str(input("Enter the Image name with its extension: "))

Desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
Path = os.path.join(Desktop, 'New Image.jpg')           # Searching for the Desktop path on client's computer to save the image there
NewImage = open(Path,'wb')                              # if image exists, create a new image to write its data
for conn in range(connections):                         # for every established TCP connection
    newThread = Client(conn, connections, FileName)     # assign a thread for that connection
    newThread.start()                                   # start the thread
    threads.append(newThread)                           # add this thread to threads list

for t in threads:                                       # for every thread in the threads list
    t.join()                                            # join them all after they are done

totalData.sort(key=lambda x: x[0])                      # sort the data according to the assigned ID
for i in range(len(totalData)):                         # Creating the Image
    NewImage.write(totalData[i][1])                     # write into the image from the stored data

NewImage.close()                                        # close the image that we are writing its data on
print("Yay! Image has been received\nThe Image has been saved in your Desktop")
exit()                                                  # close the connection

#=======================================================================================================
#=======================================================================================================