import InstrumentController
import LaserController
import time

class Laser_Control_Calibrator():
    def __init__(self):
        pass

    def test_laser_connection(self):
        # "C:\\Windows\\System32\\visa32.dll"

        device_manager = InstrumentController.DeviceManager("C:\\Windows\\System32\\visa32.dll")

        print(device_manager.list_devices())
        # TODO: Look for a device with the address GPIB0

        laser_controller_address = "GPIB0::8::INSTR"

        self.laser_controller = LaserController.LaserController(device_manager, laser_controller_address)

        self.laser_controller.connect()

        print(self.laser_controller.status())
    
    def gather_data(self, min_current, max_current, current_step, min_resistance, max_resistance, resistance_step):
        '''
        Accumulate data for different current and resistance values.
        '''
        
        # Run through all resistance(temperature) values
        for resistance in range(min_resistance, max_resistance, resistance_step):
            print(resistance)
            # Run through all current values


if __name__ == "__main__":
    control_calibrator = Laser_Control_Calibrator()
    control_calibrator.test_laser_connection()
    print(control_calibrator.laser_controller.set_thm_res(14200))
    time.sleep(60)
    # control_calibrator.gather_data(0, 100, 1, 80, 120, 1)