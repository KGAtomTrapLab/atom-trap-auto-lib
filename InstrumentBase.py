from abc import ABC, abstractmethod


# Generic Base Class for Instruments
# Used to define basic methods that all instruments must implement

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
    def is_connected(self):
        pass



