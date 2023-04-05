import xmlrpc.client
import threading
from time import sleep

server = xmlrpc.client.ServerProxy("http://localhost:8000")

def function_call():
    while True:
        print(server.pow(2,3))
        sleep(0.1)

threading.Thread(target=function_call).start()