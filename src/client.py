import xmlrpc.client
import threading
from time import sleep
import random
import sys

serverIps = []
serverPorts = []
serverCount = -1

with open("./src/config.txt", 'r') as f:
    for line in f:
        serverCount+=1
        line = line.rstrip('\n')
        s = line.split(':')
        serverIps.append(s[0])
        serverPorts.append(s[1])

try:
    id = sys.argv[1]
except IndexError:
    print("ERROR: define a client id.")
    sys.exit(0)

def function_call():
    while True:
        randomServer = random.randint(0,serverCount)
        server = xmlrpc.client.ServerProxy(f"http://{serverIps[randomServer]}:{serverPorts[randomServer]}")
        randomOp = random.randint(1,100)
        if randomOp<=70:
            print(server.read(id))
            sleep(0.1)
        if 70<randomOp<=90:
            print(server.insert(id))
            sleep(0.1)
        if 90<randomOp<=100:
            print(server.delete(id))
            sleep(0.1)

threading.Thread(target=function_call).start()