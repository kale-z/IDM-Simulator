# Internet Download Manager Simulator
This is an application of Transmission Control Protocol (TCP) practicing Socket Programming and Threading to simulate Internet Download Manager, where a client is requesting a file from a server, then the server will be transmitting files' chunks, in different packet sizes, to client to download it.


<br>

## Getting Started
This program includes 3 parts, but each part consists only of the same two main files, which are:
- ```Server.py```: the main scripting file to run as a server.
- ```Client.py```: the client/user that will be connecting to the server to download a file.


<br>

## Explanation
In this section, I will explain the differences between each part/folder:

- **Part [ 1 ]** <br>
In the first part, simply the client-server application downloads an image file in different sizes using a single TCP connection.

- **Part [ 2 ]** <br>
The second part is the same of the first one, with some improvements. Before sending a file, it's getting divided into smaller packets and identify each of them, then send the packets separately. Due to that, the client will receive them and organize them according to the identifiers. Finally combine them and reconstruct them as the downloaded image.

- **Part [ 3 ]** <br>
In previous parts, file downloader used single TCP connection. In this part, there are multiple TCP connections between server and client (e.g. 5, 10, 20 or 50 connections). Of course the file is divided and transmitted over these threading connections, then sorted at client side to reconstruct them. The purpose was comparing and testifying the performance of having multi-threads.


<br>

## Usage
1. Run the server file ```Server.py```.
2. Now the server is listening to the port waiting for a user's connection.
3. Run the client file ```Client.py```.
4. Now you are connected. I have set the image ```Data.jpg``` as the file to be downloaded. Therefore, the user must type the file's name to request downloading it.
5. Done, and the file is downloaded in your Desktop!



