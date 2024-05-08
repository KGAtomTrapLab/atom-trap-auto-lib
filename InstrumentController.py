import pyvisa
import logging
from InstrumentBase import InstrumentBase

# Class to wrap around PyVisa's resource manager
class DeviceManager:
    def __init__(self, visa_library_path=None):
        self.visa_library_path = visa_library_path
        self.resource_manager = pyvisa.ResourceManager(visa_library_path)

    def list_resources(self):
        """List all connected VISA resources."""
        return self.resource_manager.list_resources('?*')


# Generic Instrement Controller class
# Includes methods for connecting, disconnecting, sending commands, and querying
class InstrumentController(InstrumentBase):
    def __init__(self, visa_resource_manager, resource_address):
        self.visa_resource_manager = visa_resource_manager
        self.resource_address = resource_address
        self.instrument = None

    def connect(self):
        self.instrument = self.visa_resource_manager.resource_manager.open_resource(self.resource_address)
        logging.info(f"Connected to {self.resource_address}")

        logging.info(f"Connected to Inst. at: {self.instrument.query("*IDN?")}")

    def disconnect(self):
        if self.instrument:
            self.instrument.close()
            logging.info(f"Disconnected from {self.resource_address}")

    def status(self):
        if self.instrument:
            return f"Connected to Inst. at: {self.resource_address}"
        else:
            return "Not connected"

    def send_command(self, command):
        if self.instrument:
            self.instrument.write(command)
            logging.info(f"Sent command: {command}")

    def query(self, query):
        if self.instrument:
            response = self.instrument.query(query)
            logging.info(f"Query: {query} - Response: {response}")
            return response
        
