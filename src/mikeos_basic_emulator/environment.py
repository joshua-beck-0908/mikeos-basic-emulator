# Environment manager for the MikeOS Basic Emulator
# This file ensures other parts can communicate with each other.

from pathlib import Path
import time
import typing

if typing.TYPE_CHECKING:
    from runcmd import CommandRunner
    from arglist import CommandArgumentList

from backend.interface.display import TextDisplay
from variables import VariableManager, ForVariable
from memory import Memory
from backend.pygame.display import PygameTextDisplay
#from backend.ncurses.display import CursesTextDisplay
from debugger import Debugger
from filesystem import SFNDirectory
from serialport import SerialPort
from sound import Speaker





class Environment():
    """
    This class hold the whole state of the emulator.
    It's passed to a command or debugger to connect all the other parts.
    """
    def __init__(self) -> None:
        self.memory = Memory()
        self.debugger = Debugger()
        self.variables = VariableManager(self.memory, self.debugger)
        #self.display: TextDisplay = CursesTextDisplay(
        self.display: TextDisplay = PygameTextDisplay(
            self.variables, self.debugger)
        self.filesystem = SFNDirectory(Path('virtual_disk'), self.memory)
        self.serial_port = SerialPort('NULL')
        self.speaker = Speaker()
        self.program_size = 0
        self.command_runner: CommandRunner|None = None
        self.do_stack: list[int] = []
        self.for_variables: dict[str, ForVariable] = {}
        self.gosub_stack: list[int] = []
        self.condition_stack: list[bool] = []
        self.program_counter = 0
        self.program_finished = False
        self.next_line_address = 0
        self.last_if_true = True
        self.next_command: CommandArgumentList|None = None

    def set_command_runner(self, command_runner: 'CommandRunner') -> None:
        self.command_runner = command_runner
        
    def get_command_runner(self) -> 'CommandRunner':
        if self.command_runner is None:
            raise ValueError('Command runner is not set.')
        return self.command_runner
        
    def delay(self, seconds: float) -> None:
        intervals = seconds * 20
        for _ in range(int(intervals)):
            time.sleep(0.05)
            if self.display.has_exited():
                raise SystemExit