from InstrumentController import InstrumentController
from InstrumentController import VisaResourceManager
from LaserController import LaserController

visa_resource_manager = VisaResourceManager("C:\\WINDOWS\\system32\\visa32.dll")

print(visa_resource_manager.list_resources())

laser = LaserController(visa_resource_manager, 'GPIB0::8::INSTR')

laser.connect()

print(laser.status())






