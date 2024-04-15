from config import *
import InstrumentController
import LaserController
import OscilloscopeController


class VirtualLab():
    def __init(self):
        self.instruments = {}

    def instrument_connected(self, name):
        return name in self.instruments

    def connect_to_laser_controller(self, name, adddress, resource_man):

        laser = LaserController.LaserController(adddress, resource_man)
        laser.connect()
        if laser.is_connected():
            self.instruments[name] = laser
        else:
            print("Failed to connect to laser controller")
            return False
        

