## Self-Organizing Map (SOM)
##
## http://robin.meier.free.fr
## http://www.neuromuse.org
## paris 13eme, february 06
##
 
"""self organizing-map a la kohonen. to interact, send and receive data via udp"""
 
import sys
#psyco for intel procs only...
#from psyco import *
from numarray import *
from numarray.random_array import *
from math import *
from socket import *
from cPickle import *
 
class Networking:
	def __init__(self, rechost="", recport=12345, buf=32768, verbose=0):
		self.recaddr = (rechost,recport)
		self.buf = buf
		self.UDPSock = socket(AF_INET,SOCK_DGRAM)
		self.TCPSock = socket(AF_INET, SOCK_STREAM)
		self.verbose = verbose
	def bindUDPSocket(self):
		self.UDPSock.bind(self.recaddr)
		if self.verbose:
			print "UDP socket bound on", self.recaddr
	def bindTCPSocket(self):
		self.TCPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.TCPSock.bind(self.recaddr)
		self.TCPSock.listen(5)		#let at most one connection wait to be processed. probably too small.
		if self.verbose:
			print "tcp server running on", self.recaddr
	def connectTCPServer(self,desthost="localhost", destport=12345):
		self.TCPSock.connect((desthost,destport))
		if self.verbose:
			print "connected to", desthost, destport
	def receiveUDPData(self):
		while 1:
			print "waiting for data"
			data,self.recaddr = self.UDPSock.recvfrom(self.buf)
			if not data:
				print "Client has exited!"
				break
			else:
				input = loads(data)
				if self.verbose:
					print "YO! message received '", input,"'"
				return input
				break
	def receiveTCPData(self):
		while 1:
			clientsock, clientaddr = self.TCPSock.accept()
			if self.verbose:
				print "got connection from", clientsock.getpeername()
			data = clientsock.recv(self.buf)
			if not data:
				print "Client has exited!"
				break
			else:
				input = loads(data)
				if self.verbose:
					print "YO! message received '", input,"'"
				return input
				break
	def sendUDPData(self, datatosend, desthost="localhost", destport=12345):
		destaddr = (desthost,destport)
		if self.verbose:
			print "sending to", destaddr
		self.UDPSock.sendto(dumps(datatosend),destaddr)
		if self.verbose:
			print "YO! data was sent '", datatosend,"'"
		else:
			print "YO! data sent."
	def sendTCPData(self, datatosend, desthost="localhost", destport=12345):
		destaddr = (desthost,destport)
		if self.verbose:
			print "sending to", destaddr
		self.TCPSock.sendto(dumps(datatosend),destaddr)
		if self.verbose:
			print "YO! data was sent via tcp '", datatosend, "'"
		else:
			print "YO! data sent (tcp)."
 
class Som:
	def __init__(self, somsize=100, vectorsize=10):
		self.somsize = somsize
		self.weights = random((somsize,vectorsize))
	def randomizeWeights(self, inputvector):
		self.weights = random((self.somsize,len(inputvector)))
	def getActivation(self, inputvector):
		"""euclidean distance without sqrt"""
		self.activation = sum(((self.weights-inputvector)*(self.weights-inputvector)),1)
	def getWinner(self):
		self.winner = int((argsort(self.activation))[0])
	def updateWeights(self, inputvector, learningrate=0.1, radius=3):
		#conversion index-&gt;coord
		seite = int(sqrt(self.somsize))
		winy = int(self.winner/seite)
		winx = int(self.winner%seite)
		#calculate distances
		def dist(x,y):
			return (x-winx)**2+(y-winy)**2
		self.distances = fromfunction(dist, (seite, seite))
		#print self.distances
		for i in range(self.somsize):
			iy=int(i/seite)
			ix = int(i%seite)
			n = float(self.distances[iy,ix])
			if n < radius: #pour mettre a jour seulement les neurones proche du winner (c plus vite)
				delta = learningrate*(inputvector-(take(self.weights,i)))*(exp(-1*((n*n)/(2*radius*radius))))#take(self.weights,winner) is vector of winner
				put(self.weights,i,((take(self.weights,i)+delta)))
 
################################################################
 
#mexican hat#
#(2/sqrt(3))*(pow(pi,-0.25))*(1-(n*n))*(exp(-1*((n*n)/2)))
 
#gaussian#
#exp(-1*((n*n)/(2*radius*radius)))
 
################
# stuff to send#
################
 
# send poids (somsize)
# UDPSock.sendto(dumps(poids),destaddr)
# print "message sent '", poids, "'"
 
# send activation (somsize)
# UDPSock.sendto(dumps(activation.getflat()),destaddr)
# print "message sent '", activation, "'"
 
# send winner (input)
# UDPSock.sendto(dumps(list(poids[winner,:])),destaddr)
# print "message sent '", list(poids[winner,:]), "'"