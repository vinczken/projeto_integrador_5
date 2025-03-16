from pygame import Surface
from enuns.playerId import PlayerId
from render.board import Board
from misc.generalUtils import GeneralUtils
from misc.selectionProperties import SelectionProperties

class Field(object):

    def __init__(self, display: Surface, screen_width, screen_height, game_state):
        self.display = display
        self.size = 0.86 * screen_height        
        self.x_position = (screen_width - self.size) / 2
        self.y_position = (screen_height - self.size) / 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_id = PlayerId.Player1
        self.game_state = game_state
        self.selected_indexes = []
        self.moviments = []
        self.boards = []
        
        for index in range(4):
            self.boards.append(
                  Board(
                      self.display, 
                      self.screen_width,
                      self.screen_height,
                      self.x_position, 
                      self.y_position, 
                      index, 
                      game_state[(index * 16): ((index + 1) * 16)]
                    )
                )
            
    
    def draw(self):    
        
        for index in range(4):
            self.boards[index].draw()
        
        return
    
    def clean_moviments(self):
        for selected_index in self.selected_indexes:
            self.boards[selected_index.board_index].clean_moviments()
                    
    
    def handle_click(self, mouse_position):
        
        if not GeneralUtils.verify_click((self.x_position, self.y_position), self.size, self.size, mouse_position):
            return
            
        for index in range(4):
            
            if (selected_index := next((obj for obj in self.selected_indexes if obj.board_index == index), None)):
                
                if self.boards[index].handle_selected_click(mouse_position):
                    self.clean_moviments()
                    
                    self.selected_indexes.remove(selected_index)

                    self.selected_indexes = [obj for obj in self.selected_indexes if obj.board_index != index]

                    blocked_board_index = (index + 2) % 4
                
                    self.boards[blocked_board_index].blocked = False
                    
                    return
                
            
            if self.boards[index].handle_click(mouse_position, self.player_id):

                selected_square = self.boards[index].selected_square

                self.selected_indexes.append(SelectionProperties(index, selected_square))
                                
                blocked_board_index = (index + 2) % 4
                
                self.boards[blocked_board_index].blocked = True
                            
                return
    
    def set_moviments(self, moviments):
        
        self.moviments = moviments
        
        for i in range(2):
            selected_board_index = self.selected_indexes[i].board_index                
            self.boards[selected_board_index].set_moviments([moviment[i] for moviment in moviments])