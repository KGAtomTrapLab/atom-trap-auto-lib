from .InstrumentController import InstrumentController
import logging
import time

# Class for controlling the Laser Controller
# Inherits from InstrumentController
class LaserController(InstrumentController):
    
    def __init__(self, resource_manager, resource_address):
        super().__init__(resource_manager, resource_address)

    # Turns the laser on
    def laser_on(self):
        self.send_command(':LASER ON')

    def tec_on(self):
        '''
            Enable the thermistor control
        '''
        self.send_command(':TEC ON')

    # Turns the laser off
    def laser_off(self):
        self.send_command(':LASER OFF')

    def tec_off(self):
        '''
            Disable the thermistor control
        '''
        self.send_command(':TEC OFF')
    
    # Sets the current in mA
    def set_current(self, current):
        # Convert the current value from mA to A and format it in scientific notation
        current_in_A = "{:.2e}".format(float(current) * 10**-3)
        self.send_command(f':ILD:SET {current_in_A}')
        #logging.info(f"Current set to {current_in_A} A")

    # Gets the current in mA
    def get_current(self):
        current_in_A = self.query(':ILD:ACT?').split()[1]
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
        return float(self.query(':RESI:ACT?').split()[1])
    
    def raise_current(self, amount):
        current = self.get_current()
        self.set_current(current + amount)

    def lower_current(self, amount):
        current = self.get_current()
        self.set_current(current - amount)
        
    def set_resistance_and_wait(self, amount, threshold=20, check_iterations=400):
        '''
        Set the resistance value and block until the controller reaches this resistance.

        :param amount: Resistance value in ohms
        :param threshold: The ohmic range that the the resistance is considered within the target
        '''
        
        self.set_thm_res(amount)

        print("Target:", amount)
        print("Actual:", self.get_thm_res())

        while abs(amount - self.get_thm_res()) > threshold:
            print(self.get_thm_res())
            pass

        # check that the value is staying consistent

        num_iterations = 0
        while (num_iterations < check_iterations):
            actual_resistance = self.get_thm_res()
            print(actual_resistance)
            if abs(amount - actual_resistance) < threshold:
                num_iterations += 1
            else:
                num_iterations = 0
            time.sleep(0.0001)

        return
    
    def set_current_and_wait(self, amount, threshold=.2, check_iterations=20):
        '''
        Set the current value and block until the controller reaches this.

        :param amount: Current value in mA
        :param threshold: The range that the the current is considered within the target
        '''
        
        self.set_current(amount)

        while abs(amount - (float(self.get_current()))) > threshold:
            pass

        # check that the value is staying consistent

        num_iterations = 0
        adjusted_amount = 0
        total_num_iterations = 0
        while (num_iterations < check_iterations):
            total_num_iterations += 1
            # Loop to break out of a stuck control
            if (total_num_iterations > (check_iterations * 10)):
                # print("Entering loop")
                # error = amount - self.get_current()
                # adjusted_amount = amount + (error/2)
                # self.set_current(adjusted_amount)
                # total_num_iterations = 0
                break
            if abs(amount - self.get_current()) < threshold:
                num_iterations += 1
            else:
                num_iterations = 0
            time.sleep(0.001)

        return

