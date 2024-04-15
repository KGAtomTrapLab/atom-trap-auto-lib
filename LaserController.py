import InstrumentController
import logging

class LaserController(InstrumentController.InstrumentController):
    
    def __init__(self, resource_manager, resource_address):
        super().__init__(resource_manager, resource_address)

    def set_current(self, intensity):
        
        # Convert the current value from mA to A and format it in scientific notation
        current_in_A = "{:.2e}".format(int(intensity) * 10**-3)
        self.send_command(f':ILD:SET {current_in_A}')
        logging.info(f"Current set to {current_in_A} A")

    def get_current(self):
        return self.query(':ILD:ACT?')

    # Add more laser-specific methods here