from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socket



# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


import xmlrpc.client
while True:
    try:
        database = input("Please input database address: ")
        d = xmlrpc.client.ServerProxy('http://'+database+':8001')
        print(d.Connect())
        break
    except:
        print("Connection failed!, Please try again")


host = str(socket.gethostbyname(socket.gethostname()))
print("Host Name:", host)
# Create server
with SimpleXMLRPCServer((host, 8000), allow_none=True,
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class MyFuncs:
        __userData = {}
        __userResults = []
        def Connect(self):
            return "Connection Successful!"
        
        def Evaluate(self, grades = {}):
            if self.__userData == {}:
                if grades == {}: #grades only = {} if grades were fetched from database, which would be in __userData
                    return 'Error'
                self.__userData = grades
                self.__userData['id'] = 'guest'
            if self.__userResults == []:
                self.__ProcessGrades()
            if len(self.__userData) < 13 or (len(self.__userData) > 31 and self.__userData['id'] is not None): 
                return "Invalid results length, must be between 12 and 30."
            failCount = 0
            for i in self.__userResults:
                if float(i) < 50:
                    failCount += 1
            average = self.Average(self.__userResults)
            if failCount > 6: #CA-07
                return self.__userData['f_name'] + ', ' + str(average) + ', with 6 or more Fails! DOES NOT QUALIFY FOR HONORS STUDY!'
            elif average >= 70: #CA-01
                return self.__userData['f_name'] + ', ' + str(average) + ', QUALIFIED FOR HONORS STUDY!'
            else:
                top8 = self.Average(self.__userResults[-8:])
                if average >= 65:
                    if top8 >= 80: #CA-02
                        return self.__userData['f_name'] + ', ' + str(average) + ', ' + str(top8) + ', QUALIFIED FOR HONORS STUDY'
                    else:
                        return self.__userData['f_name'] + ', ' + str(average) + ', ' + str(top8) + ", MAY HAVE A GOOD CHANCE! Need further assessment!"
                elif average >= 60:
                    if top8 >= 80:
                        return self.__userData['f_name'] + ', ' + str(average) + ', ' + str(top8) + ", MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator's permission!"
                    else:
                        return self.__userData['f_name'] + ', ' + str(average) + ' DOES NOT QUALIFY FOR HONORS STUDY!'
                else:
                    return self.__userData['f_name'] + ', ' + str(average) + ', DOES NOT QUALIFY FOR HONORS STUDY!'

        def Average(self, arr):
            total = 0
            num = 0
            for i in arr:
                total += float(i)
                num += 1
            return round(total / num, 2)

        def Authenticate(self, ID, password):
            actual_password = d.getPassword(ID)
            if actual_password is not False:
                if actual_password == password:
                    self.__userData = eval(d.getGrades(ID))
                    return True
            return False

        def __getUserGrades(self, ID): #private function
            return d.getGrades(ID)

        def __ProcessGrades(self):
            for i in self.__userData:
                if i == 'f_name' or i == 'id' or i == 'password':
                    continue
                else:
                    for j in self.__userData[i]:
                        if j is not None:
                            self.__userResults.append(j)
            self.__userResults.sort()

        def DisplayTable(self):
            table = self.__userData['f_name'] + '\t' + self.__userData['id'] + '\n'
            table = table + 'Unit code\tAttempt 1\tAttempt 2\tAttempt3\n'
            for key in self.__userData:
                if key != 'f_name' and key != 'id' and key != 'password':
                    table = table + key + '\t\t' + str(self.__userData[key][0])
                    table = table + '\t\t' + str(self.__userData[key][1]) 
                    table = table + '\t\t' + str(self.__userData[key][2]) + '\n'
            return table
            
        def LogOut(self):
            self.__userData = {}
            self.__userResults = []
            return '' #functions cannot return None across rpc

        def MenuOptions(self, choice):
            if self.__userResults == []:
                self.__ProcessGrades()
            if choice == '1':
                return self.DisplayTable()
            elif choice == '2':
                return self.Average(self.__userResults)
            elif choice == '3':
                return self.Average(self.__userResults[-8:])
            elif choice == '4':
                return self.Evaluate()
    server.register_instance(MyFuncs())

    # Run the server's main loop
    server.serve_forever()
