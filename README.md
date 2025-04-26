# Multi-Client Chat Server

A Python-based chat server and client application that supports multiple clients connecting simultaneously to a server. Clients can send messages to each other, and the server can broadcast messages to all connected clients. This project utilizes **socket**, **threading**, **sys**, **time**, and **platform** libraries.

## Features

- Multi-client support: multiple clients can connect to the server and chat simultaneously.
- Real-time messaging: clients can send messages to the server, and the server broadcasts messages to all connected clients.
- Identifies which client is sending which message.
- Multi-threaded to allow multiple clients to connect at the same time.
- Cross-platform: supports Windows, Linux, and macOS.

## Technologies

- Python 3.x
- Socket (for client-server communication)
- Threading (for handling multiple clients simultaneously)
- Sys (for handling system-specific parameters)
- Time (for managing time-related functions)
- Platform (for checking the client's operating system)

## Setup and Usage

### Server Side

1. Ensure Python 3.x is installed on your system.
2. Run the server script to listen for incoming client connections:

```bash
python server.py
```
3. The server will listen for incoming connections from clients and manage the communication between them.

### Client Side
1. Ensure Python 3.x is installed on your system.
2. Run the client script to connect to the server:
```
python client.py
```
3. Once connected, you can start sending messages to the server. The server will broadcast these messages to all connected clients.

Note: Ensure that both the server and clients are on the same network or the server is accessible by the clients.
