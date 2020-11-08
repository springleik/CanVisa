#!/usr/bin/env python3
# file CanVisa.py

import sys, can, time, datetime, string, struct, math, pyvisa

# get object dictionary for the Visa instrument
from Keithley2230 import theTree

# setup for various CAN interfaces

# https://copperhilltech.com/pican2-controller-area-network-can-interface-for-raspberry-pi/
# sudo ip link set can0 up type can bitrate 1000000
# canBus = can.interface.Bus(channel='can0', bustype='socketcan_native')

# https://pascal-walter.blogspot.com/2015/08/installing-lawicel-canusb-on-linux.html
# sudo slcand -o -c -f -s8 /dev/ttyUSB0 slcan0
# sudo ifconfig slcan0 up
canBus = can.interface.Bus(channel='slcan0', bustype = 'socketcan_native')

# Lawicel interface on Windows
# canBus = can.interface.Bus(bustype='slcan', channel='COM6', bitrate=1000000)

# command line arguments
print ('CanVisa.py exposes an SDO interface for VISA instruments')
print ('M. Williamsen, 11/7/2020, https://github.com/springleik')
print ('Usage: python3 CanVisa.py [arg names and values]')
print ('  arg name | arg value')
print ('  ---------|----------')
print ('  -node    | CAN node number   (default is 46)')
print ('  -indx    | CAN SDO index     (default is 0x6000)')
print ('  -visa    | VISA descriptor   (default is USB0...)')

# set defaults
theNode = 46
theIndx = 0x6000
theVisa = 'USB0::1510::8752::9032100::0::INSTR'

# check for user inputs on command line
args = iter(sys.argv)
print ('Running script: "{0}" in Python:\n {1}'.format(next(args), sys.version))
for arg in args:
	if '-node' == arg:
		theNode = int(next(args, theNode), 0)
	elif '-indx' == arg:
		theIndx = int(next(args, theIndx), 0)
	elif '-visa' == arg:
		theVisa = next(args, theVisa)
	else:
		print ('Unexpected argument: {0}'.format(arg))

# --------------------------------
# setup for VISA instrument
theMgr = pyvisa.ResourceManager()
print ('Available Visa resources:\n {0}'.format(theMgr.list_resources()))
theInst = theMgr.open_resource(theVisa)
theInst.read_termination = '\n'
theInst.write_termination = '\n'
theInst.timeout = 10000	# 10 seconds
print ('Instrument {0} exposed as CAN node {1}.'.format(theVisa, theNode))
print (' Visa timeout {0} msec.'.format(theInst.timeout))
print ('*IDN? {0}'.format(theInst.query('*IDN?').strip()))

# find out what to do
# note that confirmation codes are a bit arbitrary
def checkTree(msg):
	command, index, subidx = struct.unpack('<BHB', msg.data[0:4])
	if index in theTree:
		subTree = theTree[index]
		if subidx in subTree:
			subTree = subTree[subidx]
			if command in subTree:
			
				# now we know what to do
				what = subTree[command]
				if 0x40 == command:
					if isinstance(what, str):
						rslt = theInst.query(what)
						msg.data[0] = 0x43
						struct.pack_into('<f', msg.data, 4, float(rslt))
					elif isinstance(what, int):
						# assume byte unless told otherwise
						msg.data[0] = 0x4f
						if 'size' in subTree:
							size = subTree['size']
							if 4 == size:
								msg.data[0] = 0x43
						struct.pack_into('<L', msg.data, 4, what)
					else:
						print ('Unknown data type in object dictionary.')
						msg.data[0] = 0x80
						struct.pack_into('<L', msg.data, 4, 0x050400001)
				elif 0x23 == command:
					if isinstance(what, str):
						theInst.write(what + ' ' +
							str(struct.unpack_from('<f', msg.data, 4)[0]))
						msg.data[0] = 0x60
						msg.data[4:8] = [0]*4
					elif isinstance(what, int):
						msg.data[0] = 0x80
						struct.pack_into('<L', msg.data, 4, 0x06010002)
					else:
						# report instance error
						msg.data[0] = 0x80
						msg.data[4:8] = 0x060a0023
				else:
					# report data size error
					msg.data[0] = 0x80
					struct.pack_into('<L', msg.data, 4, 0x06040043)
			else:
				# report command error
				msg.data[0] = 0x80
				struct.pack_into('<L', msg.data, 4, 0x06010000)
		else:
			# report subidx error
			msg.data[0] = 0x80
			struct.pack_into('<L', msg.data, 4, 0x06090011)
	else:
		# report index error
		msg.data[0] = 0x80
		struct.pack_into('<L', msg.data, 4, 0x06020000)

	# always send reply
	msg.arbitration_id = 0x580 + theNode
	canBus.send(msg)
	
# CAN message handler
def msgHandler(msg):
	hiByte = (msg.arbitration_id >> 8) & 0xff
	loByte = msg.arbitration_id & 0xff
	
	# check channel and node address
	if (0x06 == hiByte) and (theNode == loByte): checkTree(msg)

# synchronous (blocking) wait for message
while True:
	theMsg = canBus.recv()
	
	# print (theMsg)
	msgHandler(theMsg)
	
