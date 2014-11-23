import socks
import socket
import requests

from csv import writer
#from TorCtl import TorCtl

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

#def get_newIdentity():
#    conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="")
#    conn.send_signal("NEWNYM")
#    conn.close()

# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

# import urllib2

# print urllib2.urlopen('http://checkip.dyndns.com/').read()
with open('times.csv','w') as f:
    w = writer(f)
for i in range(0, 10): 
	response = requests.get('http://checkip.dyndns.com/')
	w.writerows(response.elapsed)	
	
