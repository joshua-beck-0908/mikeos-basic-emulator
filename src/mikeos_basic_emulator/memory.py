# This is the memory module of the MikeOS Basic Emulator.
# It is responsible for emulating the 64k memory of the emulated machine.

# TODO: Add address validation to the read and write methods.

class Memory:
    def __init__(self) -> None:
        self.data = bytearray(65536)

    def read_byte(self, address: int) -> int:
        return self.data[address]

    def read_word(self, address: int) -> int:
        return self.data[address] + (self.data[address + 1] << 8)

    def write_byte(self, address: int, value: int) -> None:
        self.data[address] = value

    def write_word(self, address: int, value: int) -> None:
        self.data[address] = value & 0xff
        self.data[address + 1] = (value >> 8) & 0xff

    def read_string(self, 
        address: int, 
        limit: int = 127,
        terminator: int = 0) -> str:

        encoded = self.data[address:address + limit]
        # Check for null terminator.
        # If present before the limit, use it's position as the length.
        if terminator in encoded:
            length = encoded.index(terminator)
        else:
            length = limit
        return encoded[:length].decode('ascii', 'replace')

    def write_string(self, 
        address: int, 
        string: str,
        limit: int = 127) -> None:

        encoded = string.encode('ascii', 'replace')[:limit]
        self.data[address:address + len(encoded)] = encoded

    def dump(self, address: int, length: int) -> None:
        for i in range(address, address + length):
            print(f'{i:04x}: {self.data[i]:02x}')
            
            
    def read_line(self, address: int) -> str:
        return self.read_string(address, 255, terminator=0x0A)
    
    def find_next_line(self, address: int) -> int:
        return self.data.index(0x0A, address) + 1

    # Returns the index of the first occurrence of the string in memory.
    # If not found, returns -1.
    def find_string(self, 
        string: str, 
        start: int = 0, 
        limit: int = 65536) -> int:
        
        encoded = string.encode('ascii', 'replace')
        return self.data.find(encoded, start, limit)

    def read_data(self, address: int, length: int) -> bytearray:
        return self.data[address:address + length]
    
    def write_data(self, address: int, data: bytes|bytearray) -> None:
        if type(data) == bytes:
            data = bytearray(data)
        self.data[address:address + len(data)] = data