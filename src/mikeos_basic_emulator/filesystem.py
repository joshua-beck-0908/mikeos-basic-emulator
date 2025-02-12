# This is the filesystem module of the MikeOS Basic Emulator.
# It is responsible for all disk operations.

import os
from pathlib import Path
import re

from memory import Memory

FilenameLookup = dict[str, str]

disk_path = Path('virtual_disk')


class SFNDirectory:
    def __init__(self, directory: Path, memory: Memory) -> None:
        self.directory = directory
        self.memory = memory
        self.lfn_lookup: FilenameLookup = {}
        self.sfn_lookup: FilenameLookup = {}

    
    def read_files(self) -> None:
        files: FilenameLookup = {}
        for file in self.directory.iterdir():
            if not file.is_file():
                continue

            existing_files = list(files.values())
            files[file.name] = self.convert_to_sfn(file.name, existing_files)
        self.lfn_lookup = files
        self.sfn_lookup = {v: k for k, v in files.items()}
    
    def list_full_names(self) -> list[str]:
        return list(self.lfn_lookup.keys())
    
    def list_files(self) -> list[str]:
        return list(self.sfn_lookup.keys())
    
    def get_file_path(self, filename: str) -> Path:
        try:
            return self.directory / self.sfn_lookup[filename]
        except KeyError:
            return self.directory / filename
    
    def add_file(self, filename: str) -> None:
        new_name = self.convert_to_sfn(filename, self.list_full_names())
        new_path = self.directory / new_name
        if not new_path.exists():
            new_path.touch()
        self.read_files()

    def get_new_file_path(self, filename: str) -> Path:
        try:
            return self.directory / self.sfn_lookup[filename]
        except KeyError:
            self.add_file(filename)
            return self.get_file_path(filename)

            
    def get_existing_file_path(self, filename: str) -> Path:
        path = self.get_file_path(filename)
        if not path.exists():
            raise FileNotFoundError(f'File not found: {filename}')
        return path
        
    def get_file_size(self, filename: str) -> int:
        path = self.get_existing_file_path(filename)
        return os.path.getsize(path)
    
    def load_file(self, filename: str, address: int) -> None:
        path = self.get_existing_file_path(filename)
        with open(path, 'rb') as file:
            data = file.read()
            self.memory.write_data(address, data)
            
    def save_file(self, filename: str, address: int, length: int) -> None:
        path = self.get_existing_file_path(filename)
        with open(path, 'wb') as file:
            data = self.memory.read_data(address, length)
            file.write(data)
            
    def does_file_exist(self, filename: str) -> bool:
        path = self.get_file_path(filename)
        if path.exists() and path.is_file():
            return True
        else:
            return False
        
    def delete_file(self, filename: str) -> None:
        path = self.get_existing_file_path(filename)
        path.unlink()
        self.read_files()
        
    def rename_file(self, existing_name: str, new_name: str) -> None:
        path = self.get_existing_file_path(existing_name)
        new_name = self.convert_to_sfn(new_name, self.list_full_names())
        new_path = self.directory / new_name
        path.rename(new_path)
        self.read_files()
    
    def convert_to_sfn(self, filename: str, existing_files: list[str]) -> str:
        filename, lossy = self.sanitize_filename(filename)
        base, too_long = self.get_basename(filename)
        ext = self.get_extension(filename)
        base = self.get_basename_with_tail(
            base, ext, existing_files, lossy, too_long
        )
        return base + ext

    def sanitize_filename(self, filename: str) -> tuple[str, bool]:
        lossy = False
        # SFNs must be all uppercase.
        filename = filename.upper()
        # Remove all spaces prior to processing.
        filename = filename.replace(' ', '')
        # Remove any leading periods.
        filename = re.sub(r'^\.*', '', filename)
        
        newname = ''
        for char in filename:
            # Any non-allowed character is replaced with an underscore.
            # The lossy flag is set if any character is replaced.
            if self.is_valid_for_8dot3_filename(char):
                newname += char
            else:
                lossy = True
                newname += '_'
        return (newname, lossy)
                
            

    def is_valid_for_8dot3_filename(self, char: str) -> bool:
        # According to Microsoft's specification for 8.3 filenames.
        # Allowed characters are:

        # Alphanumeric characters
        if char.isalnum():
            return True
        # One of the following characters:
        elif char in "$%'-_@~`!(){}^#&":
            return True
        # One period for marking the extension
        elif char == '.':
            return True
        # Any codepoint from 128 to 255
        elif 127 < ord(char) < 256:
            return True
        # Replace any other character with an underscore
        else:
            return False

    def get_basename(self, fullname: str) -> tuple[str, bool]:
        basename = ''
        too_long = False
        for n, char in enumerate(fullname):
            if char == '.':
                break
            if n > 7:
                too_long = True
                break
            basename += char
        return (basename, too_long)
    
    def get_extension(self, fullname: str) -> str:
        last_dot = fullname.rfind('.')
        if last_dot != -1:
            ext = fullname[last_dot:last_dot+4]
            if len(ext) == 1:
                return ''
            else:
                return ext
        else:
            return ''

    def get_basename_with_tail(
        self,
        basename: str,
        ext: str,
        existing_sfns: list[str],
        lossy: bool,
        too_long: bool
        ) -> str:

        if (not lossy and 
            not too_long and 
            (basename + ext) not in existing_sfns and
            basename != ''):
                return basename
        
        for i in range(1, 1000000):
            tail = f'~{i}'
            tail_length = len(tail)
            new_basename = basename[:8 - tail_length] + tail
            if (new_basename + ext) not in existing_sfns:
                return new_basename
        raise ValueError('Unable to generate a unique SFN.')


        

        
    
        
    


