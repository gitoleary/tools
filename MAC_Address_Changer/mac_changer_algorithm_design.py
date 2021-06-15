#!/usr/bin/env python

import subprocess
import optparse

def get_arguments():
	parse = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="Interface Adapter To Change")
	parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
	(options, args) = parser.parse_args()
	if not options.interface:
		parser.error("[-] Please specify an interface, use --help for more information.")
	elif not options.new_mac:
		parser.error("[-] Please specify a new mac, use --help for more information.")
	return options


def change_mac(interface, new_mac):
	print("[+] Change MAC Address for " + interface + " to" + new_mac)
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])


options = get_arguments()
change_mac(options.interface, options.new_mac)