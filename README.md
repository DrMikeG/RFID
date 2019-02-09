# RFIDp

This project is for setting up my raspberry pi v3, with volumio 2 and a PN532 RFID reader connected to GPIO.

There is a ./setup script with various auto and semi-manual steps for configuring the raw volumio 2 image to support libNFC

There is a directory of python, copied from an example pynfc (see headers for origin) from which pollForActions can be run continuously.

I use socketTest to communicate with volumio to test a few things in the WebAPI

There is also an arduino nano test program for reading cards using the pn532-HUD library.
