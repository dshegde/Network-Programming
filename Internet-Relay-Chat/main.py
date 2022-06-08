# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


#This module contains the socket connection
import socket
import threading #for multiple process


host = '127.0.0.1' #localhost
port = 65000  #use any available port less than 65535

#starting the server
#AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections
#AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) #server is binding
server.listen() #now its in listening mode


instructions = '\nApplication Menu:\n' \
               '1.menu (lists the menu)\n' \
               '2.list (lists all the available rooms)\n' \
               '3.create roomname - like "create room1" (creates a new room)\n' \
               '4.join roomname - like "join room1" (joins the room)\n' \
               '5.switch roomname - like "switch room2" (switches the room)\n' \
               '6.leave (leave from the room) \n' \
               '7.personal name message - like "personal nickname hello" (sends personal message)\n' \
               '8.exit (exits the client app)\n'


#now create a empty list and dict for data storage
clients = []
nicknames = []
roomdetails = {}
users = {}
users_in_room = {}

#to broadcast the message
def broadcast(message, roomname):
    for client in roomdetails[roomname].peoples:
        msg = '['+roomname+'] '+message
        client.send(msg.encode('utf-8'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
