from pygame import Surface, Rect
from render.square import Square 

class Board(object):
    
    def __init__(self, display: Surface, screen_width, screen_height, field_x, field_y, board_index: int):
        self.display = display
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_index = board_index
        self.selected = False
        self.size = screen_height * 0.4
        
        margin = screen_height * 0.06
        
        if board_index % 2 == 0:
            self.background_color = (153, 65, 16)
            self.x_position = field_x
        
        else:
            self.background_color = (250, 243, 173)
            self.x_position = field_x + self.size + margin

        if board_index < 2:
            self.y_position = field_y

        else:
            self.y_position = field_y + self.size + margin
    
        self.rect = Surface((self.size, self.size))
        self.rect.fill(self.background_color)
            
        self.squares = []    
        
        for index in range(16):
            self.squares.append(Square(self.display, self.size, self.x_position, self.y_position, index, self.background_color))
        
    def draw(self):
        self.display.blit(self.rect, (self.x_position, self.y_position))
        
        for index in range(16):
            self.squares[index].draw()
        
        return    
        