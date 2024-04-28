#!/bin/bash

nmcli networking off
nmcli networking on

# ifconfig returns two usb devices. One of them contains keyword 'inet'. 
# We have to get IP address from that. 'sudo dhclient -v usbX'
# Example: 
# usb1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
#         inet 192.168.225.32  netmask 255.255.255.0  broadcast 192.168.225.255
#         inet6 2607:fb91:20c2:3020:4608:8a23:da0b:a1ef  prefixlen 64  scopeid 0x0<global>
#         inet6 fe80::e955:663c:4087:18f6  prefixlen 64  scopeid 0x20<link>
#         inet6 2607:fb91:20c2:3020:c244:aafb:53f2:73d8  prefixlen 64  scopeid 0x0<global>
#         ether 9a:09:ed:37:57:29  txqueuelen 1000  (Ethernet)
#         RX packets 19492  bytes 1350075 (1.3 MB)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 18680  bytes 2610131 (2.6 MB)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# usb0:avahi: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
#         inet 169.254.6.20  netmask 255.255.0.0  broadcast 169.254.255.255
#         ether 86:8d:4b:7f:44:47  txqueuelen 1000  (Ethernet)


# Run ifconfig command and store the output in a variable
output=$(ifconfig)

# Function to run dhclient on the specified interface
run_dhclient() {
    local interface="$1"
    sudo dhclient -v "$interface"
}

# Check if usb1 interface is present in the output and if it has 'inet' in the second line after 'usb1:'
if grep -q "usb1:" <<< "$output" && grep -q "inet" <<< "$(grep -A 2 "usb1:" <<< "$output" | sed -n '2p')"; then
    echo "Running dhclient on usb1..."
    run_dhclient "usb1"
# Check if usb0 interface is present in the output and if it has 'inet' in the second line after 'usb0:'
elif grep -q "usb0:" <<< "$output" && grep -q "inet" <<< "$(grep -A 2 "usb0:" <<< "$output" | sed -n '2p')"; then
    echo "Running dhclient on usb0..."
    run_dhclient "usb0"
else
    echo "No relevant interface found"
fi
