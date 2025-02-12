# Environment manager for the MikeOS Basic Emulator
# This file ensures other parts can communicate with each other.

from pathlib import Path
import typing
if typing.TYPE_CHECKING:
    from runcmd import CommandRunner

from backend.interface.display import TextDisplay
from variables import VariableManager
from memory import Memory
from backend.pygame.display import PygameTextDisplay
from backend.ncurses.display import CursesTextDisplay
from debugger import Debugger
from filesystem import SFNDirectory



class Environment():
    def __init__(self) -> None:
        self.memory = Memory()
        self.debugger = Debugger()
        self.variables = VariableManager(self.memory)
        #self.display: TextDisplay = CursesTextDisplay(
        self.display: TextDisplay = PygameTextDisplay(
            self.variables, self.debugger)
        self.filesystem = SFNDirectory(Path('virtual_disk'), self.memory)
        self.program_size = 0
        self.command_runner: CommandRunner|None = None
        self.do_stack = []
        self.for_stack = []

    def set_command_runner(self, command_runner: 'CommandRunner') -> None:
        self.command_runner = command_runner
        
    def get_command_runner(self) -> 'CommandRunner':
        if self.command_runner is None:
            raise ValueError('Command runner is not set.')
        return self.command_runner
        