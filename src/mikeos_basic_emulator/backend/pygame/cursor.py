from backend.interface.area import Position

class Cursor:
    def __init__(self, limits: Position) -> None:
        self.col = 0
        self.row = 0
        self.offset = 0
        self.limit = limits
        self.need_scroll = False
        
    def fix_offset(self) -> None:
        self.offset = self.row * self.limit.col + self.col

    def move(self, new_position: Position) -> None:
        self.col = new_position.col
        self.row = new_position.row
        if self.col < 0:
            self.col = 0
        elif self.col >= self.limit.col:
            self.col = self.limit.col - 1

        if self.row < 0:
            self.row = 0
        elif self.row >= self.limit.row:
            self.row = self.limit.row - 1
        self.fix_offset()
            
    def advance(self) -> None:
        self.offset += 1
        self.col += 1
        if self.col >= self.limit.col:
            self.newline()
        
    def newline(self) -> None:
        self.col = 0
        self.row += 1
        if self.row >= self.limit.row:
            self.row = self.limit.row - 1
            self.need_scroll = True
        self.fix_offset()
            
    def get_position(self) -> Position:
        return Position(self.col, self.row)
    
    def get_offset(self) -> int:
        return self.offset
            
    def wants_scroll(self) -> bool:
        return self.need_scroll
        

    def on_last_line(self) -> bool:
        return self.row == self.limit.row - 1
    
    def on_last_column(self) -> bool:
        return self.col == self.limit.col - 1

