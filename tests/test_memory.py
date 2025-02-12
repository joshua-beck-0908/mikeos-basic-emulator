# This tests the memory module of the MikeOS Basic Emulator.
# It checks that the memory module can read and write bytes, words, and strings.

from memory import Memory

memory = Memory()

def test_read_write_byte() -> None:
    memory.write_byte(0x4000, 0x12)
    assert memory.read_byte(0x4000) == 0x12

def test_read_write_word() -> None:
    memory.write_word(0x4000, 0x1234)
    assert memory.read_word(0x4000) == 0x1234
    
def test_read_write_string() -> None:
    memory.write_string(0x4000, 'test')
    assert memory.read_string(0x4000, 4) == 'test'
    
def test_read_write_string_limit() -> None:
    memory.write_string(0x4000, 'test')
    assert memory.read_string(0x4000, 3) == 'tes'
    
def test_write_string_without_limit() -> None:
    memory.write_string(0x4000, 'test')
    assert memory.read_string(0x4000) == 'test'