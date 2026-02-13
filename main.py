import InstrumentController
import LaserController
import time

class Laser_Control_Calibrator():
    def __init__(self):
        self.laser_controller = None

    def test_laser_connection(self):
        # "C:\\Windows\\System32\\visa32.dll"

        device_manager = InstrumentController.DeviceManager("C:\\Windows\\System32\\visa32.dll")

        print(device_manager.list_devices())
        # TODO: Look for a device with the address GPIB0

        laser_controller_address = "GPIB0::8::INSTR"

        self.laser_controller = LaserController.LaserController(device_manager, laser_controller_address)

        self.laser_controller.connect()

        print(self.laser_controller.status())

    def connect_laser_controller(self):
        device_manager = InstrumentController.DeviceManager("C:\\Windows\\System32\\visa32.dll")

        found_devices = device_manager.list_devices()
    
    def gather_data(self, res_min, res_max, res_step, cur_min, cur_max, cur_step):
        '''
        Accumulate data for different current and resistance values.
        '''

        num_resistor_intervals = res_max - res_min / res_step
        num_current_intervals = cur_max - cur_min / cur_step
        
        # Run through all resistance(temperature) values
        for i in range(0, num_resistor_intervals):
            target_resistance = res_min + (i * res_step)

            # Run through all current values


if __name__ == "__main__":
    control_calibrator = Laser_Control_Calibrator()
    control_calibrator.test_laser_connection()
    print(control_calibrator.laser_controller.set_thm_res(14200))
    time.sleep(60)
    # control_calibrator.gather_data(0, 100, 1, 80, 120, 1)