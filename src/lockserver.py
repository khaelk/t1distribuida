import threading
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread, Semaphore
import sys
import queue

delete = False
insert = False

q = queue.Queue()

try:
    ip = sys.argv[1]
    port = sys.argv[2]
except IndexError:
    print("ERROR: IP or port not defined when passing arguments.")
    sys.exit(0)

def queueOp(op):
    global q
    q.put(op)
    print(q)
    return 'queueing'

def dequeueOp():
    global q
    q.get()
    print(q)
    return 'dequeueing'

def emptyQueue():
    global q
    if q.empty():
        return True
    else:
        return False

def changeDelete():
    global delete
    delete = not delete
    print(f"Changing delete to {delete}")
    return delete

def checkDelete():
    print(f"Checking delete {delete}")
    return delete

def changeInsert():
    global insert
    insert = not insert
    print(f"Changing insert to {insert}")
    return insert

def checkInsert():
    print(f"Checking insert {insert}")
    return insert

with SimpleXMLRPCServer((ip, int(port))) as server:
    server.register_function(changeDelete)
    server.register_function(changeInsert)
    server.register_function(checkDelete)
    server.register_function(checkInsert)
    server.register_function(queueOp)
    server.register_function(dequeueOp)
    server.register_function(emptyQueue)
    print(f'Serving Lock Server on {ip} port {port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)