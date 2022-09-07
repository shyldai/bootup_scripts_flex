sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install pyserial
mkdir -p ~/Documents/SIM7600X_4G_for_JETSON_NANO
wget -P ~/Documents/SIM7600X_4G_for_JETSON_NANO/ https://www.waveshare.com/w/upload/6/64/SIM7600X_4G_for_JETSON_NANO.tar.gz
cd ~/Documents/SIM7600X_4G_for_JETSON_NANO/
tar -xvf SIM7600X_4G_for_JETSON_NANO.tar.gz
sudo pip3 install Jetson.GPIO
sudo groupadd -f -r gpio
sudo usermod -a -G gpio shyld
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo apt-get install minicom
apt-get install udhcpc

# test functionality
sudo python3 ~/Documents/SIM7600X_4G_for_JETSON_NANO/AT/AT.py


echo 200 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio200/direction
echo 1 > /sys/class/gpio/gpio200/value
echo 0 > /sys/class/gpio/gpio200/value

# testing network
sudo minicom -D /dev/ttyUSB2


# Download driver
cd
wget https://www.waveshare.com/w/upload/4/46/Simcom_wwan.zip
unzip Simcom_wwan.zip
cd simcom_wwan 
# Modify the makefile from https://github.com/phillipdavidstearns/simcom_wwan-setup
sudo su
make

insmod simcom_wwan.ko
sudo lsmod
sudo dmesg | grep simcom

ifconfig wwan0
sudo ifconfig wwan0 up
ifconfig wwan0
echo -e 'AT+CNMP=2\r' > /dev/ttyUSB2
echo -e 'AT$QCRMCALL=1,1\r' > /dev/ttyUSB2

# set IP
sudo dhclient -1 -v wwan0
sudo dhclient -1 -v wwan0


git clone https://github.com/phillipdavidstearns/simcom_wwan-setup.git
cd simcom_wwan-setup
chmod +x install.sh uninstall.sh update.sh
sudo ./install.sh

sudo systemctl enable simcom_wwan@wwan0.service
sudo systemctl start simcom_wwan@wwan0.service
sudo systemctl status simcom_wwan@wwan0.service

sudo vim /etc/modules-load.d/modules.conf

# add the following to the file: simcom_wwan

sudo vim /etc/udev/rules.d/99-usb-4g.rules

# add the following to the file: SUBSYSTEM=="tty", KERNEL=="ttyUSB2", TAG+="systemd", ENV{SYSTEMD_WANTS}+="simcom_wwan@wwan0.service"
