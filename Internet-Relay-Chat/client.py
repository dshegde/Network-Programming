import socket
import sys
import threading  # for multiple process

import data

from connection import Connection


conn_obj = Connection('app_config_file.ini')
nickname = input("Enter your nickname: ")
threads = []

# To start the connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# TODO: connect_ex does not raise an exception, instead it returns an error code
client.connect_ex((conn_obj.get_host(), conn_obj.get_port()))


def receive():
    """This function is to recieve and send messages from the server"""
    while True:
        try:
            message = client.recv(data.BUFFER_SIZE).decode('utf-8')
            if not message:
                print("Connection to the server is lost... Exiting!!")
                client.close()
                sys.exit()
            elif message == data.NICKNAME_CODE:
                client.send(nickname.encode('utf-8'))
            elif message == data.EXIT_CODE:
                client.send('Client is exiting'.encode('utf-8'))
                client.close()
                print('Type \'exit\' again to confirm')
                sys.exit(0)
            else:
                print(message)
        except Exception as e:
            print('An exception occured at the CLIENT side')
            client.close()
            sys.exit()


def write():
    """This function is to write to the server"""
    while True:
        message = '{} {}'.format(nickname, input(''))
        try:
            client.send(message.encode('utf-8'))
        except:
            sys.exit(0)


receive_thread = threading.Thread(target=receive)
receive_thread.start()
threads.append(receive_thread)
write_thread = threading.Thread(target=write)
write_thread.start()
threads.append(write_thread)
