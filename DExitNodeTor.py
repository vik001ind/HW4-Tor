import StringIO
import socket
import urllib

import socks  # SocksiPy module
import stem.process

from stem.util import term

SOCKS_PORT = 9050

# Set socks proxy and wrap the urllib module

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo


def query(url):
  """
  Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
  """

  try:
    return urllib.urlopen(url).read()
  except:
    return "Unable to reach %s" % url


# Start an instance of Tor configured to only exit through Russia. This prints
# Tor's bootstrap information as it starts. Note that this likely will not
# work if you have another Tor instance running.

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print term.format(line, term.Color.BLUE)


print term.format("Starting Tor:\n", term.Attr.BOLD)

tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort': str(SOCKS_PORT),
    'ExitNodes': '{de}''{ch}''{pl}', 	
    'GeoIPFile': '/home/v1k/tor-browser_en-US/Browser/TorBrowser/Data/Tor/geoip',
    'GeoIPv6File': '/home/v1k/tor-browser_en-US/Browser/TorBrowser/Data/Tor/geoip6',
  },
  init_msg_handler = print_bootstrap_lines,
)

print term.format("\nChecking our endpoint:\n", term.Attr.BOLD)
print term.format(query("http://dogo.ece.cmu.edu/tor-homework/secret/"), term.Color.BLUE)

tor_process.kill()  # stops tor
