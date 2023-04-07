import xmlrpc.client
import threading
from time import sleep
import sys

try:
    id = sys.argv[1]
except IndexError:
    print("ERROR: IP or port not defined when passing arguments.")
    sys.exit(0)

server = xmlrpc.client.ServerProxy("http://localhost:8000")

def function_call():
    while True:
        print(server.read(id))
        sleep(0.1)
        print(server.insert())
        sleep(0.1)
        print(server.delete())
        sleep(0.1)

threading.Thread(target=function_call).start()