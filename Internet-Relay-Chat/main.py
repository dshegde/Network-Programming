# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# This module contains the socket connection
import socket
import configparser


configObj = configparser.ConfigParser()
configObj.read('app_config_file.ini')
nwConnection = configObj['Network Connection']
# IP address of the server, in this case it is the localhost
HOST = nwConnection['HOST']
PORT = int(nwConnection['PORT'])  # use any available port less than 65535

# starting the server
'''AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))  # server is binding
server.listen()  # now its in listening mode

# Create an empty list and dictionary for data storage
clients = []
nicknames = []
roomdetails = {}
users = {}
users_in_room = {}

# to broadcast the message


def broadcast(message, roomname):
    for client in roomdetails[roomname].peoples:
        msg = '['+roomname+'] '+message
        client.send(msg.encode('utf-8'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
