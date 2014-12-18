from stem import CircStatus
from stem.control import Controller
from stem.util.str_tools import get_size_label

import socks
import socket
import time

from stem import Signal
from stem.control import Controller

def newID(): # force Tor for new identity
	with Controller.from_port(port = 9151) as controller:
  			controller.authenticate()
			controller.signal(Signal.NEWNYM)	

for i in range(10):
	newID()
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
	s = socks.socksocket()
	start_time = time.time()
	s.connect(('www.cmu.edu', 80)) # socket connect	
	message = 'GET / HTTP/1.0\r\n\r\n'
	s.sendall(message) # send GET request
	
	data = s.recv(512)
	while True: # receive all data
	    if not data: 
		break
	    data = s.recv(512)

	end_time = time.time()
	print end_time - start_time # measure response	
	s.close() # close socket
