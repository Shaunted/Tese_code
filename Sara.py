#!/usr/bin/python3

import sys, serial, time

port = None #global variable of Serial port
cnc_connected = False
connect_timeout = 5

# CNC controls
def getStatus():
	if port is not None:
		if port.isOpen():
			port.write('?\r'.encode('utf-8'))
			time.sleep(1/10)
			if cnc_connected:
				if port.in_waiting > 0:
					something = port.read(port.in_waiting)
					start = something.decode('utf-8').find("<")
					end = something.decode('utf-8').find(">")
					if start < end and (start >= 0 and end >= 0):
						something = something[start+1:end]
						stat = something.decode().split("|")[0]
						xyz = something.decode().split("|")[1][5:].split(",")
						feedrate = something.decode().split("|")[2].split(",")[0][3:]
						port.flushInput() #flush input buffer, discarding all its contents
						port.flushOutput()#flush output buffer, aborting current output 
						return stat, xyz, feedrate
					else:
						port.flushInput() #flush input buffer, discarding all its contents
						port.flushOutput()#flush output buffer, aborting current output 
						return None, None, None
			else:
				port.flushInput() #flush input buffer, discarding all its contents
				port.flushOutput()#flush output buffer, aborting current output 

				return None, None, None

def writeConfiguration(config):
	for key in config:
		cmd = key + '=' + config[key] + '\r'
		self.printToConsole(message=cmd[:-2], newLine=True)
		port.write(cmd.encode('utf-8'))
		time.sleep(1/10)
	port.flushInput() #flush input buffer, discarding all its contents
	port.flushOutput()#flush output buffer, aborting current output 


def getConfiguration():
	config = {}
	port.write('$$\r'.encode('utf-8'))
	time.sleep(1/10)
	something = port.read(port.in_waiting)
	something = something.decode().rsplit("\r\n")
	for a in something[:-2]:
		line = a.split("=")
		config[line[0]] = line[1]
		self.printToConsole(message=a, newLine=True)
	return config


def goToPosition(self, lin_rap=0, x=None, y=None, z=None, feedrate=None):
	cmd = "G"

	if lin_rap: #linear1 rapid0
		cmd+="1"
	else: cmd+="0"
		
	cmd += " "

	if x is not None:
		cmd += "X" + str(x) + " "

	if y is not None:
		cmd += "Y" + str(y) + " "

	if z is not None:
		cmd += "Z" + str(z) + " "

	if feedrate is not None:
		cmd += "F" + str(feedrate)

	cmd += "\r"

	serialMutex.lock()
	port.write(cmd.encode('utf-8'))
	time.sleep(1/100)
	#something = port.read(port.in_waiting)
	port.flushInput() #flush input buffer, discarding all its contents
	port.flushOutput()#flush output buffer, aborting current output 
	serialMutex.unlock()



#decrease X
def man_left(self):
	if port is not None:
		stat, pos, feedrate = self.getStatus()
		if stat == "Idle":
			x=float(pos[0])- 1#mm
			if x >= 0:
				self.goToPosition(lin_rap=0, x=x)
			else:
				self.goToPosition(lin_rap=0, x=0)

#increase X
def man_right(self):
	if port is not None:
		stat, pos, feedrate = self.getStatus()
		if stat == "Idle":
			x=float(pos[0])+1#mm
			if x <= 140:
				self.goToPosition(lin_rap=0, x=x)
			else:
				self.goToPosition(lin_rap=0, x=140)



def main():
	global cnc_connected
	global connect_timeout
	global port
	print("Starting CNC application...")
	print("Scanning for COM ports...")
	try:
		from serial.tools.list_ports import comports
	except ImportError:
		return None
	if comports:
		index = 0
		print("Please choose a COM port:")
		for port in  list(comports()):
			print("[" + str(index) + "] - " + port.name)
			index = index + 1
		port_index = input('Enter port number: ')
		port_index = int(port_index)
		
	else:
		print("No COM ports available...")
		return

	print("Starting communication with port: " + list(comports())[port_index].name + " at 115200bps.")
	port = serial.Serial()
	port.port = "/dev/"+list(comports())[port_index].name
	port.baudrate = 115200
	port.bytesize = serial.EIGHTBITS #number of bits per bytes
	port.parity = serial.PARITY_NONE #set parity check: no parity
	port.stopbits = serial.STOPBITS_ONE #number of stop bits
	#port.timeout = None          #block read
	port.timeout = 1            #non-block read
	#port.timeout = 2              #timeout block read
	port.xonxoff = False     #disable software flow control
	port.rtscts = False     #disable hardware (RTS/CTS) flow control
	port.dsrdtr = False       #disable hardware (DSR/DTR) flow control
	port.writeTimeout = 2     #timeout for write

	try:
		port.open()
		print("Port opened ok.")
	except Exception as e:
		#print("If no permission: sudo chmod a+rw /dev/ttyACM0")
		print (str(e))
        
	if port.isOpen():
		try:
			print("Connecting to CNC: ")
			time_start = time.time()
			while cnc_connected == False:
				if time.time() - time_start > connect_timeout:
					print("Error connecting to CNC! (timeout reached)")
					break
				else:
					port.write("?\r".encode('utf-8'))
					if port.in_waiting > 10:
						cnc_connected = True
						print(str(port.read(port.in_waiting)))
						port.flushInput() #flush input buffer, discarding all its contents
						port.flushOutput()#flush output buffer, aborting current output 
						time.sleep(0.1) 
				if cnc_connected:
					print("CNC connect - OK")
		except Exception as e1:
			print ("error communicating...: " + str(e1))

	else:
		print("Port open - ERROR")
      
	print(getStatus())

 
if __name__ == "__main__":
		main()



