
Nano:

https://www.element14.com/community/community/raspberry-pi/blog/2012/12/14/nfc-on-raspberrypi-with-pn532-py532lib-and-i2c
https://github.com/HubCityLabs/py532lib

** 1) I have it working on an arduino nano (RFIDpi.ino) using PN532-PN532_HSU

Dev PI:

https://blog.stigok.com/2017/10/12/setting-up-a-pn532-nfc-module-on-a-raspberry-pi-using-i2c.html
These instructions 

sudo apt install i2c-tools

i2cdetect -y 1

Install NFC tools: sudo apt install libnfc5 libnfc-bin libnfc-examples
Let libnfc know the device address of the reader in /etc/nfc/libnfc.conf:
device.name = "PN532 over I2C"
device.connstring = "pn532_i2c:/dev/i2c-1"

fix for hanging SSH connected to PI
sudo ifconfig wlan0 mtu 500 up

https://github.com/ikelos/pynfc
libnfc wrapper for python - needed modification 

Error:
File "/home/pi/newpynfc-master/src/nfc.py", line 607, in 
_libs["nfc"] = load_library("nfc")
File "/home/pi/newpynfc-master/src/nfc.py", line 367, in load_library
raise ImportError("%s not found." % libname)
ImportError: nfc not found.
Fix:
if you're in RPi, code to find libnfc is buggy. For a quick workaround change line 477 of nfc.py to:
for dir in open('/etc/ld.so.conf.d/arm-linux-gnueabihf.conf')


** 2) Using nfc-poll, I'm accessing libNFC and can scan for a card (then it exits)
** 3) Using mifareauth.py with modified (nfc.py) I can read UID, but I don't understand the code at all