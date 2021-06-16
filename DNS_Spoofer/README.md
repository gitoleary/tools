# DNS Spoofer

## Net Cut

Intercepting Packets on the network:

* Accept packets
* Drop packets

## DNS Spoof
Remaps any DNS to another DNS server  


## Usefull Commands

Work on VM  
sudo iptables -I FORWARD -j NFQUEUE --queue-num 0  Move packets into FORWARD queue  
sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward' IP forwarding  

Work Locally  
sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0  
sudo iptables -I INPUT -j NFQUEUE --queue-num 0  

Flush iptables  
sudo iptables --flush  