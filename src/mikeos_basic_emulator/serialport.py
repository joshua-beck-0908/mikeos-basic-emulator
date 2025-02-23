# This file contains the serial interface code for the MikeOS BASIC emulator.

# TODO: Implement the serial interface.
class SerialPort:
    def __init__(self, device: str) -> None:
        self.device = device
        self.enabled = False
        self.baud_rate = 0
        self.buffer = bytearray()

    def setup(self, baud_rate: int) -> None:
        self.enabled = True
        self.baud_rate = baud_rate

    def read(self) -> int:
        return 0

    def write(self, value: int) -> None:
        self.buffer.append(value)
        
    def process_input(self, data: bytes) -> None:
        pass
    
    def flush_output(self) -> None:
        pass

