from stem import CircStatus
from stem.control import Controller
from stem.util.str_tools import get_size_label

with Controller.from_port(port = 9151) as controller:
  controller.authenticate()

  for circ in sorted(controller.get_circuits()):
    if circ.status != CircStatus.BUILT:
      continue

    print
    print "Circuit %s (%s)" % (circ.id, circ.purpose)

    for i, entry in enumerate(circ.path):
      if i == 0:
   	str = "Entry node"
      elif i == len(circ.path) - 1:
   	str = "Exit node"
      else:
   	str = "Middle node" 
      fingerprint, nickname = entry
      
      bw_rate = get_size_label(int(controller.get_conf('BandwidthRate', '0')))
      bw_burst = get_size_label(int(controller.get_conf('BandwidthBurst', '0')))
		
      desc = controller.get_network_status(fingerprint, None)
      address = desc.address if desc else 'unknown'
      country = controller.get_info("ip-to-country/%s" % desc.address, "unknown")
	
      print " %s: [IP: %s, Country Code: %s, Bandwidth: %s/s]" % (str, address, country, bw_rate)
