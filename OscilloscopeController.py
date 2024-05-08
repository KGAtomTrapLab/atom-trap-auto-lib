import InstrumentController
import logging

class OscilloscopeController(InstrumentController):
    def __init__(self, address, port):
        super().__init__(address, port)
        

    def reset(self):
        self.send_command("*rst; status:preset; *cls")
        logging.info("Oscilloscope reset")

    def set_timebase(self, timebase):
        self.send_command(f":TIMEBASE:SCALE {timebase}")
        logging.info(f"Timebase set to {timebase}")

    # Add more oscilloscope-specific methods heres