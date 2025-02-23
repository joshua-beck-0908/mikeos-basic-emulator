# This is the memory module of the MikeOS Basic Emulator.
# It is responsible for emulating the 64k memory of the emulated machine.

# TODO: Add address validation to the read and write methods.

class Memory:
    """
    This class simulates the 64 kiB memory of the emulated machine.
    
    Methods provided take the form of:
     - read_x(address: int) -> type
     - write_x(address: int, value: type) -> None
    
    Current types are:
     - byte (8 bits)
     - word (16 bits)
     - string (cp437 encoded, null terminated)
     - line (cp437 encoded, newline terminated)
     - data (fixed length byte array)

    
    """
    def __init__(self) -> None:
        self.data = bytearray(65536)

    def read_byte(self, address: int) -> int:
        """
        Reads a single 8-bit byte from memory.

        The values is returned as and unsigned integer between 0 and 255.
        """
        return self.data[address]

    def read_word(self, address: int) -> int:
        """
        Reads a 16-bit word from memory.

        The value is returned as an unsigned integer between 0 and 65535.
        """
        return self.data[address] + (self.data[address + 1] << 8)

    def write_byte(self, address: int, value: int) -> None:
        """
        Writes a single 8-bit byte to memory.
        The value must be an unsigned integer between 0 and 255.
        Out of range values will be truncated to 8 bits.
        """
        self.data[address] = value & 0xff

    def write_word(self, address: int, value: int) -> None:
        """
        Writes a 16-bit word to memory.
        The value must be an unsigned integer between 0 and 65535.
        Out of range values will be truncated to 16 bits.
        """
        self.data[address] = value & 0xff
        self.data[address + 1] = (value >> 8) & 0xff

    def read_string(self, 
        address: int, 
        limit: int = 127,
        terminator: int = 0) -> str:
        """
        Writes a null terminated string to memory.

        The string is read until the limit is reached or the terminator is 
        found. 
        
        If the limit is reached before the terminator, the string is truncated.
        
        The default limit is 127 characters as this is the maximum length of a
        MikeOS string by default.
        
        The string is decoded from cp437 encoding (the BIOS codepage).
        """

        encoded = self.data[address:address + limit]
        # Check for null terminator.
        # If present before the limit, use it's position as the length.
        if terminator in encoded:
            length = encoded.index(terminator)
        else:
            length = limit
        return encoded[:length].decode('cp437', 'replace')

    def write_string(self, 
        address: int, 
        string: str,
        limit: int = 127) -> None:
        """
        Writes a null terminated string to memory.
        
        The string is encoded to cp437 before being written.

        If the string is longer than the limit, it is truncated.
        
        One extra byte will be used for the null terminator.

        The default limit is 127 characters as this is the maximum length of a
        MikeOS string by default.
        """

        encoded = string.encode('cp437', 'replace')[:limit]
        self.data[address:address + len(encoded)] = encoded

    def dump(self, address: int, length: int) -> None:
        for i in range(address, address + length):
            print(f'{i:04x}: {self.data[i]:02x}')
            
            
    def read_line(self, address: int) -> str:
        """
        Reads a line of text from memory terminated by a newline character.

        The string is decoded from cp437 encoding (the BIOS codepage).

        The newline character is not included in the returned string.

        Up to 255 characters will be read before the newline character.
        """
        return self.read_string(address, 255, terminator=0x0A)
    
    def find_next_line(self, address: int) -> int:
        """
        Returns the address of the next line in memory.

        Search starts at the given address and continues until the first
        newline character is found.
        
        A ValueError is raised if no newline character is found.
        """
        return self.data.index(0x0A, address) + 1

    def find_string(self, 
        string: str, 
        start: int = 0, 
        limit: int = 65536) -> int:
        
        """
        Returns the first occurrence of the given string in memory between the
        start and limit addresses.
        
        A ValueError is raised if the string is not found.
        """
        
        encoded = string.encode('cp437', 'replace')
        index = self.data.find(encoded, start, limit)
        if index == -1:
            raise ValueError(f'String not found: {string}')
        return index
    

    def read_data(self, address: int, length: int) -> bytearray:
        """
        Reads a fixed length block of data from memory.

        Returns a bytearray of the data.
        
        This may be less than the requested length if the end of memory is
        reached.
        """
        return self.data[address:address + length]
    
    def write_data(self, address: int, data: bytes|bytearray) -> None:
        """
        Writes a fixed length block of data to memory.

        The data must be a bytes or bytearray object.

        The data will be truncated if it is longer than the available memory.
        """

        if type(data) == bytes:
            data = bytearray(data)
        self.data[address:address + len(data)] = data