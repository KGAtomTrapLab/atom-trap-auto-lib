# from gpib_ctypes import make_default_gpib
# make_default_gpib()

# import ctypes
# ctypes._load_lib('C:\\Windows\\System32\\gpib-32.dll')

import pyvisa
import logging

# Configure the logger to write to a file
logging.basicConfig(filename='pyvisa_log.txt', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# print(pyvisa.ResourceManager().visalib)
rm = pyvisa.ResourceManager('C:\\WINDOWS\\system32\\visa32.dll')
#rm = pyvisa.ResourceManager('C:\\WINDOWS\\SysWOW64\\visa32.dll')

# rm = pyvisa.ResourceManager('@py')
print(rm.list_resources('?*'))

#inst = rm.open_resource('GPIB0::8::INSTR')

#print(rm.list_resources('?*'))

#print(inst.query('*IDN?'))

# oscilloscope = rm.open_resource('USB0::0x0957::0x175D::MY49520268::INSTR')

# oscilloscope.write("*rst; status:preset; *cls")

