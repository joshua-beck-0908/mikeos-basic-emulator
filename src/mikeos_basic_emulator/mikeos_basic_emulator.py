import logging
import time
from queue import Queue
import cProfile

from environment import Environment
from runcmd import CommandRunnerThread
from constants import EMULATED_MIKEOS_VERSION_STRING as OS_VERSION
from constants import EMULATED_MIKEOS_COMMAND_LIST as COMMANDS

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO)
    env = Environment()
    cmdqueue = setup_interpreter(env)
    display_preamble(env)
    load_program(cmdqueue, 'APP.BAS')
    try:
        while not (env.display.has_exited() or env.debugger.finished):
            env.display.handle_events()
            env.display.update()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    env.display.exit()

def setup_interpreter(env: Environment) -> Queue[str]:
    env.display.open_window()
    env.display.update()
    env.filesystem.read_files()
    env.debugger.enable()
    # TODO: Make this a config option.
    #env.debugger.enable_debug_on_exit()
    cmdqueue: Queue[str] = Queue()
    interpreter = CommandRunnerThread(env, cmdqueue)
    interpreter.start()
    return cmdqueue

def display_preamble(env: Environment) -> None:
    env.display.print(f'MikeOS {OS_VERSION} (BASIC Emulator)\n')
    env.display.print(f'Commands: {", ".join(COMMANDS)}\n')
    env.display.print('> PROGRAM.BAS\n')
    
def add_program(cmdqueue: Queue[str], filename: str) -> None:
    cmdqueue.put(f'INCLUDE "{filename}"')
    
def load_program(cmdqueue: Queue[str], program: str) -> None:
    add_program(cmdqueue, program)
    cmdqueue.put('GOTO PROGSTART')
    cmdqueue.put('/RUN')

if __name__ == '__main__':
    main()
    #cProfile.run('main()', sort='cumtime')
