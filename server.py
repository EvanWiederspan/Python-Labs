# This file should be run first so that the client has something to attach to

import socket
from time import ctime
from re import split
from sys import argv as args

import serverTools

host = ""
# optionally takes port from command line
port = args[2] if len(args) >= 3 else 21567
bufSize = 1024
addr = (host, port)

# Load tools into dictionary
# Read the exports list in serverTools and create a string -> function dictionary from it
tools = {t:getattr(serverTools, t) for t in serverTools.exports}
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
        serv.bind(addr)
        serv.listen(5)
        print("Waiting for connection...")
        with serv.accept()[0] as client:
            print("Client connected")
            # helper function to save typing
            send = lambda data: client.send(bytes(data, 'utf-8'))
            while True:
                data = client.recv(bufSize).decode('utf-8')
                # disconnect after receiving empty string
                # and wait for a new connection
                if not data:
                    print('Client disconnecting')
                    break
                # split into pieces by whitespace to get command and parameters
                commands = split(r'\s+', data.strip())
                try:
                    if commands[0] in tools:
                        send(tools[commands[0]](*commands[1:]))
                    else: # not valid command, send timestamp and data back
                        send("{}: Received '{}'".format(ctime(), data))
                # covers incorrect parameters, either number given or type
                except (TypeError, ValueError):
                    send("Error: Invalid parameters '{}' for command '{}'".format(" ".join(commands[1:]), commands[0]))
                # exit the server
                # sockets are closed automatically by with statements
                except serverTools.ExitServerException:
                    print("Exiting Server")
                    quit()
                # catch all errors so it doesn't crash if input is bad
                except:
                    send("Error running '{}'".format(data))
        