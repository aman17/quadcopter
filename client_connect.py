import rec_main
import est_tcp_conn
import loginCheck
from PyQt4 import QtGui, QtCore, uic
import sys
import os
import est_udp_rec_conn
import threading
import cv2
import cv2.cv as cv
import pickle
import socket
import struct
import numpy as np
import json
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot


cap = cv2.VideoCapture(-1) 
capRead = cv2.VideoCapture('output.avi')
cap.set(3,160)
cap.set(4,120)
capRead.set(3,160)
capRead.set(4,120)

# Define the codec and create VideoWriter object
#fourcc = cv.CV_FOURCC('X','V','I','D')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (160,120))
'''try:
    conn = psycopg2.connect(database = "201201063", user = "201201063", password="201201063", host="10.100.71.21",port="5432")
    print "success"
except:
    print "I am unable to connect to the database"
cur = conn.cursor()'''
    
class liveConnect(QtCore.QThread):
	def __init__(self,conn_dict):
		QtCore.QThread.__init__(self)
		self.udp_sock = conn_dict
		'''self.udp_sock = conn_dict['udp']
		self.tcp_sock = conn_dict['tcp']'''
		print "thread __init__"
 	def run(self):
 		print "thread run"
 		#self.tcp_sock.send("live")
 		#self.tcp_sock.recv(1024)
 		while True:
 			c = cv2.waitKey(1) & 0xFF
			d = self.udp_sock.recvfrom(65536)
			data = d[0]
			addr = d[1]
			print addr
			self.emit(QtCore.SIGNAL('display'),data)
			if c==ord('q'):
				#self.quit()
				break
	 	print "oner"
 		return


class StudentGui(QtGui.QMainWindow):
	def __init__(self):
		print "check check"
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('RecieverMainWindow.ui')
		self.ui.show()
		print "loaded..."
		self.connect(self.ui.btnLive, QtCore.SIGNAL("clicked()"), self.live)
		self.connect(self.ui.btnArchives, QtCore.SIGNAL("clicked()"), self.archive)
		#self.connect(self.ui.btnArchives, QtCore.SIGNAL("clicked()"), self.buttonFn_2)
		self.conn_dict = est_udp_rec_conn.create_connection()
		
	def disp(self, dat):
		buf = pickle.loads(dat)
		#print buf
		frame = cv2.imdecode(buf,0)
		cv2.imshow('ClientRecieving',frame)
		#print frame

	def archive(self):
		self.at = archiveThread(self.conn_dict)
		self.connect(self.at,QtCore.SIGNAL('display'),self.disp)
		self.at.start()

	def live(self):
		print "live"
		self.lc = liveConnect(self.conn_dict)
		self.connect(self.lc,QtCore.SIGNAL('display'),self.disp)
		self.lc.start()

class CameraCapture(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)
 	def run(self):
 		while True:
 			ret, frame = cap.read()
 			print frame
 			if ret:
	 			#out.write(frame)
				#print "aman",frame
				(retval,buf) = cv2.imencode(".jpg",frame)
				ser = pickle.dumps(buf)
	 			self.emit(QtCore.SIGNAL('captureNow'),ser)
	 			c = cv2.waitKey(50) & 0xFF
	 			if c==ord('q'):
	 				break
	 		else:
	 			print "break"
	 			break
	 	print "oner"
 		return

class TeacherGui(QtGui.QMainWindow):
	def __init__(self,ip):
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('TeacherGui.ui')
		self.ui.show()
		self.MCAST_GRP = ip
		self.connect(self.ui.btnStartLecture,QtCore.SIGNAL("clicked()"),self.startLiveFeed)
		
	def runCap(self,text):
		#print text
		buff = pickle.loads(text)
		
		frame = cv2.imdecode(buff,0)
		cv2.imshow('serverSending',frame)
		self.sock.sendto(text, (self.MCAST_GRP, self.MCAST_PORT))	
	def startLiveFeed(self):
		lectureName = self.ui.leLectureName.text()
		#self.MCAST_GRP = '224.1.1.1'
		self.MCAST_PORT = 5011
		print self.MCAST_GRP
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)


		self.TCP_IP = '127.0.0.1'
		self.TCP_PORT = 5053
		self.BUFFER_SIZE_TCP = 20
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((self.TCP_IP, self.TCP_PORT))

		self.capture = CameraCapture()
		self.connect(self.capture,QtCore.SIGNAL('captureNow'),self.runCap)
		self.capture.start()
class loginScreen(QtGui.QMainWindow):
	def __init__(self,app1):
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('loginScreen.ui')
		self.ui.show()
		self.ui.lePwd.setEchoMode(2)
		self.connect(self.ui.BtnSignIn, QtCore.SIGNAL("clicked()"), self.getLoginData)
		self.app1 = app1
		self.ui.setStyleSheet("QMainWindow {background-image: url(online-learning.jpg);background-repeat: no-repeat}")
		#self.connect(self.ui.BtnRegister, QtCore.SIGNAL("clicked()"), self.register)
	def getLoginData(self):
		usr = self.ui.leUserId.text()
		usr = str(usr)
		pwd = self.ui.lePwd.text()
		pwd = str(pwd)
		s = est_tcp_conn.create_tcp()
		s.send("login")
		data = s.recv(1024)
		#print data
		if data == "requesting login data":
			s.send(usr)
			s.recv(1024)
			s.send(pwd)
			a = s.recv(1024)
			s.send("ack")
			print type(a)
			#string = "('aman', 'agarwal', 1)"
			a_new = pickle.loads(a)
			
			print " ",a_new[0]," ",a_new[1]," ",a_new[2]
			login_val = a_new[2]
			
			if login_val == 2:
				print "student"
				self.ui.close()
				self.stu = StudentGui()
			if login_val == 1:
				ip = s.recv(1024)
				'''ipdata = pickle.loads(ipdata)
				print ipdata[1]'''
				print ip
				self.ui.close()
				self.tea = TeacherGui(ip)



if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	win = loginScreen(app)
	sys.exit(app.exec_())
