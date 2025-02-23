import tomllib
from backend.interface.colours import PalettePair, text_to_palette_pair
from typing import List

# Load the emulator constants from the TOML file
CONFIG_PATH: str = "config.toml"
with open(CONFIG_PATH, 'rb') as f:
    config = tomllib.load(f)

# Memory settings
DEFAULT_LOAD_POINT: int = \
    config["memory"]["load_point"]
"""
The location within the simulated memory to load programs.
This is set based on the default MikeOS memory layout.
Make sure it doesn't overlap with other memory areas!
"""

DEFAULT_NUMERIC_VARIABLES_LOCATION: int = \
    config["memory"]["numeric_variables_location"]
"""
The location within the simulated memory to store numeric variables.
52 bytes are reserved for single-letter variables (A-Z).
Each is stored as a 16-bit unsigned integer.
"""

DEFAULT_STRING_VARIABLES_LOCATION: int = \
    config["memory"]["string_variables_location"]
"""
The location within the simulated memory to store string variables.
1024 bytes are reserved for string variables ($1-$8).
"""

# Emulation settings
EMULATED_MIKEOS_VERSION: int = \
    config["emulation"]["mikeos_version"]
"""
The MikeOS API version that is emulated.
Programs can call `x = VERSION` to retrieve this value.
"""
EMULATED_MIKEOS_VERSION_STRING: str = \
    config["emulation"]["mikeos_version_string"]
"""
The MikeOS version string that is emulated.
This will be printed to the console when the program starts.
"""
EMULATED_MIKEOS_COMMAND_LIST: List[str] = \
    config["emulation"]["commands"]
"""
These aren't implemented in the emulator, but are available in MikeOS.
They're just shown in the help text before the program starts.
"""

# Display settings
DEFAULT_COLUMNS: int = \
    config["display"]["columns"]
"""
The number of columns in the text display.
Matches the normal BIOS mode 3 by default.
"""

DEFAULT_LINES: int = \
    config["display"]["lines"]
"""
The number of rows in the text display.
Matches the normal BIOS mode 3 by default.
"""

DEFAULT_CHARACTER_WIDTH: int = \
    config["display"]["character_width"]
"""
The pixel width of each character in the text display.
Only changes for graphical backends.
"""

DEFAULT_CHARACTER_HEIGHT: int = \
    config["display"]["character_height"]
"""
The pixel height of each character in the text display.
Only changes for graphical backends.
"""

DEFAULT_STRING_LENGTH: int = \
    config["display"]["string_length"]
"""
The maximum length of a string variable in the emulator.
Matches the normal MikeOS limit by default.
"""

DEFAULT_BACKGROUND_COLOUR: PalettePair = \
    text_to_palette_pair(config["display"]["background_colour"])
"""
The background colour of text cells by default.
The screen is cleared to this colour when the emulator starts.
"""

DEFAULT_PRINT_COLOUR: PalettePair = \
    text_to_palette_pair(config["display"]["print_colour"])
"""
The default colour for printing text to the screen if not changed.
"""

# Cursor settings
DEFAULT_CURSOR_BLINK_INTERVAL: float = \
    config["cursor"]["blink_interval"]
"""
The blinking rate of the text cursor.
Time in seconds between cursor on and off.
"""

DEFAULT_CURSOR_VISIBILITY: bool = \
    config["cursor"]["visibility"]
"""
If the cursor should be visible by default.
A program can change this with the `CURSOR` command.
"""

DEFAULT_CURSOR_BLINK: bool = \
    config["cursor"]["blink"]
"""
If the text cursor should blink by default.
If False, it will be always on or always off.
Matches normal MikeOS behavior.
"""

DEFAULT_CURSOR_HEIGHT: int = \
    config["cursor"]["height"]
"""
The height of the text mode cursor.
It is drawn as a block from the bottom.
"""

DEFAULT_DIALOG_OUTER_COLOUR: PalettePair = \
    text_to_palette_pair(config["dialog"]["outer_colour"])
"""
The outside colour of OS dialog boxes by default (e.g. LISTBOX).
May be changed by programs to customise appearance.
"""

DEFAULT_DIALOG_INNER_COLOUR: PalettePair = \
    text_to_palette_pair(config["dialog"]["inner_colour"])
"""
The inner colour used for buttons and text in OS dialog boxes.
May be changed by programs to customise appearance.
"""

DEFAULT_DIALOG_SELECTOR_COLOUR: PalettePair = \
    text_to_palette_pair(config["dialog"]["selector_colour"])
"""
The colour used for the selected item in OS dialog boxes by default.
May be changed by programs to customise appearance.
"""

# List dialog settings
DEFAULT_LIST_DIALOG_WIDTH: int = \
    config["list_dialog"]["width"]
"""
The default width of a list dialog box.
Matches normal MikeOS size by default.
"""

DEFAULT_LIST_DIALOG_HEIGHT: int = \
    config["list_dialog"]["height"]
"""
The default height of a list dialog box.
Matches normal MikeOS size by default.
"""

DEFAULT_LIST_DIALOG_X: int = \
    config["list_dialog"]["x"]
"""
The default x position (column) of a list dialog box.
Matches normal MikeOS position by default.
"""

DEFAULT_LIST_DIALOG_Y: int = \
    config["list_dialog"]["y"]
"""
The default y position (row) of a list dialog box.
Matches normal MikeOS position by default.
"""

# Message dialog settings
DEFAULT_MESSAGE_DIALOG_WIDTH: int = \
    config["message_dialog"]["width"]
"""
The default width of a message dialog box.
Matches normal MikeOS size by default.
"""

DEFAULT_MESSAGE_DIALOG_HEIGHT: int = \
    config["message_dialog"]["height"]
"""
The default height of a message dialog box.
Matches normal MikeOS size by default.
"""

DEFAULT_MESSAGE_DIALOG_X: int = \
    config["message_dialog"]["x"]
"""
The default x position (column) of a message dialog box.
Matches normal MikeOS position by default.
"""

DEFAULT_MESSAGE_DIALOG_Y: int = \
    config["message_dialog"]["y"]
"""
The default y position (row) of a message dialog box.
Matches normal MikeOS position by default.
"""

# Window settings
DEFAULT_WINDOW_TITLE: str = \
    config["window"]["title"]
"""
The title of the window to use for graphical backends.
"""
