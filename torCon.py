import socks
import socket
import requests

from stem import Signal
from stem.control import Controller
	
def create_connection(address, timeout=None, source_address=None):
    	with Controller.from_port(port = 9151) as controller:
  		controller.authenticate()
		controller.signal(Signal.NEWNYM)
    	sock = socks.socksocket()
    	sock.connect(address)
    	return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

response = requests.get('http://checkip.dyndns.com/')
print response.elapsed
