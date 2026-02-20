import time


class DataLogger():
    '''
    A class to log all data on current run of ramp/DAVLL.

    :param log_folder: The folder location of data logs.
    '''
    def __init__(self, log_folder) -> None:
        self.folder = log_folder
        self.make_log()

    def make_log(self):
        '''
        Creates a new file called "run_currentdate/time.log"
        '''
        # Make string for start time
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.file = open(f"{self.folder}/{timestr}.log", "w")
        # Print some standard information
        self.file.write(f"Gillen Atom Trap Ramp Controller\nSTART TIME: {time.strftime('%H:%M:%S %m-%d-%Y')}\n")

    def log(self, msg):
        self.writeTime()
        self.file.write(msg)
        self.file.write("\n")

    def write_dataline(self, dataArray, valley_position=0):
        '''
        write a line of data, synchronized with one ramp edge
        
        :param dataArray: array of values from the davll
        :param valley_position: the index into the array where the ramp started rising
        '''
        self.writeTime()
        self.file.write(f"RAMP START: {valley_position},")
        self.file.write("DAVLL: ")
        for number in dataArray:
            self.file.write(f"{number},")
        self.file.write("\n")

    def writeTime(self):
        self.file.write(f"{time.strftime('%H:%M:%S %m-%d-%Y')}\t")

    def close_log(self):
        self.file.close()

    