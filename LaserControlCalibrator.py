import laser_controller.InstrumentController as InstrumentController
import laser_controller.LaserController as LaserController
import time

class LaserControlCalibrator():
    def __init__(self):
        self.laser_controller = None

    def connect_laser_controller(self):
        device_manager = InstrumentController.DeviceManager("C:\\Windows\\System32\\visa32.dll")

        found_devices = device_manager.list_devices()

        laser_controller_address = ""
        for found_device in found_devices:
            if "GPIB0" in found_device:
                laser_controller_address = found_device

        self.laser_controller = LaserController.LaserController(device_manager, laser_controller_address)
        self.laser_controller.connect()
        print(self.laser_controller.status())

    
    def gather_data(self, res_min, res_max, res_step, cur_min, cur_max, cur_step, digital_davll):
        '''
        Accumulate data for different current and resistance values.
        '''

        num_resistor_intervals = int(res_max - res_min / res_step)
        num_current_intervals = int(cur_max - cur_min / cur_step)
        
        # Run through all resistance(temperature) values
        for i in range(0, num_resistor_intervals):
            target_resistance = res_min + (i * res_step)
            print(f"Setting resistance to {target_resistance}...")
            self.laser_controller.set_resistance_and_wait(target_resistance)
            print("Resistance set.")

            # Run through all current values
            for j in range(0, num_current_intervals):
                target_current = cur_min + (i * cur_step)
                print(f"Setting current to {target_current}...")
                self.laser_controller.set_current_and_wait(target_current)
                print("Current set.")
                print("Reading line of data...")
                digital_davll.clear_queue()
                digital_davll.get_data_line()