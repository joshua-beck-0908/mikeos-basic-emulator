from typing import NamedTuple

#class Position(NamedTuple):
#    col: int
#    row: int

class Position:
    def __init__(self, col: int, row: int) -> None:
        self.col = col
        self.row = row
    
    def down(self, amount: int = 1) -> 'Position':
        return Position(self.col, self.row + amount)
    
    def up(self, amount: int = 1) -> 'Position':
        return Position(self.col, self.row - amount)
    
    def right(self, amount: int = 1) -> 'Position':
        return Position(self.col + amount, self.row)
    
    def left(self, amount: int = 1) -> 'Position':
        return Position(self.col - amount, self.row)

    
#class Area(NamedTuple):
#    start: Position
#    end: Position

class Area:
    def __init__(self, start: Position, end: Position) -> None:
        self.start = start
        self.end = end
        self.width = end.col - start.col
        self.height = end.row - start.row
        
