import socks
import socket
import requests

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

# import urllib2

# print urllib2.urlopen('http://checkip.dyndns.com/').read()

response = requests.get('http://checkip.dyndns.com/')
print response.elapsed
