# The is the command runner for the emulator.
# It imports and adds all commands.

from threading import Thread
import queue
from queue import Queue
import time

from parser import CommandParser
from arglist import CommandArgumentList, CommandRoutine
from environment import Environment
from instructions.builtins import all_commands as builtin_commands
from instructions.screen import all_commands as display_commands
from instructions.control import all_commands as control_commands
from instructions.disk import all_commands as disk_commands
from instructions.string import all_commands as string_commands
from instructions.key import all_commands as key_commands
from instructions.hardware import all_commands as hardware_commands
from instructions.data import all_commands as data_commands


all_commands: list[dict[str, CommandRoutine]] = [
    builtin_commands,
    display_commands,
    control_commands,
    disk_commands,
    string_commands,
    key_commands,
    hardware_commands,
    data_commands,
]

class InterpreterSyntaxError(Exception):
    """ For when a command has a syntax error. """
    
class EndOfProgramError(Exception):
    """ For when the end of the program is reached. """


class CommandRunnerThread(Thread):
    """ Used to run commands in a separate thread. """
    def __init__(self, env: Environment, command_queue: Queue[str]) -> None:
        super().__init__()
        self.env = env
        self.queue = command_queue
        self.interpreter = CommandRunner(env)
        self.to_run: list[str] = []
        self.env.set_command_runner(self.interpreter)
        self.running_from_memory = False
        self.all_done = False
        
    def run(self) -> None:
        while not (self.all_done or self.env.program_finished):
            if self.env.next_command is not None:
                self.interpreter.run_command(self.env.next_command)
                self.env.next_command = None

            try:
                self.run_from_queue()
            except queue.Empty:
                self.run_from_memory()
                
            time.sleep(0)
        self.env.display.exit()
            
    def run_from_queue(self) -> None:
        command = self.queue.get(block=False)
        if command.startswith('/'):
            self.run_special_command(command[1:])
        else:
            self.interpreter.run_command(command)
        self.queue.task_done()
        
    def run_special_command(self, command: str) -> None:
        """ Run commands added by the queue by the loader or debugger. """
        command = command.strip().upper()
        if command == 'EXIT':
            self.all_done = True
        elif command == 'RUN':
            self.running_from_memory = True
            
    def run_from_memory(self) -> None:
        """ Run commands from the program memory. """
        if not self.running_from_memory:
            return
        
        try:
            line = self.interpreter.read_program_line()
        except EndOfProgramError:
            self.running_from_memory = False
            self.env.debugger.on_program_exit(self.env)
            return
        else:
            self.interpreter.run_command(line)

class CommandRunner:
    """ Run BASIC commands passed through `run_command()` """
    def __init__(self, env: Environment) -> None:
        self.parser = CommandParser()
        self.commands: dict[str, CommandRoutine] = {}
        self.env = env
        self.register_all_commands()
    
    def register_command(self, 
        name: str, 
        command: CommandRoutine
        ) -> None:
        """
        Registers a runnable command keyword with the interpreter.
        """

        self.env.debugger.log_command_register(name)
        self.commands[name] = command

    def read_program_line(self) -> str:
        """
        Reads the next line from the program memory.
        
        The address of the next line is stored in `next_line_address` property
        of the environment.
        
        This address is calculated in advanced, but can be modified by control flow commands such as `LOOP` or `GOTO`.
        
        Raises `EndOfProgramError` if the end of the program is reached.
        """
        try:
            self.env.program_counter = self.env.next_line_address
            line = self.env.memory.read_line(self.env.program_counter)
            self.env.next_line_address = \
                self.env.memory.find_next_line(self.env.program_counter)
        except ValueError:
            raise EndOfProgramError()
        return line
    

    def decode_arguments(self, line: str) -> CommandArgumentList:
        """
        Converts a line of BASIC code into a list of arguments.
        """
        parts = self.parser.parse(line)
        return CommandArgumentList(parts, self.env.variables)

    def run_command(self, command: str|CommandArgumentList) -> None:
        """ 
        Runs a single BASIC command in the interpreter's environment.
        
        The command can be given as a string or argument list.
        
        The interpreter will check for any valid operation and run it.
        
        Numeric or string assignment is also done if required.

        Labels and comments will be ignored.
        
        An `InterpreterSyntaxError` will be raised if there is no valid 
        operation or command in the given input.
        """

        # If a string was passed, convert it to a list of arguments.
        if isinstance(command, str):
            self.env.debugger.log_command(f'Running command: "{command}"')
            command = self.decode_arguments(command)
        
        
        # Ignore empty lines, comments, labels, etc.
        if not command.has_any() or command.has_non_semantic():
            return
        # A numeric variable indicates an assignment.
        elif command.has_numeric_variable():
            self.execute_command('(assign)', command)
        # A string variable indicates a string assignment.
        elif command.has_string_variable():
            self.execute_command('(build_string)', command)
        # Otherwise expect a valid command word.
        elif command.has_word():
            self.execute_command(command.get_word(), command)
        else:
            raise InterpreterSyntaxError(
                'Line does not contain a command or assignment.'
            )

    def execute_command(self, name: str, args: CommandArgumentList) -> None:
        """
        Executes a command by name with a list of arguments.
        """
        if name not in self.commands:
            raise InterpreterSyntaxError(
                f'Unknown command: "{name}"'
            )
        self.commands[name](args, self.env)
        
    def register_all_commands(self) -> None:
        for commands in all_commands:
            for name, command in commands.items():
                self.register_command(name, command)
        
        