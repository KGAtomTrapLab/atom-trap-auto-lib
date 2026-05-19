import serial
import time
import random
import threading

class Arduino:
    def __init__(self, device_port, baud_rate) -> None:
        self.device_port = device_port
        self.baud_rate = baud_rate
        self.serial_connection = None
        self.connected = False
        self.i = 0

    def connect(self):
        # TODO: Make something that looks for available devices and finds the most likely one

        self.serial_connection = serial.Serial(self.device_port, self.baud_rate)  # open serial port
        # Read the "Serial Initialized value sent"
        self.serial_connection.readline()
        self.connected = True
        # Device is connected
        return self.serial_connection.name
    
    # TODO: For any function that requires a connected device, make sure a conection has been made first
    def read(self):
        arduino_output = self.serial_connection.read()
        return arduino_output
    
    def readLine(self) -> str:
        '''
        Blocking function that taks in a line from the arduino
        
        '''
        # TODO: Add a timeout?
        
        arduino_output = self.serial_connection.readline()

        return arduino_output.decode("ascii")
    
    def send(self, value: str):
        '''
        Send a string to the device across the port.
        Does not gaurantee the string was received.
        
        :param value: Message to send to arduino
        '''
        # Encode into a bytes object for sending
        value_buffer = value.encode()
        self.serial_connection.write(value_buffer)
        # Write a newline
        self.serial_connection.write(b"\n")

    def close(self):
        self.serial_connection.close()             # close port

class Ramp_Controller(Arduino):
    def __init__(self, device_port, baud_rate) -> None:
        self.period = 200
        self.pot = 0
        self.rampstart = 0
        self.rampend = 4096
        super().__init__(device_port, baud_rate)

    def get_status(self):
        '''
        Get the status of the ramp controller.
        Returns [period(ms), wiper(0-128)]
        '''

        # Send the stat command
        self.send("stat")

        # Receive the data
        # Read period line
        # Await a value that isn't the peak notifier
        # TODO: Put this into a function to remove peak checker
        periodStr = 'p\r\n'
        while periodStr == 'p\r\n' or periodStr == 'v\r\n':
            periodStr = self.readLine()
        print("Value received: ", periodStr)
        period = int(periodStr)

        # Read wiper line
        wiperStr = self.readLine()
        wiper = int(wiperStr)

        return period, wiper

    def set_period(self, value: int):
        '''
        Set the period of the ramp time, in ms
        
        :param value: Number of ms for the period
        '''
        # Do not send if the value isn't an int
        if (value % 1 != 0) or (value <= 0):
            print("Please send an integer larger than 0.")
            return
        
        self.send(f"period {value}")
        self.period = value
        # Record period in class

    def set_wiper(self, value: int):
        '''
        Set the wiper on the potentiometer.
        
        :param value: Number from 0-127.
        '''
        # Do not send if the value isn't an int
        if (value % 1 != 0) or (value < 0) or (value >= 128):
            print("Please send an integer between 0-127")
            return
        
        self.send(f"pot {value}")
        self.pot = value

    def set_start(self, value: int):
        '''
            Set the starting position of the ramp
        '''
        self.send(f"rampstart {value}")
        self.rampstart = value

    def set_end(self, value: int):
        '''
            Set the ending position of the ramp
        '''
        self.send(f"rampend {value}")
        self.rampend = value

    def read_short(self):
        first_byte = self.read()
        second_byte = self.read()
        return int.from_bytes(first_byte+second_byte, byteorder='little', signed=True)


    
    def read_packet(self):
        '''
            Read a packet being sent across the arduino
        '''
        # Send a read request
        self.send("read")

        # Read the length of the packet
        pkt_lengths = self.read_short()
        # Arrays will never be longer than 4096. Send an error if this occurs
        if (pkt_lengths > 4096):
            print("Transmission Error Occured!")
            # TODO: Clear buffer
        # Read first array
        first_array = []
        for i in range(0, pkt_lengths):
            first_array.append(self.read_short())

        # Read second array
        second_array = []
        for i in range(0, pkt_lengths):
            second_array.append(self.read_short())

        return first_array, second_array