import socket
import struct
def create_connection():
	print "connection createing"
	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5011
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('', MCAST_PORT))
	mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	'''TCP_IP = '127.0.0.1'
	TCP_PORT = 5053
	BUFFER_SIZE_TCP = 20
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))'''

	#conn_dict = {'udp': sock, 'tcp': s}
	print "connection fin.."
	return sock
