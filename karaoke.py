#!/usr/bin/python

import subprocess
import struct
import time

subprocess.call(["sudo chmod +r /dev/hidraw0"], shell=True)
subprocess.call(["echo none | sudo tee /sys/class/leds/led0/trigger"], shell=True)

file = 0

arecord = 0
aplay = 0
while True:
	with open("/dev/hidraw0", "rb") as f:
		x = f.read(4) 
	y = struct.unpack("<l", x[0:4])
	print("%08x" % y)
	if aplay != 0:
		if aplay.poll() == 0:
			aplay = 0
	if (((y[0] >> 16) & 1) == 1):
		subprocess.call(["echo 1 | sudo tee /sys/class/leds/led0/brightness"], shell=True)
		if arecord == 0:
			file += 1
			arecord = subprocess.Popen(["exec arecord -f dat -D hw:1,0 record%d.wav -c 2" % file], stdout=subprocess.PIPE, shell=True)
	if (((y[0] >> 17) & 1) == 1):
		subprocess.call(["echo 0 | sudo tee /sys/class/leds/led0/brightness"], shell=True)
		if arecord != 0:	
			print("killing arecord")
			arecord.kill()
			arecord = 0

	if (((y[0] >> 18) & 1) == 1):
		if aplay == 0:
			aplay = subprocess.Popen(["exec aplay -D hw:2,0 record%d.wav" % file], stdout=subprocess.PIPE, shell=True)
	if (((y[0] >> 19) & 1) == 1):
		if aplay != 0:	
			print("killing aplay")
			aplay.kill()
			aplay = 0
	time.sleep(.1)

