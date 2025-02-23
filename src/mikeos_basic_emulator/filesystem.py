# This is the filesystem module of the MikeOS Basic Emulator.
# It is responsible for all disk operations.

import os
from pathlib import Path
import re

from memory import Memory

FilenameLookup = dict[str, str]

disk_path = Path('virtual_disk')


class SFNDirectory:
    """
    This class is responsible for managing the disk directory.

    The interpreter uses it to interact with the operating system's real
    files though a specific directory.

    All filenames are converted to 8.3 format as per the FAT filesystem
    specification. This is done to ensure compatibility with the MikeOS.

    This class keeps track of which real files correspond to which 8.3
    filenames and provides the interpreter with the necessary methods.
    
    Note that `read_files` must be called to populate the lookup tables.
    """
    def __init__(self, directory: Path, memory: Memory) -> None:
        self.directory = directory
        self.memory = memory
        self.lfn_lookup: FilenameLookup = {}
        self.sfn_lookup: FilenameLookup = {}

    
    def read_files(self) -> None:
        """
        Discovers all files in the directory and populates the lookup tables.
        
        The Basis-Name Generation Algorithm and Numeric-Tail Generation
        Algorithm are used to generate unique 8.3 filenames.
        
        This is a complex process and is broken down into several steps.
        """

        files: FilenameLookup = {}
        for file in self.directory.iterdir():
            if not file.is_file():
                continue

            existing_files = list(files.values())
            files[file.name] = self._convert_to_sfn(file.name, existing_files)
        self.lfn_lookup = files
        self.sfn_lookup = {v: k for k, v in files.items()}
    
    def list_full_names(self) -> list[str]:
        """
        Lists the full names of the files in the host OS directory.
        """
        return list(self.lfn_lookup.keys())
    
    def list_files(self) -> list[str]:
        """
        Lists all available simulated 8.3 filenames.

        These can be passed to the other functions.
        """
        return list(self.sfn_lookup.keys())
    
    def get_file_path(self, filename: str) -> Path:
        """
        Returns the real file path for a simulated 8.3 filename.
        
        A KeyError is raised if the file does not exist.
        """
        try:
            return self.directory / self.sfn_lookup[filename]
        except KeyError:
            return self.directory / filename
    
    def add_file(self, filename: str) -> None:
        """
        Creates a file if it does not exist.
        """
        new_name = self._convert_to_sfn(filename, self.list_full_names())
        new_path = self.directory / new_name
        if not new_path.exists():
            new_path.touch()
        self.read_files()

    def get_new_file_path(self, filename: str) -> Path:
        """
        Returns the real path of a simulated 8.3 filename.
        The file is created if it does not exist.
        """
        try:
            return self.directory / self.sfn_lookup[filename]
        except KeyError:
            self.add_file(filename)
            return self.get_file_path(filename)

            
    def get_existing_file_path(self, filename: str) -> Path:
        """
        Returns the real path of a simulated 8.3 filename.
        If the file does not exist, a FileNotFoundError is raised.
        """

        path = self.get_file_path(filename)
        if not path.exists():
            raise FileNotFoundError(f'File not found: {filename}')
        return path
        
    def get_file_size(self, filename: str) -> int:
        """
        Gets the size of a file in bytes.
        
        May raise a FileNotFoundError if the file does not exist.
        """

        path = self.get_existing_file_path(filename)
        return os.path.getsize(path)
    
    def load_file(self, filename: str, address: int) -> None:
        """
        Loads a file into the emulated memory.

        No ASCII conversion is done, the file is loaded as-is.
        
        A FileNotFoundError is raised if the file does not exist.
        """
        
        path = self.get_existing_file_path(filename)
        with open(path, 'rb') as file:
            data = file.read()
            self.memory.write_data(address, data)
            
    def save_file(self, filename: str, address: int, length: int) -> None:
        """
        Saves a file from the emulated memory to the host OS.
        
        May raise an OSError if the file cannot be written.
        """

        path = self.get_new_file_path(filename)
        with open(path, 'wb') as file:
            data = self.memory.read_data(address, length)
            file.write(data)
            
    def does_file_exist(self, filename: str) -> bool:
        """
        Checks if the give 8.3 filename exists simulated directory.
        """
        path = self.get_file_path(filename)
        if path.exists() and path.is_file():
            return True
        else:
            return False
        
    def delete_file(self, filename: str) -> None:
        """
        Deletes a file from the simulated directory and the host OS.
        """

        path = self.get_existing_file_path(filename)
        path.unlink()
        self.read_files()
        
    def rename_file(self, existing_name: str, new_name: str) -> None:
        """
        Renames a file in the simulated directory and the host OS.
        
        Note that the new host name will be the 8.3 filename.
        """
        path = self.get_existing_file_path(existing_name)
        new_name = self._convert_to_sfn(new_name, self.list_full_names())
        new_path = self.directory / new_name
        path.rename(new_path)
        self.read_files()
    
    def _convert_to_sfn(self, filename: str, existing_files: list[str]) -> str:
        """
        Converts a long filename to a valid 8.3 SFN.
        """
        filename, lossy = self._sanitize_filename(filename)
        base, too_long = self._get_basename(filename)
        ext = self._get_extension(filename)
        base = self._get_basename_with_tail(
            base, ext, existing_files, lossy, too_long
        )
        return base + ext

    def _sanitize_filename(self, filename: str) -> tuple[str, bool]:
        """
        Removes an characters that an not valid for a SFN (8.3 filename).

        This is part of the Basis-Name Generation Algorithm.

        It must also keep track of the "lossy" flag for the later 
        Numeric-Tail Generation Algorithm.
        e.g. if any characters are replaced, the flag is set to True.
        """
        lossy = False
        # SFNs must be all uppercase.
        filename = filename.upper()
        # Remove all spaces prior to processing.
        filename = filename.replace(' ', '')
        # Remove any leading periods.
        filename = re.sub(r'^\.*', '', filename)
        
        newname = ''
        for char in filename:
            if self._is_valid_for_8dot3_filename(char):
                newname += char
            else:
                # Any non-allowed character is replaced with an underscore.
                # The lossy flag is set if any character is replaced.
                lossy = True
                newname += '_'
        return (newname, lossy)
                
            

    def _is_valid_for_8dot3_filename(self, char: str) -> bool:
        """
        Checks if a character is valid for an 8.3 filename.
        This includes letters, numbers, and a few special characters.
        Or any character from 128 to 255.
        """
        
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

    def _get_basename(self, fullname: str) -> tuple[str, bool]:
        """
        Extracts the base name (part before the extension) for a SFN.
        
        Up to 8 characters are allowed for the base name.

        We must keep track of excessive length (the "too_long" flag) for the
        later Numeric-Tail Generation Algorithm.
        """
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
    
    def _get_extension(self, fullname: str) -> str:
        """
        Extracts the extension (part after the base name) for a SFN.
        
        This is up to 3 characters long.
        """
        # There may be multiple periods in a filename.
        # Or multiple file extensions (e.g. .tar.gz).
        # Only the last one is considered the extension!
        last_dot = fullname.rfind('.')
        if last_dot != -1:
            # Only take the dot plus the next 3 characters.
            # Any more characters are ignored.
            ext = fullname[last_dot:last_dot+4]
            if len(ext) == 1:
                return ''
            else:
                return ext
        else:
            return ''

    def _get_basename_with_tail(
        self,
        basename: str,
        ext: str,
        existing_sfns: list[str],
        lossy: bool,
        too_long: bool
        ) -> str:
        
        """
        Takes the original base name an overwrites part of it with a tilde
        and a number to make it unique.
        e.g. BASENAME -> BASENA~2
        
        Returns the new base name.
        
        This also needs access to the extension and the existing SFNs.

        Implements the Numeric-Tail Generation Algorithm.

        Needs the "lossy" and "too_long" flags from the previous steps to ensure the generated name is unique and valid.
        """

        # If no flags are set and the name is unique, do nothing.
        if (not lossy and 
            not too_long and 
            (basename + ext) not in existing_sfns and
            basename != ''):
                return basename
        
        # Otherwise keep trying to generate a unique name.
        for i in range(1, 1000000):
            # Generate the tail name.
            tail = f'~{i}'
            # The tail overwrites part of the base name.
            tail_length = len(tail)
            new_basename = basename[:8 - tail_length] + tail
            # Stop if the new name is unique, otherwise try the next number.
            if (new_basename + ext) not in existing_sfns:
                return new_basename
        raise ValueError('Unable to generate a unique SFN.')


        

        
    
        
    


