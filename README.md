# Internet Relay Chat

## Project Overview:

Internet Relay Chat (IRC) is a chat system on the Internet. It is a text-based chat (instant messaging) system. IRC is generally designed for group communication in discussion forums, called channels, but also allows one-on-one communication via private messages as well as chat and data transfer, including file sharing.

This project implements features like - connecting clients with servers, creating a chat room for communication between individuals/in groups, joining a channel, leaving the channel, switching between rooms, listing members of room, disconnecting from server, message handler that guides user for next actions like join, leave, list of rooms and many more.

Our motive is to learn and implement as many features as possible to accomplish a good project which can be useful for a great communication between clients and servers.

## Functionalities supported by the application

* List Menu
* List available rooms
* Create new room
* Join room
* Switch room
* Send private message
* Leave room
* Exit application

## How to Run

Download the repository <br /> <br />
Run the `requirements.txt` as shown below with the environment name of your choice<br /> <br />
`conda create --name <env> --file requirements.txt` <br /> <br />
Run the `app_config_file_generator.py` to generate the app_config_file.ini file <br /> <br />
`python app_config_file_generator.py`<br /> <br />
Open a terminal for the server and as many terminals required for as many clients. <br /> <br />
Start the server <br /> <br />
`python server.py` <br /> <br />
Once the server is running, start the client <br /> <br />
`python client.py` <br /> <br />

## Sample screenshots for running the application

<img src="Images/readme_server.png" width="500"><br /> <br /><br /> <br />
<img src="Images/readme_client.png" width="500"><br /> <br />

## Reference

* [TCP chat in python](https://www.neuralnine.com/tcp-chat-in-python/)
