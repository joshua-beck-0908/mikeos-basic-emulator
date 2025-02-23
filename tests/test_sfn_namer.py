# This file contains test for the DOS 8.3 filename conversion.

import pytest
from pathlib import Path

from memory import Memory
from filesystem import SFNDirectory

# Full of *evil* filenames.
#test_dir = Path('tests/test_disk/testnames')

test_dir = Path('tests/test_disk')
memory = Memory()


def test_sanitizer_uppercases() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._sanitize_filename('test') == ('TEST', False)
    
def test_sanitizer_removes_spaces() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._sanitize_filename('test test') == ('TESTTEST', False)
    
def test_sanitizer_removes_leading_spaces() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._sanitize_filename(' test') == ('TEST', False)

def test_sanitizer_removes_leading_periods() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._sanitize_filename('.test') == ('TEST', False)

def test_sanitizer_removes_multiple_leading_periods() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._sanitize_filename('...test') == ('TEST', False)
    
def test_sanitizer_leaves_extension_period() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._sanitize_filename('test.txt') == ('TEST.TXT', False)
    
def test_sanitize_replaces_invalid_characters() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._sanitize_filename('test*&') == ('TEST_&', True)
    

def test_get_basename() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_basename('TEST.TXT') == ('TEST', False)
    
def test_get_basename_at_limit() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_basename('12345678.TXT') == ('12345678', False)
    
def test_get_basename_too_long() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_basename('123456789.TXT') == ('12345678', True)

def test_get_extension() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_extension('TEST.TXT') == '.TXT'

def test_get_extension_with_no_extension() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_extension('TEST') == ''
    
def test_get_extension_with_no_extension2() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_extension('TEST.') == ''
    
def test_get_extension_wtih_witout_basename() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_extension('.TXT') == '.TXT'
    
def test_get_extension_with_short_extension() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_extension('TEST.T') == '.T'
    
def test_get_extension_with_long_extension() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_extension('TEST.TEXT') == '.TEX'
    
def test_get_extension_with_multiple_extensions() -> None:
    fname = SFNDirectory(test_dir, memory)
    assert fname._get_extension('TEST.TAR.GZ') == '.GZ'
    
def test_read_files() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    assert sorted(fname.list_files()) == [
        'AUTORUN.BAS',
        'FILEONE.TEX',
        'THE_SE~1.TXT',
    ]
    
def test_load_file() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    data = 'This is file one.'.encode('ascii')
    with open(test_dir / 'fileone.texty', 'wb') as file:
        file.write(data)
    fname.load_file('FILEONE.TEX', 0x1000)
    assert memory.read_data(0x1000, len(data)) == data
    
def test_load_file_not_found() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    with pytest.raises(FileNotFoundError):
        fname.load_file('FILETWO.TEX', 0x1000)
    
def test_save_file() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    data = 'This is file one.'.encode('ascii')
    memory.write_data(0x1000, data)
    fname.save_file('FILEONE.TEX', 0x1000, len(data))
    with open(test_dir / 'fileone.texty', 'rb') as file:
        assert file.read() == data
        
def test_does_file_exist_true() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    assert fname.does_file_exist('FILEONE.TEX')
    
def test_does_file_exist_false() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    assert not fname.does_file_exist('FILETWO.TEX')
    
def test_delete_file() -> None:
    fname = SFNDirectory(test_dir, memory)
    tmpfile = test_dir / 'TEMP.TXT'
    tmpfile.touch()
    fname.read_files()
    with open(tmpfile, 'w') as file:
        file.write('delete me')
    fname.delete_file('TEMP.TXT')
    assert not fname.does_file_exist('TEMP.TXT')
    
def test_delete_file_not_found() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    with pytest.raises(FileNotFoundError):
        fname.delete_file('FILETWO.TEX')

def test_rename_file() -> None:
    fname = SFNDirectory(test_dir, memory)
    tmpfile = test_dir / 'TEMP.TXT'
    tmpfile2 = test_dir / 'TEMP2.TXT'
    tmpfile.touch()
    fname.read_files()
    fname.rename_file('TEMP.TXT', 'TEMP2.TXT')
    assert fname.does_file_exist('TEMP2.TXT')
    assert not fname.does_file_exist('TEMP.TXT')
    tmpfile.unlink(missing_ok=True)
    tmpfile2.unlink(missing_ok=True)
    
def test_rename_file_not_found() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    with pytest.raises(FileNotFoundError):
        fname.rename_file('TEMP.TXT', 'TEMP2.TXT')
        
def test_get_file_size() -> None:
    fname = SFNDirectory(test_dir, memory)
    fname.read_files()
    tmpfile = test_dir / 'TEMP.TXT'
    data = 'This is a test file.'.encode('ascii')
    with open(tmpfile, 'wb') as file:
        file.write(data)
    assert fname.get_file_size('TEMP.TXT') == len(data)
    tmpfile.unlink()