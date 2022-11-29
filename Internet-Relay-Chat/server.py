# This python file contains all the functionalities

from main import *
from helper import *

# this function is to instatiate by creating objects


class User:
    def __init__(self, name):
        self.name = name
        self.roomdetails = []
        self.thisRoom = ''


class Room:
    def __init__(self, name):
        self.peoples = []
        self.nicknames = []
        self.name = name


'''This function is to list the available room details'''


def list_all_roomdetails(nickname):
    name = users[nickname]
    print(len(roomdetails))
    if len(roomdetails) == 0:
        name.send('No rooms available\n'.encode('utf-8'))
    else:
        reply = "List of available roomdetails: \n"
        name.send(f'{reply}'.encode('utf-8'))
        for room in roomdetails:
            print(roomdetails[room].name)
            print(roomdetails[room].nicknames)
            name.send(f'{roomdetails[room].name}\n'.encode('utf-8'))


'''This function is to create new rooms'''


def create_room(nickname, room_name):
    name = users[nickname]
    user = users_in_room[nickname]
    if not room_name:
        name.send(
            'Enter a roomname! you have not entered a roomname\n'.encode('utf-8'))
    elif room_name not in roomdetails:
        room = Room(room_name)
        roomdetails[room_name] = room
        room.peoples.append(name)
        room.nicknames.append(nickname)
        user.thisRoom = room_name
        user.roomdetails.append(room)
        name.send(f'{room_name} created\n'.encode('utf-8'))
    else:
        #room = roomdetails[room_name]
        if room_name in user.roomdetails:
            name.send(
                'Room with the same name already exists, please choose another name for the room\n'.encode('utf-8'))


'''This function is to join to other rooms'''


def join_room(nickname, room_name):
    name = users[nickname]
    user = users_in_room[nickname]
    print(len(roomdetails))
    if len(roomdetails) == 0:
        name.send(
            'No rooms are available to join. Create a room first!\n'.encode('utf-8'))
    else:
        room = roomdetails[room_name]
        if room_name in user.roomdetails:
            name.send('You are already in the room\n'.encode('utf-8'))
        else:
            room.peoples.append(name)
            room.nicknames.append(nickname)
            user.thisRoom = room_name
            user.roomdetails.append(room)
            broadcast(f'{nickname} joined the room', room_name)


'''This function is to personally send messages'''


def personalMessage(message):
    args = message.split(" ")
    user = args[2]
    sender = users[args[0]]
    sender.send('entered personal message function'.encode('utf-8'))
    if user not in users:
        sender.send('User not found\n'.encode('utf-8'))
    else:
        reciever = users[user]
        msg = ' '.join(args[3:])
        reciever.send(f'[personal message] {args[0]}: {msg}'.encode('utf-8'))
        sender.send(f'[personal message] {args[0]}: {msg}'.encode('utf-8'))


'''This function is to switch to other room'''


def switch_room(nickname, roomname):
    user = users_in_room[nickname]
    name = users[nickname]
    room = roomdetails[roomname]
    if roomname == user.thisRoom:
        name.send(
            'You are already in the room, choose another available room to change\n'.encode('utf-8'))
    elif room not in user.roomdetails:
        name.send(
            'Change of room not available, you are not part of the room\n'.encode('utf-8'))
    else:
        user.thisRoom = roomname
        name.send(f'Switched to {roomname}\n'.encode('utf-8'))


'''This function is to leave the room'''


def leave_room(nickname):
    user = users_in_room[nickname]
    name = users[nickname]
    if user.thisRoom == '':
        name.send('You are not part of any room\n'.encode('utf-8'))
    else:
        roomname = user.thisRoom
        room = roomdetails[roomname]
        user.thisRoom = ''
        user.roomdetails.remove(room)
        roomdetails[roomname].peoples.remove(name)
        roomdetails[roomname].nicknames.remove(nickname)
        broadcast(f'{nickname} left the room\n', roomname)
        name.send('You left the room\n'.encode('utf-8'))


'''This function is to exit the server/application'''


def remove_client(nickname):
    nicknames.remove(nickname)
    client = users[nickname]
    user = users_in_room[nickname]
    user.thisRoom = ''
    for room in user.roomdetails:
        print(room.name)
        room.peoples.remove(client)
        print(room.peoples)
        room.nicknames.remove(nickname)
        print(room.nicknames)
        broadcast(f'{nickname} left the room\n', room.name)


'''This function handles the client when it connects to the server like recv/send messages'''


def handle(client):
    nickname = ''
    while True:
        try:
            message = client.recv(Helper.BUFFER_SIZE).decode('utf-8')
            print("Message is!!!!!!")
            print(message)
            args = message.split(" ")
            name = users[args[0]]
            nickname = args[0]
            if 'menu' in message:
                name.send(instructions.encode('utf-8'))
            elif 'list' in message:
                list_all_roomdetails(args[0])
            elif 'create' in message:
                create_room(nickname, ' '.join(args[2:]))
            elif 'join' in message:
                join_room(nickname, ' '.join(args[2:]))
            elif 'leave' in message:
                leave_room(nickname)
            elif 'switch' in message:
                switch_room(nickname, args[2])
            elif 'personal' in message:
                personalMessage(message)
            elif 'exit' in message:
                remove_client(nickname)
                name.send('EXIT'.encode('utf-8'))
                print(client.recv(Helper.BUFFER_SIZE).decode('utf-8'))
                # name.close()
            else:
                if users_in_room[nickname].thisRoom == '':
                    name.send('You are not part of any room\n'.encode('utf-8'))
                else:
                    msg = ' '.join(args[1:])
                    broadcast(f'{nickname}: {msg}',
                              users_in_room[nickname].thisRoom)

        except Exception as e:
            clients.remove(client)
            client.close()
            print(f'Client - {nickname} left')
            if nickname in nicknames:
                remove_client(nickname)
            # if nick in nicknames:
            #     nicknames.remove(nick)
            break

# main


def recieve():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}\n')
        print(client)
        client.send(Helper.NICKNAME_CODE.encode('utf-8'))
        nickname = client.recv(Helper.BUFFER_SIZE).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        user = User(nickname)
        users_in_room[nickname] = user
        users[nickname] = client
        print(f'Nickname of the client is {nickname}\n')
        client.send('\nYAY! Connected to the server!\n'.encode('utf-8'))
        client.send(instructions.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Server is listening...')
recieve()
