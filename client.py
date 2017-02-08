# Evan Wiederspan
# Advanced Python Lab #5: Client / Server
# Program split into three files

import socket
from sys import argv as args

host = '127.0.0.1'
# optionally take port from commandline
port = args[2] if len(args) >= 3 else 21567
bufSize = 1024
addr = (host, port)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect(addr)
    # should catch if port is of wrong type
    except TypeError:
        print("Invalid port '{}'".format(port))
    while True:     
        data = input('> ')
        s.send(bytes(data, 'utf-8'))
        # socket closed by with statement
        if data == "EXITSERVER" or not data:
            break
        recData = s.recv(bufSize)
        if not recData:
            break
        print(recData.decode('utf-8'))