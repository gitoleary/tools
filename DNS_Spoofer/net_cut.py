#!/usr/bin/env python

#https://github.com/kti/python-netfilterqueue
#Work on VM
#sudo iptables -I FORWARD -j NFQUEUE --queue-num 0  Move packets into FORWARD queue
#sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward' IP forwarding

#Work Locally
#sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#sudo iptables -I INPUT -j NFQUEUE --queue-num 0

from netfilterqueue import NetfilterQueue

def process_packet(packet):
	print(packet)
	#packet.accept()
	packet.drop()

nfqueue = NetfilterQueue()
nfqueue.bind(0, process_packet)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()