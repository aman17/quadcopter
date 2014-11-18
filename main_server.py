import socket
import threading
import SocketServer
import loginCheck
import pickle
import json

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        if data=="login":
        	self.request.sendall("requesting login data")
        	usr = self.request.recv(1024)
        	self.request.sendall("ack")
        	pwd = self.request.recv(1024)
        	loginData = loginCheck.login(usr,pwd)
        	self.request.sendall(pickle.dumps(loginData))
        	self.request.recv(1024)
        	login_val = loginData[2]
        	print login_val
        	if(login_val==1):
        		rows = loginCheck.get_ip(loginData[0])
        		print loginData[0],"in here"
        		for row in rows:
        			if row[0]==loginData[0]:
        				ip = row[1]
        		
        		print ip,"here"
        		self.request.sendall(ip)
        	#pickle.dumps(ipdata)



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 5578
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    print "ip: ",ip
    print "port: ",port

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    while(1):
    	inp = raw_input('1.Send client\n2.shutdown server')

    	if inp == "1":
    		client(ip, port, "Hello World")
    	if inp == "2":
			server.shutdown()
			break	
		
		
