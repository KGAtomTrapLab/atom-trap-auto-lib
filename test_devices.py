# Testing devices that send default values for connections
from devices import Ramp_Controller
from digital_davll import Digital_DAVLL
from font_colors import color_red, color_yellow
import time
import math
import random

class Test_DAVLL(Digital_DAVLL):
    def connect(self):
        # Connect the ramp
        self.run_logger.log(f"Attempting to connect ramp on port {self.ramp_port} with baud rate {self.ramp_baud_rate}")
        self.ramp_controller = Test_Ramp(self.ramp_port, self.ramp_baud_rate) 
        self.ramp_controller.connect()
        connection_port = self.ramp_port
        controller_status = self.ramp_controller.get_status()
        self.run_logger.log(f"Ramp successfully connected on port {connection_port}")
        print(f"Current period (ms): {color_yellow(controller_status[0])}")
        print(f"Current Potentiometer Value: {color_yellow(controller_status[1])}")
        self._start_serial_reader()
    
    def process_packet(self, packet):
        output_array = []
        # Create a sine wave vased on the period
        for i in range(0, 4096):
            output_array.append(((16 * self.ramp_controller.pot) * math.cos(i / self.ramp_controller.period)) + ((random.random()-0.5) * 100))

        return output_array

class Test_Ramp(Ramp_Controller):
    '''
        Ramp Simulator for testing purposes
    '''
    def __init__(self, device_port, baud_rate):
        super().__init__(device_port, baud_rate)
        self.counter = 0

        self.period = 200
        self.valley_period = self.period / 10
        self.last_peak = time.perf_counter()

    def connect(self):
        self.connected = True
        return self.device_port
    
    def read_packet(self):
        return ""
    
    def check_for_peak_valley(self):
        check_time = time.perf_counter()
        if (check_time >= (self.last_peak + (self.period / 1000))):
            self.last_peak = check_time
            return 1
        # if (check_time >= self.last_peak + (self.valley_period / 100)):
        #     return 2
        return 0
    
    def set_period(self, value: int):
        self.period = value
    
    def set_wiper(self, value: int):
        self.pot = value
     
    def get_status(self):
        return self.period, 0
        
