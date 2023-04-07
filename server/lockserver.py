import threading
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread, Semaphore
import sys

    # t1 = threading.Thread(target=processing, args=(1,))
    # t1.start()
    # t1.join()

    # semaphore.acquire(timeout=10)
    # semaphore.release(n=3)
delete = False
insert = False

try:
    ip = sys.argv[1]
    port = sys.argv[2]
except IndexError:
    print("ERROR: IP or port not defined when passing arguments.")
    sys.exit(0)

def checkLock():
    return delete

def youCanLock():
    if(delete):
        # acessa e deleta linha do arquivo ou guarda log
        # sleep
        return "Delete OK"
    else:
        return "File is locked"

# ====================

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
    print(f'Serving Lock Server on {ip} port {port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)