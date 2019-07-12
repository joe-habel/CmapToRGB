import pexpect
import sys
from time import sleep

from makeCmap import image_to_packets

packets_per_connection = 60

image = 'bp.png'
all_packets = image_to_packets(image)
n = packets_per_connection
connections = [all_packets[i * n:(i + 1) * n] for i in range((len(all_packets) + n - 1) // n )]

for i, packets in enumerate(connections):
    print "Strip: ", i+1
    shell = pexpect.spawn('sudo gatttool -b DB:B8:00:36:82:E8 -I -t random --sec-level=high')

    shell.expect_exact('[sudo] password for ebicuser: ')
    shell.sendline('nanoSca1e')
    shell.expect_exact('[DB:B8:00:36:82:E8][LE]> ')
    shell.sendline('connect')
    shell.expect('.*Connection successful.*')
    print "found"
    sleep(1)
    for j, packet in enumerate(packets):
        shell.sendline('char-write-cmd 0x0025 %s'%packet)
        sleep(0.05)
        print "... Packet: ", j+1
    #print "sent", packet
    shell.sendline('exit')
    shell.close()

