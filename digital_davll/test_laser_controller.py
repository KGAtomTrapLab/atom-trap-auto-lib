import pyvisa
import sys

#Opens a resource manager and shows the available VISA devices.
rm = pyvisa.ResourceManager()


#Opens the connection to the device. The variable instr is the handle for the device.
#The 'USB0...' number for a device can e.g. be found in the returned list of rm.list_resources(). 
print(rm.list_resources())

# print("Used device: ",instr.query('*IDN?'))