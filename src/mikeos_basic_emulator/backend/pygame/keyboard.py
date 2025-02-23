# This file handles the keyboard input for the Pygame backend.

import queue
import string
import logging
from queue import Queue

import pygame
from pygame.event import Event

from debugger import Debugger
from backend.interface.display import TextDisplay
from backend.pygame.keymap import pygame_key_to_int16, basic_special_cases

logger = logging.getLogger(__name__)

class Keyboard:
    def __init__(self, display: TextDisplay, debugger: Debugger) -> None:
        self.key_queue: Queue[int] = Queue()
        self.debugger = debugger
        self.display = display
        
    def handle_input(self, event: Event) -> None:
        if event.key not in pygame_key_to_int16:
            self.debugger.debug('KEYBOARD', f'Unknown key: {event.key}');

        if event.key not in pygame_key_to_int16:
            return
        
        keymap = pygame_key_to_int16[event.key]
        if event.mod == pygame.KMOD_CTRL:
            bioskey = keymap.ctrl
        elif event.mod == pygame.KMOD_ALT:
            bioskey = keymap.alt
        elif event.mod == pygame.KMOD_SHIFT:
            bioskey = keymap.shifted
        else:
            bioskey = keymap.regular
            
        if bioskey in basic_special_cases:
            self.key_queue.put(basic_special_cases[bioskey])
        else:
            self.key_queue.put(bioskey & 0xFF)
            
    def read_char(self, is_blocking: bool = True) -> int:
        key = 0
        while key == 0:
            try:
                key = self.key_queue.get(block=is_blocking, timeout=0.1)
                self.key_queue.task_done()
            except queue.Empty:
                key = 0
            if self.display.has_exited():
                raise SystemExit
            if not is_blocking:
                return key
        return key

        
    def read_string(self, prompt: str = '') -> str:
        if prompt != '':
            self.display.print(prompt)
        output = ''
        key = ''
        while key != 13:
            key = self.read_char()
            if key == 13:
                continue
            elif chr(key) in string.printable:
                self.display.print(chr(key))
                output += chr(key)
        self.display.newline()
        return output

    
