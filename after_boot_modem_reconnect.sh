#!/bin/bash
sudo insmod /root/Simcom_wwan/simcom_wwan/simcom_wwan.ko
sudo lsmod
sudo dmesg | grep simcom
sudo ifconfig wwan0 up

nmcli networking off
nmcli networking on

sudo echo -e 'AT+CNMP=2\r' > /dev/ttyUSB2
sudo echo -e 'AT$QCRMCALL=1,1\r' > /dev/ttyUSB2

sudo dhclient -1 -v wwan0

sudo echo -e 'AT+CNMP=2\r' > /dev/ttyUSB2
sudo echo -e 'AT$QCRMCALL=1,1\r' > /dev/ttyUSB2

sudo dhclient -1 -v wwan0
