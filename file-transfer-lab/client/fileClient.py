#! /usr/bin/env python3

# Echo client program
import socket, sys, re
from lib.framedSock import framedSend, framedReceive
sys.path.append("../../lib")       # for params
import params


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('-f', '--file'), "file", "constitution.txt")
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug, file_name  = paramMap["server"], paramMap["usage"], paramMap["debug"], paramMap["file"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

framedSend(s, file_name.encode(), debug)
response = framedReceive(s, debug)
if response.decode() == "File exists":
    print("The file is already in the server. Closing the socket")
    s.close()
else:
    with open(file_name, 'r') as file:
        if debug: print("OPENED FILE")
        data = file.read(100)
        while data:
            framedSend(s, data.encode(), debug)
            data = file.read(100)
        s.shutdown(socket.SHUT_WR)
