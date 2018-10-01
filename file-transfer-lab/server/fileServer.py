#! /usr/bin/env python3

import os
import socket
import sys

sys.path.append("../../lib")       # for params
import params
from framedSock import framedReceive, framedSend

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False)  # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap["listenPort"]

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while 1:
    sock, addr = lsock.accept()                             # Wait for a connection.
    print("connection rec'd from", addr)
    print("Child will take care of the request")
    rc = os.fork()                                          # Once a connection is made fork of a child to take care of the request.
    if rc < 0:                                              # If unable to fork wait for another connection.
        print("Failed to fork")
        continue
    elif rc == 0:                                           # Child
        payload = framedReceive(sock, debug)                # Receive the request.
        if debug: print("rec'd: ", payload)
        if os.path.exists(payload):                         # Check if the file is in the server already.
            if debug: print("FILE ALREADY EXISTS")
            framedSend(sock, b"File exists")                # Send the file exists.
            sock.shutdown(socket.SHUT_RDWR)                 # Shutdown the socket.
            sys.exit(0)                                     # Kill the child.
        else:
            framedSend(sock, b"Ready")                      # Send the file is ready to receive the file.
            with open(payload, 'w') as file:                # Open file to receive
                if debug: print("OPENED FILE")
                while True:
                    payload = framedReceive(sock, debug)    # Receive the file.
                    if debug: print("RECEIVED PAYLOAD: %s" % payload)
                    if not payload:                         # Check if done receiving file.
                        if debug: print("DONE WRITING INSIDE NOT PAYLOAD")
                        sock.shutdown(socket.SHUT_RDWR)     # Shutdown the socket
                        if debug: print("CLOSED THE SOCKET")
                        sys.exit(0)                         # Kill the child
                    else:
                        file.write(payload.decode())        # Write the data to the file.
                        if debug: print("WROTE THE PAYLOAD TO FILE")
    else:                                                   # Parent
        print("listening on:", bindAddr)
