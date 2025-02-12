import pygame
from pygame.font import Font

from backend.interface.area import Position
from backend.interface.colours import PalettePair, palette_pair_to_rgb
from backend.interface.display import GraphicTextDisplay
from constants import DEFAULT_BACKGROUND_COLOUR


class TextCharacter:
    def __init__(self, display: GraphicTextDisplay, position: Position) -> None:
        self.char: str = ' '
        self.colour = DEFAULT_BACKGROUND_COLOUR
        self.rgb = palette_pair_to_rgb(self.colour)
        self.display = display
        self.position = position
        self.font: Font = display.get_font()
        self.width, self.height = self.display.get_character_width_and_height()
        self.buffer: pygame.Surface = pygame.Surface((self.width, self.height))
        self.output_surface: pygame.Surface = display.get_surface()
        self.needs_render = True
        self.needs_draw = False
        self.cursor_decoration = False
        self.cursor_height = 0
        self.render()

    def get_char(self) -> str:
        return self.char
    
    def get_colour(self) -> PalettePair:
        return self.colour
    
    def set_char(self, char: str) -> None:
        self.char = char
        self.needs_render = True
        
    def set_colour(self, colour: PalettePair) -> None:
        self.colour = colour
        self.rgb = palette_pair_to_rgb(colour)
        self.needs_render = True
        
    def set_char_and_colour(self, char: str, colour: PalettePair) -> None:
        self.char = char
        self.colour = colour
        self.rgb = palette_pair_to_rgb(colour)
        self.needs_render = True

    def show_cursor(self, height: int) -> None:
        self.cursor_decoration = True
        self.cursor_height = height
        self.needs_render = True
        
    def hide_cursor(self) -> None:
        self.cursor_decoration = False
        self.needs_render = True

    @property
    def updated(self) -> bool:
        return self.updated_in_last_frame
    
    def render(self) -> None:
        if not self.needs_render:
            return
        self.buffer.fill(self.rgb.bg.value)
        textbuf = Font.render(
            self.font,
            self.char,
            False,
            self.rgb.text.value,
            self.rgb.bg.value
        )
        self.buffer.blit(textbuf, (0, 0))

        if self.cursor_decoration:
            pygame.draw.rect(
                self.buffer,
                self.rgb.text.value,
                (
                    0, 
                    self.height - self.cursor_height,
                    self.width, 
                    self.height
                ),
            )
        self.needs_render = False
        self.needs_draw = True
    
    def draw(self) -> None:
        if self.needs_render:
            self.render()
        self.updated_in_last_frame = self.needs_draw
        if self.needs_draw:
            self.output_surface.blit(self.buffer, (
                self.position.col * self.width,
                self.position.row * self.height
            ))
            self.needs_draw = False

