from abc import ABC, abstractmethod


# Generic Base Class for Instruments and custom devices
# Used to define basic methods that all instruments and devices
# must implement

class InstrumentBase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send_command(self, command):
        pass

    @abstractmethod
    def status(self):
        pass



