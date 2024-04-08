import InstrumentController
import LaserController

visa_resource_manager = InstrumentController.VisaResourceManager("'C:\\WINDOWS\\system32\\visa32.dll'")

laser = LaserController(visa_resource_manager, 'GPIB0::8::INSTR')

laser.connect()

print(laser.status())






