import socket
import os
import re

IP = socket.gethostbyname(socket.gethostname())
FORMAT = "utf-8"
#the function to check whether the file name is in correct format or not
def check_filename(file):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    # Pass the string in search
    # method of regex object.
    if (regex.search(file) == None and file is not None):
        return False
    else:
        return True
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
            print("Client has recieved", data_sent, "bytes")
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
            print("Client has sent", data_sent, "bytes")
    return data_sent

def client():
    connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_cmd = input("Enter the command for connection in the format: ftpclient <PORT> -")
    initial_cmd = connect_cmd.split(' ')
    if 'ftpclient' in initial_cmd[0] and len(initial_cmd) > 1:
        port = int(initial_cmd[1])
        try:
            connect.connect((IP, port))
            print("Connected to port:", port)
        except:
            print('No server found with ', port, ' port')

        try:
            while True:
                print("Please enter 'get <filename.extension>' command for getting the file from the sever or \n enter 'upload <filename.extension>' command for uploading the file to the sever or \n 'exit' to end the connection of the client with the server")
                function_cmd = input("Enter your command: ")
                #Parse the command
                command_split = function_cmd.split(' ')
                if len(command_split) == 2:
                    cmd, file = command_split
                elif len(command_split) == 1 and command_split[0] != 'exit':
                    cmd, file = None, None
                    print("Please enter file name as the second argument")
                else:
                    cmd, file = None, None
                #check if the file name does not have any special characters in it
                if(check_filename(file)):
                    print("Please enter valid file name")

                connect.send(function_cmd.encode(FORMAT))

                match cmd:
                    case 'upload':
                        #give the path of the file along with it's directory 'files' as the first argument
                        f_name = os.path.join('files', file)
                        #check if the file exists in the given path
                        if os.path.exists(f_name):
                            #get the size of the file given
                            file_size = os.path.getsize(f_name)
                            connect.send(f"SIZE {file_size}".encode(FORMAT))
                            if connect.recv(1024).decode(FORMAT) == 'OK':
                                #call the function to break the data into chunks and upload the file
                                sent_bytes = receive_data(f_name, connect)
                                print("The upload command is done. The client has uploaded a total of ", sent_bytes, "bytes to the server")
                        else:
                            print("The given file is not present in the path")
                            connect.send("The file is not present in the path".encode(FORMAT))
                    case 'get':
                        # give the path of the file along with it's directory 'files' as the first argument
                        f_name = os.path.join('files', f"new{file}")
                        receiver = connect.recv(1024).decode(FORMAT)
                        if 'SIZE' in receiver:
                            connect.send('OK'.encode(FORMAT))
                            #get the total number of size in bytes of the file given
                            total_size = int(receiver.split(' ')[1])
                            # call the function to break the data into chunks and get the file
                            sent_bytes = send_data(f_name, connect, total_size)
                            print("The get command is done. The client has recieved a total of ", sent_bytes, "bytes from the server")
                        else:
                            print(receiver)
                    case 'exit':
                        #close the connection of the client and the server
                        connect.close()
                        print("The connection between the client and server has been ended")
                        return

        except KeyboardInterrupt:
            print("The connection between the client and server will be ended now")
            #End the connection of the client and server whenever a keyboard interrupt occurs
            connect.send('exit'.encode(FORMAT))
            connect.close()
            return

        except:
            print('The connection between the client and server has been ended')
    else:
        #prompt the user to enter the connection command in valid format
        print('Please enter the command for connection in the valid format: ftpclient <PORT> -')
        return

if __name__ == "__main__":
    client()
