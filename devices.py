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
        if (value % 1 != 0) or (value <= 0) or (value >= 128):
            print("Please send an integer between 0-127")
            return
        
        self.send(f"pot {value}")
        self.pot = value

    def read_short(self):
        first_byte = self.read()
        second_byte = self.read()

        return first_byte + second_byte


    
    def read_packet(self):
        '''
            Read a packet being sent across the arduino
        '''
        read_value = self.read()
        # Await the header, parse single or dual channel
        while read_value != b'\xcc' and read_value != b'\xcd':
            read_value = self.read()

        # Read length
        arrays_length = int.from_bytes(self.read_short(), byteorder='little', signed=True)

        # Read arrays
        result_array = []
        while True:
            first_byte = self.read()
            second_byte = self.read()
            if first_byte == b'\xcb': break
            result = int.from_bytes(first_byte + second_byte, byteorder='little', signed=True)
            result_array.append(result)

        # Await footer
        return arrays_length, result_array




class PD_Reader(Arduino):
    def __init__(self, device_port, baud_rate) -> None:
        super().__init__(device_port, baud_rate)
        # Start and end signal for data
        self.START_SIGNAL = b"\xcc"
        self.END_SIGNAL = b"\xcb"

        self.channel_mode = 2

    def get_data(self) -> bytes:
        '''
        Gets all data sent across the serial port.

        Returns a bytestream of collected objects
        '''
        return b""
    
    def get_short(self) -> list[int]:
        '''
        Blocking function that receives the latest information broadcasted from the davll.

        Converts it into a short.
        
        :param self: Description
        :return: Description
        :rtype: int
        '''
        
        # Run until a complete value is safely received
        end_signal = b""
        first_byte = b""
        second_byte = b""
        result_values = []
        while (end_signal != self.END_SIGNAL):
            # Clear the serial buffer
            # self.serial_connection.reset_input_buffer()
            # Await a start signal
            start_value = b""
            while start_value != self.START_SIGNAL:
                start_value = self.serial_connection.read()
            # Grab two bytes
            for i in range(0, self.channel_mode):
                first_byte = self.serial_connection.read()
                second_byte = self.serial_connection.read()


                # Combine first and second byte, then convert into a 16-bit number
                output_stream = first_byte + second_byte
                # Communication is MSB, and the value is signed
                result_values.append(int.from_bytes(output_stream, 'little', signed=True))
            # Make sure an end signal is received
            end_signal = self.serial_connection.read()

        return result_values
    
    def clear_buffer(self):
        # Clear the serial buffer
        self.serial_connection.reset_input_buffer()
