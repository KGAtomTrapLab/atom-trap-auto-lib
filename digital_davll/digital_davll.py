from .devices import Ramp_Controller, Arduino, PD_Reader, Fake_Ramp
from .font_colors import color_yellow
from .display_data import graph_data
from .log_data import DataLogger

class Digital_DAVLL():
    ADC_RESOLUTION = 4096
    ADC_SUPPLY_VOLTAGE= 5

    def __init__(self, log_file_dir="./logs", ramp_port="COM7", ramp_baud_rate = 9600, pd_port="COM4", pd_baud_rate=115200):
        '''
        Create an instance of the DAVLL with the connection data
        
        :param log_file_dir: The location of logs for each run
        :param ramp_port: The address of the port that the ramp is connected to
        :param ramp_baud_rate: Baud rate of the ramp
        :param pd_port: Address of the photodiode reader port
        :param pd_baud_rate: Baud rate of the photodiode reader
        '''

        self.log_file_dir = log_file_dir
        self.run_logger = DataLogger(log_file_dir)

        self.ramp_port = ramp_port
        self.ramp_baud_rate = ramp_baud_rate
        self.ramp_controller = Ramp_Controller(ramp_port, ramp_baud_rate) 

        self.pd_port = pd_port
        self.pd_baud_rate = pd_baud_rate
        self.pd_reader = PD_Reader(pd_port, pd_baud_rate)

        self.channel_mode = 2

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
        except Exception as e:
            self.run_logger.log("Ramp Connection Error")
            self.run_logger.log(str(e))
            exit()


        # Connect the photodiode reader
        try:
            self.run_logger.log(f"Attempting to connect DAVLL on port {self.pd_port} with baud rate {self.pd_baud_rate}")
            connection_port = self.pd_reader.connect()
            print(f"DAVLL connected on port {connection_port}")
        except Exception as e:
            self.run_logger.log("DAVLL Connection Error")
            self.run_logger.log(str(e))
            exit()


    
    def graph_data_loop(self):
        graph_data(self.ramp_controller, self.pd_reader, self.run_logger)

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
            if signal == 2:
                valley_position = len(output_data) - 1
        self.run_logger.write_dataline(output_data, valley_position)

        return output_data, valley_position

if __name__ == "__main__":
    graph_davll = Digital_DAVLL()
    graph_davll.connect()
    graph_davll.graph_data_loop()