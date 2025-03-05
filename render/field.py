from pygame import Surface
from enuns.playerId import PlayerId
from render.board import Board
from misc.generalUtils import GeneralUtils

class Field(object):

    def __init__(self, display: Surface, screen_width, screen_height):
        self.display = display
        self.size = 0.86 * screen_height        
        self.x_position = (screen_width - self.size) / 2
        self.y_position = (screen_height - self.size) / 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_id = PlayerId.Player1
        self.selected_boards_index = []
        
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
    
    def handle_click(self, mouse_position):
        
        if not GeneralUtils.verify_click((self.x_position, self.y_position), self.size, self.size, mouse_position):
            return
          
        for index in range(4):
            
            if index in self.selected_boards_index:
                
                if self.boards[index].handle_selected_click(mouse_position):
                    self.selected_boards_index.remove(index)
                    
                    return
                
            
            if self.boards[index].handle_click(mouse_position, self.player_id):
                self.selected_boards_index.append(index)
                                
                blocked_board_index = (index + 2) % 4
                
                self.boards[blocked_board_index].blocked = True
                
                return