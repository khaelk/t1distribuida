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
        with open('./server/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=WRITE, STATUS=STARTING\n')
        sleep(5)
        with open('./server/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=WRITE, STATUS=FINISHING\n')
        return "Leitura efetuada"

def insert(id):
    if lockServer.checkDelete() or lockServer.checkInsert():
        #Retorna ao cliente
        return "O servidor está ocupado no momento"
    else:
        print('Locking insert')
        lockServer.changeInsert()
        with open('./server/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=INSERT, STATUS=STARTING\n')
            sleep(5)
        with open('./server/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=INSERT, STATUS=FINISHING\n')
        print('Unlocking insert')
        lockServer.changeInsert()
        return "Insert efetuado"
        

def delete(id):
    if lockServer.checkDelete() or lockServer.checkInsert():
        #Retorna ao cliente
        return "O servidor está ocupado no momento"
    else:
        print('Locking delete')
        lockServer.changeDelete()
        with open('./server/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=DELETE, STATUS=STARTING\n')
            sleep(5)
        with open('./server/log.txt','a') as f:
            f.write(f'CLIENT={id}, SERVER={ip}:{port}, OP=DELETE, STATUS=FINISHING\n')
        print('Unlocking delete')
        lockServer.changeDelete()
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