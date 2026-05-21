import InstrumentController
import logging

'''TODO'''
# Expand class to utilize Osciliscope VISA commands


# Class to control the Oscilloscope
# Inherits from InstrumentController
class OscilloscopeController(InstrumentController):
    def __init__(self, address, port):
        super().__init__(address, port)
    
    def set_acquire_mode(self, mode):
        allowed_modes = ["NORMAL", "PEAK", "AVERAGE"]
        if mode not in allowed_modes:
            print(f"Invalid acquire mode: {mode}. Allowed modes: {allowed_modes}")
            return
        # Correct Mode entered, Change mode
        self.send_command(f":ACQUIRE:TYPE {mode}")
        print(f"Acquire mode set to {mode}")




    # def reset(self):
    #     self.send_command("*rst; status:preset; *cls")
    #     logging.info("Oscilloscope reset")

    # def set_timebase(self, timebase):
    #     self.send_command(f":TIMEBASE:SCALE {timebase}")
    #     logging.info(f"Timebase set to {timebase}")

    # Add more oscilloscope-specific methods heres