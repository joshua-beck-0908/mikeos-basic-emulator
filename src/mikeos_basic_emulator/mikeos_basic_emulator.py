import logging
import time
from queue import Queue

from environment import Environment
from runcmd import CommandRunnerThread
from constants import EMULATED_MIKEOS_VERSION_STRING as OS_VERSION
from constants import EMULATED_MIKEOS_COMMAND_LIST as COMMANDS

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO)
    env = Environment()
    interpreter, cmdqueue = setup_interpreter(env)
    display_preamble(env)
    cmdqueue.put('FILES')
    cmdqueue.put('PRINT "Hello, World!"')
    cmdqueue.put('PRINT "Another line."')
    #cmdqueue.put('PRINT "Enter a name: " ;')
    #cmdqueue.put('INPUT $1')
    #cmdqueue.put('PRINT "Done."')
    #cmdqueue.put('ASKFILE $1')
    #cmdqueue.put('CLS')
    #cmdqueue.put('PRINT $1')
    #cmdqueue.put('ALERT $1')
    #cmdqueue.put('LISTBOX')
    #cmdqueue.put('CLS')
    cmdqueue.put('/EXIT')
    try:
        while not env.display.has_exited():
            env.display.handle_events()
            env.display.update()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    env.display.exit()
        

def setup_interpreter(env: Environment) -> tuple[
    CommandRunnerThread, Queue[str]]:
    env.display.open_window()
    env.display.update()
    env.filesystem.read_files()
    env.debugger.enable()
    cmdqueue: Queue[str] = Queue()
    interpreter = CommandRunnerThread(env, cmdqueue)
    interpreter.start()
    return interpreter, cmdqueue

def display_preamble(env: Environment) -> None:
    env.display.print(f'MikeOS {OS_VERSION} (BASIC Emulator)\n')
    env.display.print(f'Commands: {", ".join(COMMANDS)}\n')
    env.display.print('> PROGRAM.BAS\n')

if __name__ == '__main__':
    main()
