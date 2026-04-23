from devices import Ramp_Controller, Arduino, PD_Reader
from font_colors import color_yellow
from display_data import Data_Graph
from log_data import DataLogger
import threading
import random
import time
import traceback

class Digital_DAVLL():
    ADC_RESOLUTION = 4096
    ADC_SUPPLY_VOLTAGE= 5

    def __init__(self, data_logger: DataLogger, ramp_port="COM4", ramp_baud_rate = 9600, pd_port="COM4", pd_baud_rate=115200):
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
        # Record all lines from the reader
        self.recording_all = False

        # Output from PD readers
        self.davll_output = []
        
        '''
            A flag that is toggled once a new line of data has been processed.
            The reader constantly sets it to True, and other functions can set it
            to False and await it being true
        '''
        self.new_output_event = threading.Event()


    def connect(self):
        # Connect the ramp
        try:
            self.run_logger.log(f"Attempting to connect ramp on port {self.ramp_port} with baud rate {self.ramp_baud_rate}")
            self.ramp_controller = Ramp_Controller(self.ramp_port, self.ramp_baud_rate) 
            connection_port = self.ramp_controller.connect()
            self.ramp_controller.serial_connection.reset_input_buffer()
            print(f"Ramp controller connected on port {connection_port}")
            self.run_logger.log(f"Ramp successfully connected on port {connection_port}")
            try:
                controller_status = self.ramp_controller.get_status()
                print(f"Current period (ms): {color_yellow(controller_status[0])}")
                print(f"Current Potentiometer Value: {color_yellow(controller_status[1])}")
            except:
                print("Could not get controller status")

            
            self._start_serial_reader()
            return 0
        except Exception as e:
            self.run_logger.log("Ramp Connection Error.")
            traceback.print_exc()
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
                try:
                    arrays_length, self.last_packet = self.ramp_controller.read_packet()
                    self.davll_output = self.process_packet(self.last_packet, arrays_length)
                    self.new_output_event.set()
                    # Record if enabled
                    if self.recording_all:
                        self.run_logger.write_dataline(self.davll_output)
                    if self.graphing:
                        self.graph.update_graph(self.davll_output)
                except Exception as e:
                    print("Read crash:")
                    traceback.print_exc()

        t = threading.Thread(target=read_loop, daemon=True)
        t.start()

    def toggle_record(self):
        '''
            Turn recording of all ramp data on or off
        '''
        self.recording_all = not self.recording_all
        return self.recording_all

    def process_packet(self, packet, arrays_length):
        first_packet = packet[0:arrays_length]
        second_packet = packet[arrays_length:]

        return first_packet, second_packet

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
        # Clear the output flag and wait for it to be set
        self.new_output_event.wait()
        self.new_output_event.clear()
        return self.davll_output
    
    # # Record a line of data from the ramp
    # def record_data_line(self):

    
    def clear_queue(self):
        self.pd_reader.clear_buffer()

if __name__ == "__main__":
    graph_davll = Digital_DAVLL()
    graph_davll.connect()
    graph_davll.graph_data_loop()