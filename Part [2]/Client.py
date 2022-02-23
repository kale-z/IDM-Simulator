# Client

import socket
import os
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket object
host = socket.gethostname()                                 # get local machine name
port = 5115                                                 # The port that the server is connected to
server.connect((host, port))                                # Connect to given IP & Port

#=======================================================================================================

while True:
    FileName = str(input("Enter the Image name with its extension: "))
    server.send(FileName.encode('ascii'))                   # Transmitting the obtained File Name

    Desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    Path = os.path.join(Desktop, 'New Image.jpg')           # Searching for the Desktop path on client's computer to save the image there

    if server.recv(1024).decode('ascii') == "Nothing":      # This is when server informs client that image doesn't exist
        print("Unfortunately, the Image doesn't exist")
        exit()                                              # close the connection
    NewImage = open(Path,'wb')                              # if image exists, create a new image to write its data

    FileSize = server.recv(1024).decode('ascii')            # Receiving the file size to assign it for receiving the Data
    AllData = server.recv(int(FileSize))                    # Receiving Data Chunks
    DeSerialized = pickle.loads(AllData)                    # Deserializing the Data

    DeSerialized.sort(key=lambda x: x[0])                   # Sorting the Data according to its bound ID

    for i in range(len(DeSerialized)):                      # Creating the Image
        NewImage.write(DeSerialized[i][1])

    NewImage.close()                                        # close the image that we are writing its data on
    print("Yay! Image has been received\nThe Image has been saved in your Desktop")
    exit()                                                  # close the connection

#=======================================================================================================
#=======================================================================================================