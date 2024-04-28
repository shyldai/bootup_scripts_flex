#!/bin/bash

nmcli networking off
nmcli networking on

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
