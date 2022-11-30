# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# This module contains the socket connection
import socket
import configparser


# class MyChatApplication:

#     host = ''
#     port = None
#     server = None

#     def EstablishConnection(self, host, port):
#         print("calling establish connection")
#         # starting the server
#         '''AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections'''
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server.bind((host, port))  # server is binding
#         self.server.listen()  # now its in listening mode

#     def GetConnectionDetails(self):
#         print("calling get connection details")
#         configObj = configparser.ConfigParser()
#         configObj.read('app_config_file.ini')
#         nwConnection = configObj['Network Connection']
#         # IP address of the server, in this case it is the localhost
#         HOST = nwConnection['HOST']
#         # use any available port less than 65535
#         PORT = int(nwConnection['PORT'])
#         return HOST, PORT

#     def __init__(self):
#         host, port = self.GetConnectionDetails()
#         self.EstablishConnection(host, port)
# HOST, PORT = GetConnectionDetails()
# EstablishConnection(HOST, PORT)


configObj = configparser.ConfigParser()
configObj.read('app_config_file.ini')
nwConnection = configObj['Network Connection']
# IP address of the server, in this case it is the localhost
HOST = nwConnection['HOST']
PORT = int(nwConnection['PORT'])  # use any available port less than 65535

# starting the server
'''AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# checks for TIME_WAIT state when connection is closed
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
