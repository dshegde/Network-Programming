import threading  # for multiple process
import socket
import sys
import configparser
from helper import *

configObj = configparser.ConfigParser()
configObj.read('app_config_file.ini')
nwConnection = configObj['Network Connection']
nickname = input("Enter your nickname: ")
threads = []
# To start the connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect_ex does not raise an exception, instead it returns an error code
client.connect_ex((nwConnection['HOST'], int(nwConnection['PORT'])))


'''This function is to recieve and send messages from the server'''


def receive():
    while True:
        try:
            message = client.recv(Constants.BUFFER_SIZE).decode('utf-8')
            if not message:
                print("Connection to the server is lost. Exiting!!")
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                sys.exit()
            elif message == Constants.NICKNAME_CODE:
                client.send(nickname.encode('utf-8'))
            elif message == Constants.EXIT_CODE:
                client.send('Client is exiting'.encode('utf-8'))
                client.close()
                print('Type \'exit\' again to confirm')
                client.shutdown(socket.SHUT_RDWR)
                exit()
            else:
                print(message)
        except Exception as e:
            print('Server not responding')
            client.close()
            sys.exit()


def write():
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
