# This is the debugger for the MikeOS Basic Emulator.
# It's responsible for logging output and debugging information.

import typing
import logging

if typing.TYPE_CHECKING:
    from environment import Environment

log = logging.getLogger(__name__)

class Debugger:
    """
    This code records useful errors and warnings to the terminal or log file.
    Different warning levels can be enabled or disabled.
    
    A message type is provided to help filter the messages.

    It's also responsible for handling the REPL (Read-Eval-Print Loop) when
    the program is paused or stopped.
    This can be used to inspect the state of the program and variables.
    This may occurs when:
    - A breakpoint is hit.
    - The `BREAK` command is used.
    - The program finishes.
    - A syntax or logic error occurs.
    - Unsupported commands like `CALL` are used.
    
    """
    def __init__(self) -> None:
        self.show_prints = False
        self.enabled = False
        self.last_print = ''
        self.show_types: list[str] = []
        self.finished = False
        self.run_debugger_on_exit = False

    def debug(self, msgtype: str, message: str) -> None:
        if self.enabled:
            log.debug(f'{msgtype}: {message}')
        if msgtype in self.show_types:
            print(f'{msgtype}: {message}')
            
    def info(self, msgtype: str, message: str) -> None:
        
        if self.enabled:
            log.info(f'{msgtype}: {message}')
        if msgtype in self.show_types:
            print(f'{msgtype}: {message}')

    def warning(self, msgtype: str, message: str) -> None:
        if self.enabled:
            log.warning(f'{msgtype}: {message}')
        if msgtype in self.show_types:
            print(f'{msgtype}: {message}')

    def error(self, msgtype: str, message: str) -> None:
        log.error(f'{msgtype}: {message}')
        print(f'{msgtype}: {message}')

    def enable_type(self, msgtype: str) -> None:
        self.show_types.append(msgtype)
        
    def disable_type(self, msgtype: str) -> None:
        self.show_types.remove(msgtype)

    def enable_debug_on_exit(self) -> None:
        """ Enters the REPL loop when the program finishes. """
        self.run_debugger_on_exit = True

    def disable_debug_on_exit(self) -> None:
        self.run_debugger_on_exit = False

    def enable(self) -> None:
        """ Enables debug printing and logging. """
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False
    
    def enable_prints(self) -> None:
        self.show_prints = True
    
    def disable_prints(self) -> None:
        self.show_prints = False

    def log_print(self, message: str) -> None:
        if self.show_prints:
            print(f'PRINT: "{message}"')
        self.debug('PRINT', message)
        self.last_print = message

    def log_set_variable(self, variable: str, value: int) -> None:
        self.debug(f'SET', f'{variable} = {value}')
        
    def log_command(self, command: str) -> None:
        self.debug(f'COMMAND', f'{command}')
        
    def log_command_register(self, command: str) -> None:
        self.debug(f'REGISTER', f'COMMAND: {command}')
        
    def on_program_exit(self, env: 'Environment') -> None:
        """
        Called when the program has finished.
        This will enter the REPL loop until the user chooses to exit.
        """
        if not self.run_debugger_on_exit:
            self.finished = True
            env.program_finished = True
            return
        
        while not self.finished:
            #log.debug('Program exit.')
            print('Program exit.')
            env.program_finished = True
            self.repl(env)

    def breakpoint(self, env: 'Environment') -> None:
        """
        Called when a breakpoint is hit.
        """
        #log.debug('Breakpoint hit.')
        print('Breakpoint hit.')
        self.repl(env)
        
    def repl(self, env: 'Environment') -> None:
        """
        Gives the user a prompt to inspect the program state.
        This can be used to debug the program after a breakpoint or error.
        
        Commands:
        - c = continue
        - p = print last PRINT
        - q = quit
        - v = view variables
        - .<command> = run a command in the interpreter
        """
        interpreter = env.get_command_runner()
        while True:
            cmd = input('debug> ')
            if cmd == 'c':
                break
            elif cmd == 'p':
                print(f'Last PRINT: "{self.last_print}"')
            elif cmd == 'q':
                self.finished = True
                break
            elif cmd == 'v':
                env.variables.dump_numeric_variables()
                env.variables.dump_string_variables()
                env.variables.dump_runtime_variables()
                env.variables.dump_palette_variables()
            elif cmd.startswith('.'):
                interpreter.run_command(cmd[1:])
            else:
                print('Commands: c = continue, p = print last PRINT, q = quit')