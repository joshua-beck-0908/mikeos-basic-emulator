# The file contains the sound output code for the MikeOS BASIC emulator.

from typing import NewType
import numpy as np
from numpy.typing import NDArray

# sounddevice depends on PortAudio.
# This should be automatically install with the pip package on Windows and OS X.
# Unfortunately, on Linux, you may need to install it manually.
# On Debian/Ubuntu, you can install it with:
# sudo apt install portaudio19-dev
# On other distros I have no idea, please don't ask me.
import sounddevice as audio

AudioBuffer = NewType('AudioBuffer', NDArray[np.int16])



class Speaker:
    def __init__(self) -> None:
        self.buffer: None|AudioBuffer = None
        self.sample_rate = 44100
        self.channels = 1
        self.sample_width = 2
        self.max_amplitude = 2**((self.sample_width * 8) - 1) - 1
        
    def play_tone(self, frequency: int, duration: float) -> None:
        wav = self.create_wave(frequency, duration)
        audio.play(wav, self.sample_rate)

        
    def stop(self) -> None:
        audio.stop()

        
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

