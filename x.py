#!/usr/bin/python

import subprocess
import rrb3
import struct
r = rrb3.RRB3(9, 6)

subprocess.call(["sudo chmod +r /dev/hidraw0"], shell=True)

for i in xrange(10000):
	with open("/dev/hidraw0", "rb") as f:
		x = f.read(4) 
	y = struct.unpack("<l", x[0:4])
	print("%08x" % y)
	if y[0] & 0xff00 == 0xff00:
		r.forward(0, .5)
	elif y[0] & 0xff00 == 0x0000:
		r.reverse(0, .5)
	elif y[0] & 0x00ff == 0x00ff:
		r.left(0, .5)
	elif y[0] & 0x00ff == 0x0000:
		r.right(0, .5)
	else:
		r.stop()
	r.set_led1((y[0] >> 19) & 1)
	r.set_led2((y[0] >> 18) & 1)

#r.forward(1)


