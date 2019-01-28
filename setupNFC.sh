#!/bin/bash
# init

#Nano controls
#Cut line ctrl-k
#Paste line ctrl-u

#The following packages have unmet dependencies:
# apt-utils : Depends: apt (= 1.4.8) but 1.4.9 is installed
#had to fix issues with apt install using sudo apt --fix-broken install

#fix ssh hang
sudo ifconfig wlan0 mtu 500 up

#install i2c-tools
sudo apt install i2c-tools

#check the information for the next step
i2cdetect -y 1

read -p "Press [Enter] key to configiure i2c-1 device"

#install libnfc
sudo apt install libnfc5 libnfc-bin libnfc-examples

# Let libnfc know the device address of the reader in /etc/nfc/libnfc.conf:
sudo mkdir /etc/nfc
sudo touch /etc/nfc/libnfc.conf
sudo chmod 777 /etc/nfc/libnfc.conf 
sudo echo "device.name = \"PN532 over I2C\"" > /etc/nfc/libnfc.conf
sudo echo "device.connstring = \"pn532_i2c:/dev/i2c-1\"" >> /etc/nfc/libnfc.conf

nfc-scan-device -v

# use nfc-poll to test setup


