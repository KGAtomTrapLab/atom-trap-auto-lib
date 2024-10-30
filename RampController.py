import InstrumentBase
import serial

# Class to interface with custom voltage ramp
# Connects to Arduino over serial interface and wraps commands
class RampController(InstrumentBase.InstrumentBase):
    Max_Period = 1000000 # maxium period in mS

    def __init__(self, serial_port, baud_rate):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = None
        self.period = 1000 # Default Period of the ramp in mS
        self.voltage = 70 # Max voltage of the ramp in V
        self.pot_value = 127 # Poteiometer value from 1-127 Directly corrilated with voltage
        # Will likley need some varibles used for this voltage -> Pot value conversion
        


    def connect(self):
        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)

        if self.ser.isOpen():

            while(self.ser.readline().decode('utf-8').strip() != 'Serial Initilized'):
                print("Waiting for ramp controller to connect")

            print("Ramp controller connected")

            # Send inital period command
            self.set_period(self.period)

            # Send initial voltage command
            self.set_voltage(self.voltage)

        else:
            print("Error opening serial port")


        return self.ser.isOpen()
    
    def disconnect(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None
        return True
    
    def status(self):
        return self.ser.isOpen()
    
    def send_command(self, command):
        self.ser.write(command.encode())

        response = self.ser.readline()
        
        # return response for message verification
        return response.decode('utf-8').strip()
    
    def set_period(self, period):

        if period < 0 or period > RampController.Max_Period:
            print("Period out of range")
            print(" Period should be between 0 and " + str(RampController.Max_Period))
            return None
        
        # Send command to set period
        response = self.send_command(f"period {period}")

        if response == f"New Period: {period}":
            self.period = period
            return response
        else:
            print("Error setting period")
            print("Response: " + response)
            return None
        
    def set_pot(self, pot):
        
        if pot < 0 or pot > 127:
            print("Pot Value out of range")
            print(" Pot should be between 1 and 127")
            return None
        
        # Send command to set period
        response = self.send_command(f"pot {pot}")

        if response == f"New Wiper Position: {pot}" :
            self.pot = pot
            return response
        else:
            print("Error setting pot value")
            print("Response: " + response)
            return None
    
    '''TODO'''
    # Setitng the voltage requires some calculations using voltage values measured after amplification
    #  
    def set_voltage(self, voltage):
        pass
    

    
    

