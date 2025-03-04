from math import floor
from pygame import Surface, draw, SRCALPHA
from enuns.squareState import SquareState

class Square(object):
    
    def __init__(self, display: Surface, board_size, board_x, board_y, square_index, base_background_color):
        self.display = display
        self.size = board_size * 0.25
        self.square_index = square_index
        self.square_state = SquareState.Empty
        self.x_position = board_x + (self.size * (square_index % 4))
        self.y_position = board_y + (self.size * floor((square_index / 4)))  
        
        self.base = Surface((self.size, self.size))
        self.base.fill(base_background_color)
        draw.rect(self.base, (0, 0, 0), (0, 0, self.size, self.size), 5)
    
        self.stone = Surface((self.size, self.size), SRCALPHA)

        stone_color = (0, 0, 0)
        
        if square_index > 11:
            stone_color = (33, 38, 33)   
            self.square_state = SquareState.Black
        
        if square_index < 4:
            stone_color = (217, 217, 217)
            self.square_state = SquareState.White
    
        center = self.size / 2
    
        draw.circle(self.stone, stone_color, (center, center), ((self.size - self.size * 0.3) / 2))
        
        
    def draw(self):
        self.display.blit(self.base, (self.x_position, self.y_position))
        
        if self.square_state != SquareState.Empty:
            self.display.blit(self.stone, (self.x_position, self.y_position))
            
        return
