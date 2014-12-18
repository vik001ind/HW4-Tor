from stem import CircStatus
from stem.control import Controller
from stem.util.str_tools import get_size_label
import pygeoip

# GeoIP file object for obtaining country from IP
gi = pygeoip.GeoIP('GeoIP.dat') 

# Accessing controller
with Controller.from_port(port = 9151) as controller:
  controller.authenticate()
# Accessing circuits in controller 
  for circ in sorted(controller.get_circuits()):
# Filtering only 3 relay complete circuits
    if circ.status != CircStatus.BUILT or len(circ.path) < 3: 
      continue

    print 
    print "Circuit %s (%s)" % (circ.id, circ.purpose)
    cirStr = ""
# Accessing relays in each circuit
    for i, entry in enumerate(circ.path):
      if i == 0:
   	str = "Entry node"
      elif i == len(circ.path) - 1:
   	str = "Exit node"
      else:
   	str = "Middle node" 
      fingerprint, nickname = entry
      
      bw_rate = get_size_label(int(controller.get_conf('BandwidthRate', '0')))
     		
      desc = controller.get_network_status(fingerprint, None)
      address = desc.address if desc else 'unknown'
      countrycode = controller.get_info("ip-to-country/%s" % desc.address, "unknown")
      country = gi.country_name_by_addr(address)
      cirStr = cirStr + " %s: [IP: %s, Country: %s, Bandwidth: %s/s] ->" % (str, address, country, bw_rate)	
    print cirStr[:-2]
