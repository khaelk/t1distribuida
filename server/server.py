import threading
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread, Semaphore
import sys
import time, calendar
from time import sleep
import xmlrpc.client


deleteBlocked = False
InsertBlocked = False



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
        # tentar retornar
        return "O servidor está ocupado no momento"
    else:
        time_stamp = time.time()
        print(f'cliente {id}: read {time_stamp}')
        return "Leitura efetuada"

def insert():
    print('antes do if')
    if lockServer.checkDelete() or lockServer.checkInsert():
        # tentar retornar
        print('dentro do if')
        return "O servidor está ocupado no momento"
    else:
        print('antes do change')
        lockServer.changeInsert()
        sleep(5)
        # pedir pro servidor
        #(0.1)
        # pedir pro servidor
        #sleep(0.1)
        # pedir pro servidor
        #sleep(0.1)
        #resWrite = lockServer.writefile()
        #if resWrite == "OK":
        lockServer.changeInsert()
        return "Insert efetuado"
        # else:
        #     sleep(0.1)
        #     resWrite = lockServer.writefile()
        #     return "Nao foi possivel"
        # resDelete = lockServer.deleteline()
        

def delete():
    if lockServer.checkDelete() or lockServer.checkInsert():
        # tentar retornar
        return "O servidor está ocupado no momento"
    else:
        lockServer.changeDelete()
        sleep(5)
        lockServer.changeDelete()
        return "Delete efetuado"

def processing():
    
    return 1





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