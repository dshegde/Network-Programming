import socket

import constants

from connection import Connection


conn_obj = Connection('app_config_file.ini')

# IP address of the server, in this case it is the localhost
HOST = conn_obj.get_host()
PORT = conn_obj.get_port()  # use any available port less than 65535

# starting the server
"""AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# checks for TIME_WAIT state when connection is closed
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))  # server is binding
server.listen()  # now it is in listening mode


def broadcast(message, roomname):
    """This function is to broadcast the message to all the clients and server available in the network connection"""
    for client in constants.room_details[roomname].people:
        msg = '['+roomname+'] '+message
        client.send(msg.encode('utf-8'))
