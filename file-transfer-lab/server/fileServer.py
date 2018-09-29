#! /usr/bin/env python3

import sys, re, socket, os
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
    sock, addr = lsock.accept()
    print("connection rec'd from", addr)
    rc = os.fork()
    if rc < 0:
        print("Failed to fork")
        continue
    elif rc == 0:
        payload = framedReceive(sock, debug)
        if debug: print("rec'd: ", payload)
        if os.path.exists(payload):
            if debug: print("FILE ALREADY EXISTS")
            framedSend(sock, b"File exists")
            sock.shutdown(socket.SHUT_RDWR)
            sys.exit(0)
        else:
            framedSend(sock, b"Ready")
            with open(payload, 'w') as file:
                if debug: print("OPENED FILE")
                while True:
                    payload = framedReceive(sock, debug)
                    if debug: print("RECEIVED PAYLOAD: %s" % payload)
                    if not payload:
                        if debug: print("DONE WRITING INSIDE NOT PAYLOAD")
                        sock.shutdown(socket.SHUT_RDWR)
                        if debug: print("CLOSED THE SOCKET")
                        sys.exit(0)
                    else:
                        file.write(payload.decode())
                        if debug: print("WROTE THE PAYLOAD TO FILE")
    else:
        print("listening on:", bindAddr)
        # sock.close()
