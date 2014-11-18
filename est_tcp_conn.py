import socket
import struct
def create_tcp():
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5578
	BUFFER_SIZE_TCP = 20
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	return s
