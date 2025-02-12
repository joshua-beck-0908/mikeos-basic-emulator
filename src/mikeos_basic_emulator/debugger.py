# This is the debugger for the MikeOS Basic Emulator.
# It's responsible for logging output and debugging information.

import typing
import logging

if typing.TYPE_CHECKING:
    from environment import Environment

log = logging.getLogger(__name__)

class Debugger:
    def __init__(self) -> None:
        self.show_prints = False
        self.enabled = False
        self.last_print = ''
        self.show_types: list[str] = []

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

    def enable(self) -> None:
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
        
    def program_exit(self, env: 'Environment') -> None:
        while True:
            #log.debug('Program exit.')
            print('Program exit.')
            self.repl(env)

    def breakpoint(self, env: 'Environment') -> None:
        #log.debug('Breakpoint hit.')
        print('Breakpoint hit.')
        self.repl(env)
        
    def repl(self, env: 'Environment') -> None:
        interpreter = env.get_command_runner()
        while True:
            cmd = input('debug> ')
            if cmd == 'c':
                break
            elif cmd == 'p':
                print(f'Last PRINT: "{self.last_print}"')
            elif cmd == 'q':
                exit()
            elif cmd == 'v':
                env.variables.dump_numeric_variables()
                env.variables.dump_string_variables()
                env.variables.dump_runtime_variables()
                env.variables.dump_palette_variables()
            elif cmd.startswith('.'):
                interpreter.run_command(cmd[1:])
            else:
                print('Commands: c = continue, p = print last PRINT, q = quit')