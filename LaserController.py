import InstrumentController
import logging

class LaserController(InstrumentController):
    def set_current(self, intensity):
        self.send_command(f':ILD:SET {intensity}')
        logging.info(f"Current set to {intensity}")

    def get_current(self):
        return self.query(':ILD:ACT?')

    # Add more laser-specific methods here