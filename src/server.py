import threading
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread, Semaphore
import sys
import time, calendar
from time import sleep
import xmlrpc.client

try:
    ip = sys.argv[1]
    port = sys.argv[2]
    lockServerIp = sys.argv[3]
    lockServerPort = sys.argv[4]
except IndexError:
    print("ERROR: IP or port not defined when passing arguments.")
    sys.exit(0)

lockServer = xmlrpc.client.ServerProxy(f"http://{lockServerIp}:{lockServerPort}")

def read(id):
    if lockServer.checkDelete():
        #Retorna ao cliente
        return "O servidor está ocupado no momento"
    else:
        lockServer.queueOp(1)
        with open('./src/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=READ, STATUS=STARTING\n')
        sleep(0.1)
        with open('./src/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=READ, STATUS=FINISHING\n')
        lockServer.dequeueOp()
        return "Leitura efetuada"

def insert(id):
    if lockServer.checkDelete() or lockServer.checkInsert():
        #Retorna ao cliente
        return "O servidor está ocupado no momento"
    else:
        print('Locking insert')
        lockServer.changeInsert()
        lockServer.queueOp(2)
        with open('./src/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=INSERT, STATUS=STARTING\n')
        sleep(0.1)
        with open('./src/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=INSERT, STATUS=FINISHING\n')
        print('Unlocking insert')
        lockServer.changeInsert()
        lockServer.dequeueOp()
        return "Insert efetuado"
        

def delete(id):
    if not lockServer.emptyQueue():
        return "O servidor está ocupado no momento"
    elif lockServer.checkDelete() or lockServer.checkInsert():
        #Retorna ao cliente
        return "O servidor está ocupado no momento"
    else:
        print('Locking delete')
        lockServer.changeDelete()
        lockServer.queueOp(3)
        with open('./src/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=DELETE, STATUS=STARTING\n')
        sleep(0.1)
        with open('./src/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=DELETE, STATUS=FINISHING\n')
        print('Unlocking delete')
        lockServer.changeDelete()
        lockServer.dequeueOp()
        return "Delete efetuado"

with SimpleXMLRPCServer((ip, int(port))) as server:
    server.register_function(read)
    server.register_function(insert)
    server.register_function(delete)
    print(f'Serving XML-RPC on {ip} port {port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)