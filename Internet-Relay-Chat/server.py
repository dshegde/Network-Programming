import threading

import data

from main import *


class User:
    def __init__(self, name):
        self.name = name
        self.room_details = []
        self.this_room = ''


class Room:
    def __init__(self, name):
        self.people = []
        self.nicknames = []
        self.name = name


def list_all_room_details(nickname):
    name = data.users[nickname]
    if len(data.room_details) == 0:
        name.send('No rooms available\n'.encode('utf-8'))
    else:
        reply = "List of available room_details: \n"
        name.send(f'{reply}'.encode('utf-8'))
        for room in data.room_details:
            name.send(f'{data.room_details[room].name}\n'.encode('utf-8'))


def create_room(nickname, room_name):
    name = data.users[nickname]
    user = data.users_in_room[nickname]
    if not room_name:
        name.send(
            'Enter a roomname! you have not entered a roomname\n'.encode('utf-8'))
    elif room_name not in data.room_details:
        room_obj = Room(room_name)
        data.room_details[room_name] = room_obj
        room_obj.people.append(name)
        room_obj.nicknames.append(nickname)
        user.this_room = room_name
        user.room_details.append(room_obj)
        name.send(f'{room_name} created\n'.encode('utf-8'))
    else:
        if room_name in user.room_details:
            name.send(
                'Room with the same name already exists, please choose another name for the room\n'.encode('utf-8'))


def join_room(nickname, room_name):
    name = data.users[nickname]
    user = data.users_in_room[nickname]
    if len(data.room_details) == 0:
        name.send(
            'No rooms are available to join. Create a room first!\n'.encode('utf-8'))
    else:
        room = data.room_details[room_name]
        if room_name in user.room_details:
            name.send('You are already in the room\n'.encode('utf-8'))
        else:
            room.people.append(name)
            room.nicknames.append(nickname)
            user.this_room = room_name
            user.room_details.append(room)
            broadcast(f'{nickname} joined the room', room_name)


def personal_message(message):
    args = message.split(" ")
    user = args[2]
    sender = data.users[args[0]]
    sender.send('entered personal message function'.encode('utf-8'))
    if user not in data.users:
        sender.send('User not found\n'.encode('utf-8'))
    else:
        reciever = data.users[user]
        msg = ' '.join(args[3:])
        reciever.send(f'[personal message] {args[0]}: {msg}'.encode('utf-8'))
        sender.send(f'[personal message] {args[0]}: {msg}'.encode('utf-8'))


def switch_room(nickname, room_name):
    user = data.users_in_room[nickname]
    name = data.users[nickname]
    room = data.room_details[room_name]
    if room_name == user.this_room:
        name.send(
            'You are already in the room, choose another available room to change\n'.encode('utf-8'))
    elif room not in user.room_details:
        name.send(
            'Change of room not available, you are not part of the room\n'.encode('utf-8'))
    else:
        user.this_room = room_name
        name.send(f'Switched to {room_name}\n'.encode('utf-8'))


def leave_room(nickname):
    user = data.users_in_room[nickname]
    name = data.users[nickname]
    print(name)
    if user.this_room == '':
        name.send('You are not part of any room\n'.encode('utf-8'))
    else:
        room_name = user.this_room
        room = data.room_details[room_name]
        user.this_room = ''
        user.room_details.remove(room)
        data.room_details[room_name].people.remove(name)
        data.room_details[room_name].nicknames.remove(nickname)
        broadcast(f'{nickname} left the room\n', room_name)
        name.send('You left the room\n'.encode('utf-8'))


def remove_client(nickname):
    data.nicknames.remove(nickname)
    client = data.users[nickname]
    user = data.users_in_room[nickname]
    user.this_room = ''
    for room in user.room_details:
        print(room.name)
        room.people.remove(client)
        print(room.people)
        room.nicknames.remove(nickname)
        print(room.nicknames)
        broadcast(f'{nickname} left the room\n', room.name)


def handle(client):
    nickname = ''
    while True:
        try:
            message = client.recv(data.BUFFER_SIZE).decode('utf-8')
            args = message.split(" ")
            name = data.users[args[0]]
            nickname = args[0]
            if 'menu' in message:
                name.send(data.MENU_LIST.encode('utf-8'))
            elif 'list' in message:
                list_all_room_details(args[0])
            elif 'create' in message:
                create_room(nickname, ' '.join(args[2:]))
            elif 'join' in message:
                join_room(nickname, ' '.join(args[2:]))
            elif 'leave' in message:
                leave_room(nickname)
            elif 'switch' in message:
                switch_room(nickname, args[2])
            elif 'personal' in message:
                personal_message(message)
            elif 'exit' in message:
                remove_client(nickname)
                name.send('EXIT'.encode('utf-8'))
                print(client.recv(data.BUFFER_SIZE).decode('utf-8'))
            else:
                if data.users_in_room[nickname].this_room == '':
                    name.send('Wrong command!\n'.encode('utf-8'))
                else:
                    msg = ' '.join(args[1:])
                    broadcast(f'{nickname}: {msg}',
                              data.users_in_room[nickname].this_room)

        except Exception as e:
            data.clients.remove(client)
            client.close()
            print(f'Client - {nickname} left')
            if nickname in data.nicknames:
                remove_client(nickname)
            break


# TODO: server side - handle keyboard interrupt exception
# def signal_handler(sig, frame):
#     print('\n -------- Stopping Server --------')
#     sys.exit(0)


def recieve():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}\n')
        print(client)
        client.send(data.NICKNAME_CODE.encode('utf-8'))
        nickname = client.recv(data.BUFFER_SIZE).decode('utf-8')
        data.nicknames.append(nickname)
        data.clients.append(client)
        user_obj = User(nickname)
        data.users_in_room[nickname] = user_obj
        data.users[nickname] = client
        print(f'Nickname of the client is {nickname}\n')
        client.send('\nYAY! Connected to the server!\n'.encode('utf-8'))
        client.send(data.MENU_LIST.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        # TODO: capture Ctrl C keyboard interrupt
        # if (signal.signal(signal.SIGINT, signal_handler)):
        #     signal.pause()


print('Server is listening...')
recieve()
