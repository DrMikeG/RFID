#script
print('hello world1')
import subprocess
subprocess.call(['aplay -fdat /home/volumio/RFID/pop/pop1.wav'], shell=True)
print('hello world2')
