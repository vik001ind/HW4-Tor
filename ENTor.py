import StringIO
import socket
import urllib
import pycountry
import time

import socks  # SocksiPy module
import stem.process

from stem.util import term

SOCKS_PORT = 9050
mydict = {} # global country codes dictionary {country:accesstime}
cc = ""

# Set socks proxy and wrap the urllib module
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket
def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

def query(url): # query site and get status code
  global cc, mydict
  try:
    if urllib.urlopen(url).getcode() == 200: # access allowed
      t = time.strftime("%Y-%m-%d %H:%M:%S")
      print urllib.urlopen(url).getcode(), cc, t
      country = pycountry.countries.get(alpha2=str(cc[1:-1])).name
      mydict.update({country : t}) # record country and access time
    else: # access blocked
      print cc, urllib.urlopen(url).getcode() 
  except:
    return "Unable to reach from %s" % cc

for i in range(len(pycountry.countries)): # iterating over all countries 
  cc = "{" + list(pycountry.countries)[i].alpha2 + "}" # assigning a country code to list cc

  try:
    tor_process = stem.process.launch_tor_with_config(  
      config = {
      'SocksPort': str(SOCKS_PORT),
      'ExitNodes': str(cc), 	
      'GeoIPFile': '/home/v1k/tor-browser_en-US/Browser/TorBrowser/Data/Tor/geoip',
      'GeoIPv6File': '/home/v1k/tor-browser_en-US/Browser/TorBrowser/Data/Tor/geoip6',
      },
      timeout = 15, 
    )
    query("http://dogo.ece.cmu.edu/tor-homework/secret/")
    tor_process.kill()  # stops tor
  except:
    print "Timeout: no Tor Exit node found in %s" % cc

print mydict # print all access allowed countries and access time 
print "Total countries allowing access: %d"  % len(mydict.keys())
