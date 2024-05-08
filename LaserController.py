import InstrumentController
import logging

class LaserController(InstrumentController.InstrumentController):
    
    def __init__(self, resource_manager, resource_address):
        super().__init__(resource_manager, resource_address)

    # Turns the laser on
    def laser_on(self):
        self.send_command(':LASER ON')

    # Turns the laser off
    def laser_off(self):
        self.send_command(':LASER OFF')
    
    # Sets the current in mA
    def set_current(self, current):
        # Convert the current value from mA to A and format it in scientific notation
        current_in_A = "{:.2e}".format(int(current) * 10**-3)
        self.send_command(f':ILD:SET {current_in_A}')
        #logging.info(f"Current set to {current_in_A} A")

    # Gets the current in mA
    def get_current(self):
        current_in_A = self.query(':ILD:ACT?')
        current_in_mA = float(current_in_A) * 1000
        return current_in_mA
        
    def get_min_current(self):
        return self.query(':ILD:MIN?')
    
    def get_max_current(self):
        return self.query(':ILD:MAX?')
    
    # Sets the thermistor resistance in Ohms
    def set_thm_res(self, res):
        self.send_command(f':RESI:SET {res}')

    def get_thm_res(self):
        return self.query(':RESI:ACT?')
    
    def raise_current(self, amount):
        current = self.get_current()
        self.set_current(current + amount)

    def lower_current(self, amount):
        current = self.get_current()
        self.set_current(current - amount)
        
    


