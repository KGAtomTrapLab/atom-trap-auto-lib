from .InstrumentController import InstrumentController
import logging
import time

MAX_CURRENT = 140

# Class for controlling the Laser Controller
# Inherits from InstrumentController
class LaserController(InstrumentController):
    
    def __init__(self, resource_manager, resource_address):
        super().__init__(resource_manager, resource_address)
        # The speed at which the current changes, in mA/sec
        self.current_change_speed = 5

        #Desired current and temperature
        self.target_current = 0
        self.target_thm_res = 0
        # Laser/tec on/off - 0 is off and 1 is on
        self.laser_status = 0
        self.tec_status = 0

    # Turns the laser on
    def laser_on(self):
        '''
            Turns the laser on SAFELY. Verifies safe control of laser
        '''
        print("TURNING LASER ON! PRESS ENTER WHEN READY.")
        input()
        # Make sure current is zero
        self.set_current(0)
        self.send_command(':LASER ON')
        self.laser_status = 1
        # Set tec to current value
        self.set_thm_res(self.get_thm_res())

    def tec_on(self):
        '''
            Enable the thermistor control
        '''
        self.send_command(':TEC ON')
        self.tec_status = 1

    # Turns the laser off
    def laser_off(self):
        # Ramp down the current level to zero
        while (self.target_current > self.current_change_speed):
            self.lower_current(self.current_change_speed)
            # Wait a moment
            time.sleep(0.25)
        self.send_command(':LASER OFF')
        self.laser_status = 0

    def tec_off(self):
        '''
            Disable the thermistor control
        '''
        self.send_command(':TEC OFF')
        self.tec_status = 0
    
    # Sets the current in mA
    def set_current(self, target_current):
        if target_current > MAX_CURRENT or target_current < 0:
            print("Error: Current value too large")
            return
        # SAFETY LOOP: The current starts at its current position and slowly ramps up to this value.
        start_current = self.get_current()
        self.target_current = target_current
        while abs(start_current - target_current) > self.current_change_speed:
            # TODO: Make ability to subtract when actual is above target
            next_target_current =  start_current + self.current_change_speed
            # Convert the current value from mA to A and format it in scientific notation
            current_in_A = "{:.4e}".format(float(target_current) * 10**-3)
            self.send_command(f':ILD:SET {current_in_A}')
            time.sleep(1)
            start_current = next_target_current

        # Finally, send the actual target
        current_in_A = "{:.4e}".format(float(target_current) * 10**-3)
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
        self.target_thm_res = res
        self.send_command(f':RESI:SET {res}')

    def get_thm_res(self):
        return float(self.query(':RESI:ACT?').split()[1])
    
    def raise_current(self, amount):
        current = self.get_current()
        self.set_current(current + amount)

    def lower_current(self, amount):
        current = self.get_current()
        self.set_current(current - amount)

    def raise_thm_res(self, amount):
        res = self.get_thm_res()
        self.set_current(res + amount)

    def lower_thm_res(self, amount):
        res = self.get_thm_res()
        self.set_current(res - amount)
        
    def set_resistance_and_wait(self, amount, threshold=20, check_iterations=400):
        '''
        Set the resistance value and block until the controller reaches this resistance.

        :param amount: Resistance value in ohms
        :param threshold: The ohmic range that the the resistance is considered within the target
        '''
        
        self.set_thm_res(amount)

        while abs(amount - self.get_thm_res()) > threshold:
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

