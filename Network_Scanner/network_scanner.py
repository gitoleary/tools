#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
	options = parser.parse_args()
	return options

def scan(ip):
	arp_request = scapy.ARP(pdst = ip)
		#print(arp_request.summary())
		#scapy.ls(scapy.ARP()) #Listing options
		#arp_request.show()

	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
		#scapy.ls(scapy.Ether())
		#print(broadcast.summary())

	arp_request_broadcast = broadcast/arp_request
		#print(arp_request_broadcast.summary())
		#arp_request_broadcast.show()

	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #Send & Receive
		#print(answered_list.summary())

	clients_list = []
	for element in answered_list:
		#print(element[1].show()) #Printing returned packets

		client_dict = {"ip": element[1].psrc, "mac" : element[1].hwsrc}
		clients_list.append(client_dict)
	
	return clients_list

def print_result(results_list):
	print("IP\t\t\tMAC Address\n-------------------------------------")
	for client in results_list:
		print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)