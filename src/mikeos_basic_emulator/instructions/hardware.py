# This file contains the hardware commands for the MikeOS BASIC emulator.

from arglist import CommandArgumentList
from environment import Environment

def cmd_port(args: CommandArgumentList, env: Environment) -> None:
    env.debugger.error('COMMAND', 'PORT command not supported.')
    env.debugger.breakpoint(env)
    

def cmd_serial(args: CommandArgumentList, env: Environment) -> None:
    keyword = args.get_word_from_list(['ON', 'SEND', 'REC'])
    if keyword == 'ON':
        baud = args.get_numeric()
        env.serial_port.setup(baud)
    elif keyword == 'SEND':
        data = args.get_numeric()
        env.serial_port.write(data)
    elif keyword == 'READ':
        data = env.serial_port.read()
        args.set_numeric_variable(data)

def cmd_sound(args: CommandArgumentList, env: Environment) -> None:
    frequency = args.get_numeric()
    # Duration is in 1/10th of a second.
    duration = args.get_numeric() / 10
    
    env.speaker.play_tone(frequency, duration)
    env.delay(duration)
    env.speaker.stop()


all_commands = {
    'PORT': cmd_port,
    'SERIAL': cmd_serial,
    'SOUND': cmd_sound,
}