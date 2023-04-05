from xmlrpc.server import SimpleXMLRPCServer
import sys

try:
    ip = sys.argv[1]
    port = sys.argv[2]
except IndexError:
    print("ERROR: IP or port not defined when passing arguments.")
    sys.exit(0)

with SimpleXMLRPCServer((ip, int(port))) as server:
    server.register_function(pow)
    print('Serving XML-RPC on localhost port 8000')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)