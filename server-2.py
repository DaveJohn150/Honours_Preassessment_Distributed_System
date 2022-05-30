from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socket

import random

f = open("database.txt", "r")
database = eval(f.read()) #reads list of dictionaries from database file
f.close()
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


host = str(socket.gethostbyname(socket.gethostname()))
print("Database Host Name:", host)
# Create server
with SimpleXMLRPCServer((host, 8001),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class MyFuncs:
        def Connect(self):
            return "Database Connection Successful!"
        
        def getPassword(self, ID):
            for data in database:
                if data['id'] == ID:
                    return data['password']
            return False

        def getGrades(self, ID):
            for data in database:
                if data['id'] == ID:
                    return str(data)
            return str([])
    server.register_instance(MyFuncs())

    # Run the server's main loop
    server.serve_forever()





