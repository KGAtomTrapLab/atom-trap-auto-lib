from devices import Ramp_Controller, Arduino, PD_Reader
from font_colors import color_yellow
from display_data import Data_Graph
import threading
import random

class Digital_DAVLL():
    ADC_RESOLUTION = 4096
    ADC_SUPPLY_VOLTAGE= 5

    def __init__(self, data_logger, ramp_port="COM7", ramp_baud_rate = 9600, pd_port="COM4", pd_baud_rate=115200):
        '''
        Create an instance of the DAVLL with the connection data
        
        :param log_file_dir: The location of logs for each run
        :param ramp_port: The address of the port that the ramp is connected to
        :param ramp_baud_rate: Baud rate of the ramp
        :param pd_port: Address of the photodiode reader port
        :param pd_baud_rate: Baud rate of the photodiode reader
        '''
        self.run_logger = data_logger

        self.ramp_port = ramp_port
        self.ramp_baud_rate = ramp_baud_rate
        self.ramp_controller = Ramp_Controller(ramp_port, ramp_baud_rate) 

        self.pd_port = pd_port
        self.pd_baud_rate = pd_baud_rate
        self.pd_reader = PD_Reader(pd_port, pd_baud_rate)

        self.channel_mode = 2

        self.print = False
        # Last packet printed from the ramp
        self.last_packet = b""

        self.graph = Data_Graph()
        self.graphing = False

    def connect(self):
        # Connect the ramp
        try:
            self.run_logger.log(f"Attempting to connect ramp on port {self.ramp_port} with baud rate {self.ramp_baud_rate}")
            self.ramp_controller = Ramp_Controller(self.ramp_port, self.ramp_baud_rate) 
            connection_port = self.ramp_controller.connect()
            print(f"Ramp controller connected on port {connection_port}")
            self.run_logger.log(f"Ramp successfully connected on port {connection_port}")
            controller_status = self.ramp_controller.get_status()
            print(f"Current period (ms): {color_yellow(controller_status[0])}")
            print(f"Current Potentiometer Value: {color_yellow(controller_status[1])}")
            self._start_serial_reader()
            return 0
        except Exception as e:
            self.run_logger.log("Ramp Connection Error.")
            self.run_logger.log(str(e))
            return -1


        # # Connect the photodiode reader
        # try:
        #     self.run_logger.log(f"Attempting to connect DAVLL on port {self.pd_port} with baud rate {self.pd_baud_rate}")
        #     connection_port = self.pd_reader.connect()
        #     print(f"DAVLL connected on port {connection_port}")
        # except Exception as e:
        #     self.run_logger.log("DAVLL Connection Error")
        #     self.run_logger.log(str(e))
        #     exit()

    def _start_serial_reader(self):
        print("Starting reader")
        def read_loop():
            while True:
                self.last_packet = self.ramp_controller.read_packet()
                processed_lines = self.process_packet(self.last_packet)
                if self.graphing:
                    self.graph.update_graph(processed_lines)
                threading.Event().wait(self.ramp_controller.period / 1000)

        t = threading.Thread(target=read_loop, daemon=True)
        t.start()

    def process_packet(self, packet):
        output_array = []
        for i in range(0, 200):
            output_array.append(random.random())

        return output_array

    def display_graph(self):
        self.graphing = True
        t = threading.Thread(target=self.graph.create_graph, daemon=True)
        t.start()
    

    def get_data_line(self):
        '''
        Grab the most recent output of data from the davll. 
        Synchrounous blocking function that awaits a period from the DAVLL.

        Returns

        '''
        # The array where each output from the DAVLL will be stored.
        output_data = [[],[]]
        # The index into output_data where the ramp changed directions from low to high
        valley_position = 0
        # Wait for peak signal, assigns the value to signal so it can be used for logic
        while (signal := self.ramp_controller.check_for_peak_valley()) != 1:
            # Grab the latest signal from the davll. 
            data_points = self.pd_reader.get_short()
            # Calibrate the voltage based on the ADC settings
            for i in range(0, self.channel_mode):
                calibrated_data_point = (data_points[i] / Digital_DAVLL.ADC_RESOLUTION) * Digital_DAVLL.ADC_SUPPLY_VOLTAGE
                output_data[i].append(calibrated_data_point)
            # If the signal is a 2(indicating valley), mark its position so it can be graphed
            # print(output_data)
            if signal == 2:
                valley_position = len(output_data) - 1
        # self.run_logger.write_dataline(output_data, valley_position)

        return output_data, valley_position
    
    # Record a line of data from the ramp
    def record_data_line(self):
        
    
    def clear_queue(self):
        self.pd_reader.clear_buffer()

if __name__ == "__main__":
    graph_davll = Digital_DAVLL()
    graph_davll.connect()
    graph_davll.graph_data_loop()