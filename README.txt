Implementation of FTP client and server

Project Aim:
The task is to implement an FTP client and FTP server with multiple threads where the file should be transferred in chunks of 1k bytes

Language Used:
Python

Steps for Execution:
Server:
python server.py
Client:
python client.py

Functionalities:
The three main functionalities implemented are as follows:
1. 'upload <filename>': The client can upload a file to the server in chunks of 1k bytes
2. 'get <filename>': The client can get a file from the server in chunks of 1k bytes
3. 'exit': The connection between the client and server will be ended

The workflow of the program:
1. First the server is run on a port like 5106
2. Two clients are run on the same port by entering the command "ftpclient 5106" so that it will be connected to the server
3. If the port number is not the same, an error will be prompted. Else, the flow continues
4. The user will be asked with 3 options to upload file, get file or exit
5. The initial command will be taken and split to check the file name validity from a helper function check_filename written in client
6. If the user enters upload, then the file is taken from the path given and uploaded to the server using the helper function receive_data
7. If the user enters get, then the file is taken from the path given and uploaded to the server using the helper function send_data
8. If the user enters exit, then the connection from the server and client is closed
9. If a keyboard interrupt occurs, we handle the error by giving a prompt to the user and closing the connection
10. If any other exception occurs, the user will be prompted with new message to enter valid commands
11. Finally, using multi threads, multiple clients are run on the same server and upload and get are done successfully.
