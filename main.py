#!/usr/bin/env python
import time
import pickle
import socket
import threading
import sys
import signal
import bz2
import os
import pwd
import grp


roll = open('rickroll.ascii', 'r').readlines()
# for char in roll:
#     print(char)

listensock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensock.bind(("0.0.0.0", 1337))
listensock.listen()

# Try to drop privileges having bound to the port
try:
    os.setgroups([])
    os.setgid(grp.getgrnam("nogroup").gr_gid)
    os.setuid(pwd.getpwnam("nobody").pw_uid)
except OSError:
    print("Failed to drop permissions")
    sys.exit()


def dataRecv(client, addr):
    print(f"[+] Rickrolling: {addr[0]}")
    for char in roll:
        time.sleep(0.001)
        try:
            client.send(char.encode('utf-8'))
        except:
            return
    client.send("You have been rickrolled from Evangelospro!!!".encode())
    client.close()

print("Ready to roll!!!")
while True:
    try:
        client, addr = listensock.accept()
    except KeyboardInterrupt:
        listensock.close()
        sys.exit()
    except Exception:
        continue
    thread = threading.Thread(target=lambda:dataRecv(client, addr), daemon=True)
    thread.start()

