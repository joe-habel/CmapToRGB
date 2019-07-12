from bluetooth.ble import DiscoveryService, GATTRequester

import os

from makeCmap import image_to_packets

searching = True

UUID = '6E400001-B5A3-F393E0A9-E50E24DCCA9E'

image = 'inferno.png'
packets = image_to_packets(image)

while searching:
    service = DiscoveryService()
    devices = service.discover(5)


    print "Searching with a 5 second timeout"
    for address, name in devices.iteritems():
        print '...', name, address
        if name == 'Adafruit Bluefruit LE':
            addr = address
            searching = False

print "Found", addr
requester = GATTRequester(addr)
#requester.connect(True)
print "Connected"
for packet in packets:
    requester.write_by_handle(0x00D6, packet)
    resp = requester.read_by_handle(0x00D6)[0]
    while resp == 0:
        requester.write_by_handle(0x00D6, packet)
        resp = requester.read_by_handle(0x00D6)[0]

requester.disconnect()