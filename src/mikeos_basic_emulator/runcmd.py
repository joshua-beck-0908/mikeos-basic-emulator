# The is the command runner for the emulator.
# It imports and adds all commands.

from threading import Thread
from queue import Queue

from parser import CommandParser
from parser import TokenType, Token
from argument import CommandArgument
from arglist import CommandArgumentList, CommandRoutine
from environment import Environment
from instructions.screen import all_commands as display_commands
from instructions.control import all_commands as control_commands
from instructions.disk import all_commands as disk_commands
from instructions.string import all_commands as string_commands


all_commands: list[dict[str, CommandRoutine]] = [
    display_commands,
    control_commands,
    disk_commands,
    string_commands,
]

class InterpreterSyntaxError(Exception):
    """ For when a command has a syntax error. """


class CommandRunnerThread(Thread):
    """ Used to run commands in a separate thread. """
    def __init__(self, env: Environment, command_queue: Queue[str]) -> None:
        super().__init__()
        self.env = env
        self.queue = command_queue
        self.interpreter = CommandRunner(env)
        self.to_run: list[str] = []
        self.env.set_command_runner(self.interpreter)
        
    def run(self) -> None:
        while True:
            command = self.queue.get()
            if command.strip().upper() == '/EXIT':
                self.queue.task_done()
                break
            self.interpreter.run_command(command)
            self.queue.task_done()

        if self.env.debugger.enabled:
            self.env.debugger.program_exit(self.env)

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

        self.env.debugger.log_command_register(name)
        self.commands[name] = command

    def run_command(self, command: str) -> None:
        self.env.debugger.log_command(f'Running command: "{command}"')
        parts = self.parser.parse(command)
        
        # If the command is empty (e.g. a blank line) then do nothing.
        if len(parts) == 0:
            return
        
        # Now look at the first token to determine what to do.
        cmdtoken = parts[0]

        # If the if it's a comment, then do nothing.
        if cmdtoken.type == TokenType.COMMENT:
            return
        # If is a numeric variable try to do an assignment.
        elif cmdtoken.type == TokenType.VARIABLE:
            self.do_numeric_assignment(parts)
        # If it's a string variable try string building.
        elif cmdtoken.type == TokenType.STRING_VAR:
            self.do_string_assignment(parts)
        # Assume a word is a command.
        elif cmdtoken.type == TokenType.WORD:
            self.do_command(parts)
        else:
            raise InterpreterSyntaxError(
                'Line does not contain a command or assignment.'
            )
            
    def do_numeric_assignment(self, parts: list[Token]) -> None:
        if len(parts) < 3:
            raise InterpreterSyntaxError(
                'Numeric assignment must have a variable and a value.'
            )
            
        sum_variable = CommandArgument(
            parts[0], 
            self.env.variables
        ).to_numeric_variable()
        if parts[1].type != TokenType.SYMBOL or parts[1].value != '=':
            raise InterpreterSyntaxError(
                'Second token must be an assignment operator.'
            )
        
        sum = 0
        pending_operator = '='
        for part in parts[2:]:
            arg = CommandArgument(part, self.env.variables)
            if pending_operator != '':
                value = arg.to_numeric()
                sum = self.apply_operator(sum, value, pending_operator)
                pending_operator = ''
            else:
                pending_operator = arg.to_symbol()
                
        if pending_operator != '':
            raise InterpreterSyntaxError(
                'Unexpected end of line in numeric assignment.'
            )
            
        self.env.variables.set_numeric_variable(sum_variable, sum)
        
    def apply_operator(self, sum: int, value: int, operator: str) -> int:
        if operator == '+':
            result = sum + value
        elif operator == '-':
            result = sum - value
        elif operator == '*':
            result = sum * value
        elif operator == '/':
            result = sum // value
        elif operator == '%':
            result = sum % value
        elif operator == '=':
            result = value
        else:
            raise InterpreterSyntaxError(
                f'Unknown operator: "{operator}"'
            )
            
        result = result % (2**16)
        return result
    
    def do_string_assignment(self, parts: list[Token]) -> None:
        if len(parts) < 3:
            raise InterpreterSyntaxError(
                'String assignment must have a variable and a value.'
            )
            
        sum_variable = CommandArgument(
            parts[0], 
            self.env.variables
        ).to_string_variable()
        if parts[1].type != TokenType.SYMBOL or parts[1].value != '=':
            raise InterpreterSyntaxError(
                'Second token must be an assignment operator.'
            )
        
        sum = ''
        pending_operator = '='
        for part in parts[2:]:
            arg = CommandArgument(part, self.env.variables)
            if pending_operator != '':
                value = arg.to_string()
                sum += value
                pending_operator = ''
            else:
                pending_operator = arg.to_symbol()
                if pending_operator != '+':
                    raise InterpreterSyntaxError(
                        'Invalid operator in string assignment.'
                    )
                
        if pending_operator != '':
            raise InterpreterSyntaxError(
                'Unexpected end of line in string assignment.'
            )
            
        self.env.variables.set_string_variable(sum_variable, sum)

    def do_command(self, parts: list[Token]) -> None:
        command = CommandArgument(parts[0], self.env.variables).to_word()
        if command not in self.commands:
            raise InterpreterSyntaxError(
                f'Unknown command: "{command}"'
            )
        
        args = CommandArgumentList(parts[1:], self.env.variables)
        self.commands[command](args, self.env)
        
    def register_all_commands(self) -> None:
        for commands in all_commands:
            for name, command in commands.items():
                self.register_command(name, command)
        
        