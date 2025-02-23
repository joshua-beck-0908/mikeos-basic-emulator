# The file contains the sound output code for the MikeOS BASIC emulator.

from typing import NewType
import numpy as np
from numpy.typing import NDArray
# TODO: Stop using simpleaudio, it's unmaintained and causes a segfault.
# Is there any cross-platform alternative?
import simpleaudio as audio

AudioBuffer = NewType('AudioBuffer', NDArray[np.int16])
AudioTracker = audio.PlayObject



class Speaker:
    def __init__(self) -> None:
        self.buffer: None|AudioBuffer = None
        self.sound_tracker: None|AudioTracker = None
        self.sample_rate = 44100
        self.channels = 1
        self.sample_width = 2
        self.max_amplitude = 2**((self.sample_width * 8) - 1) - 1
        
    def play_tone(self, frequency: int, duration: float) -> None:
        wav = self.create_wave(frequency, duration)
        self.sound_tracker = self.play_wave(wav)

        
    def play_wave(self, buffer: AudioBuffer) -> AudioTracker:
        # Start playing the buffer with simpleaudio.
        # Note this function will return immediately.
        tracker = audio.play_buffer(
            buffer, 
            self.channels,
            self.sample_width,
            self.sample_rate,
        )
        return tracker
        
    def is_sound_finished(self) -> bool:
        if self.sound_tracker is None:
            return True
        else:
            return self.sound_tracker.is_playing()
        
    def stop(self) -> None:
        if self.sound_tracker is not None:
            self.sound_tracker.stop()

        
    def create_wave(self, frequency: int, duration: float) -> AudioBuffer:
        # Generate a series of steps in time.
        time_intervals = np.linspace(
            0,        # Start
            duration, # Stop
            int(self.sample_rate * duration), # Interval
            False     # Include stop point
        )
        
        # Generate a sine wave
        wave = np.sin(2 * np.pi * frequency * time_intervals)
        
        # Clip it to a 16-bit sined value. 
        wave *= self.max_amplitude / np.max(np.abs(wave))
        wave = wave.astype(np.int16)
        
        return wave

