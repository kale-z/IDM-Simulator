# Client

import socket
import os

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
    while True:                                             # looping over image's data
        Data = server.recv(1024)                            # receiving image's data
        NewImage.write(Data)                                # write its data to the new created image
        if not Data:                                        # if there is no more data, break the loop
            break
    NewImage.close()                                        # close the image that we are writing its data on
    print("Yay! Image has been received\nThe Image has been saved in your Desktop")
    exit()                                                  # close the connection

#=======================================================================================================
#=======================================================================================================