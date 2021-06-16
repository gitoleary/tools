#!/usr/bin/env python

#https://github.com/kti/python-netfilterqueue
from netfilterqueue import NetfilterQueue

def process_packet(packet):
	print(packet)
	packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, process_packet)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()