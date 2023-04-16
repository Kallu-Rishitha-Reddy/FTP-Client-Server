import socket
import os
#import thread
from threading import Thread

SIZE = 1024
PORT = 5109
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
FORMAT = "utf-8"
#the function to send data from the file by breaking the file size into blocks of 1024 bytes
def send_data(file, connect, total_size):
    data_sent = 0
    #opening the file in write mode
    with open(file, 'wb+') as fileContent:
        while True:
            #dividing the data into blocks of 1024 byte size
            data_block = connect.recv(1024)
            #writing the data from the blocks into the file
            fileContent.write(data_block)
            data_sent = data_sent + len(data_block)
            print("Server has recieved ",data_sent, "bytes")
            #break the loop when the data sent is equal to total size of the file
            if total_size == data_sent:
                break
    return data_sent
#the function to receive data from the file by breaking the file size into blocks of 1024 bytes
def receive_data(file, connect):
    data_sent = 0
    #opening the file in read mode
    with open(file, 'rb+') as fileContent:
        while True:
            #dividing the data into blocks of 1024 byte size
            data_block = fileContent.read(1024)
            if not data_block:
                break
            connect.sendall(data_block)
            data_sent = data_sent + len(data_block)
            print("Server has sent ",data_sent, "bytes")
    return data_sent

#function for listening to a new client
def newClient(connection, address):
    while True:
        cmd = connection.recv(1024).decode(FORMAT).split(' ')
        # Parse the initial command
        if len(cmd) == 2:
            cmd, file = cmd
        else:
            cmd, file = None, None

        if file is not None:
            match cmd:
                case 'upload':
                    f_name = os.path.join('files', f"new{file}")
                    receiver = connection.recv(1024).decode(FORMAT)
                    if 'SIZE' in receiver:
                        connection.send('OK'.encode(FORMAT))
                        total_size = int(receiver.split(' ')[1])
                        sent_bytes = send_data(f_name, connection, total_size)
                        print("The upload command is done. The server has recieved a total of ", sent_bytes,
                              "bytes from the client")
                    else:
                        print(receiver)

                case 'get':
                    f_name = os.path.join('files', file)
                    if os.path.exists(f_name):
                        file_size = os.path.getsize(f_name)
                        connection.send(f"SIZE {file_size}".encode(FORMAT))
                        if connection.recv(1024).decode(FORMAT) == 'OK':
                            sent_bytes = receive_data(f_name, connection)
                            print("The get command is done. The server has sent a total of ", sent_bytes,
                                  "bytes to the client")
                    else:
                        print("The given file is not present in the path")
                        connection.send("The file is not present in the path".encode(FORMAT))

                case 'exit':
                    # The connection of the client and server should be closed
                    connection.close()
                    print("The connection between the client and server has been ended")
                    break
    #closing the connection
    connection.close()

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("The server has been started")
    server.bind(ADDR)
    try:
        server.listen()
        print(f"The server is listening on {PORT} port")

        while True:
            connection, address = server.accept()
            print(f"A connection from the address {address} has been made successfully")
            #run the thread command by calling the new client function and passing the arguments
            Thread(target=newClient, args=(connection, address), daemon=True).start()
        #the server will be closed
        server.close()

    except:
        print("The server will be shutting down now")
        #The server will be closed
        server.close()

if __name__ == "__main__":
    server()
