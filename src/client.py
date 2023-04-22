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

reads = 70
inserts = 20
deletes = 10

if len(sys.argv)>2:
    if len(sys.argv[2:])<3:
        print("ERROR: define the chance of all operations if you want to define it.")
        sys.exit(0)

counter = 0
for arg in sys.argv[2:]:
    if counter == 0:
        reads = int(arg)
    if counter == 1:
        inserts = int(arg)
    if counter == 2:
        deletes = int(arg)
    counter += 1

def function_call():
    while True:
        randomServer = random.randint(0,serverCount)
        server = xmlrpc.client.ServerProxy(f"http://{serverIps[randomServer]}:{serverPorts[randomServer]}")
        randomOp = random.randint(1,100)
        if randomOp<=reads:
            print(server.read(id))
            sleep(0.1)
        if reads<randomOp<=reads+inserts:
            print(server.insert(id))
            sleep(0.1)
        if reads+inserts<randomOp<=reads+inserts+deletes:
            print(server.delete(id))
            sleep(0.1)

threading.Thread(target=function_call).start()