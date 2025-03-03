from pygame import Surface
from enuns.playerId import PlayerId
from render.board import Board

class Field(object):

    def __init__(self, display: Surface, screen_width, screen_height):
        self.display = display
        self.size = 0.86 * screen_height        
        self.x_position = (screen_width - self.size) / 2
        self.y_position = (screen_height - self.size) / 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_id = PlayerId.Player1
        
        self.boards = [
            Board(self.display, self.screen_width, self.screen_height, self.x_position, self.y_position, 0),
            Board(self.display, self.screen_width, self.screen_height, self.x_position, self.y_position, 1),
            Board(self.display, self.screen_width, self.screen_height, self.x_position, self.y_position, 2),
            Board(self.display, self.screen_width, self.screen_height, self.x_position, self.y_position, 3)            
        ]    
    
    
    def draw(self):
        for index in range(4):
            self.boards[index].draw()
        
        return
    