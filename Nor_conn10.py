import socks
import socket
import time



for i in range(10):
	s = socks.socksocket()
	start_time = time.time()
	s.connect(('www.cmu.edu',80)) # socket connect	
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
