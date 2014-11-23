import socks
import socket
import requests

from csv import writer
from stem import Signal
from stem.control import Controller
with Controller.from_port(port = 9151) as controller:
  	controller.authenticate()
	controller.signal(Signal.NEWNYM)

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

def get_newIdentity():	
  	controller.signal(Signal.NEWNYM)
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
	socket.socket = socks.socksocket
	socket.create_connection = create_connection

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

# import urllib2

# print urllib2.urlopen('http://checkip.dyndns.com/').read()

#with open('times.csv','w') as f:
#    w = writer(f)
for i in range(0, 10): 
#	get_newIdentity()
	response = requests.get('http://checkip.dyndns.com/')
#	w.writerows(response.elapsed)
	print response.elapsed



