import InstrumentController
import LaserController

class Laser_Control_Calibrator():
    def __init__(self):
        pass

    def test_laser_connection(self):
        # "C:\\Windows\\System32\\visa32.dll"

        device_manager = InstrumentController.DeviceManager("C:\\Windows\\System32\\visa32.dll")

        print(device_manager.list_devices())

        laser_controller_address = "GPIOB0::2::INSTR"

        laser_controller = LaserController.LaserController(device_manager, laser_controller_address)

        laser_controller.connect()

        print(laser_controller.status())
    
    def gather_data(self):
        '''
        Accumulate data for different current and resistance values.
        '''
        
        # Run through all resistance(temperature) values

            # Run through all current values


if __name__ == "__main__":
    control_calibrator = Laser_Control_Calibrator()
    control_calibrator.test_laser_connection()