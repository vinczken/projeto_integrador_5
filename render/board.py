from pygame import Surface, Rect
from render.square import Square 
from misc.generalUtils import GeneralUtils
from enuns.squareState import SquareState
from enuns.playerId import PlayerId

class Board(object):
    
    def __init__(self, display: Surface, screen_width, screen_height, field_x, field_y, board_index: int):
        self.display = display
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_index = board_index
        self.selected = False
        self.blocked = False
        self.size = screen_height * 0.4
        self.selected_square = -1
        
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


    # Verifica se uma peça selecionada foi clicada
    def handle_selected_click(self, mouse_position):
        
        if self.selected and self.selected_square > -1:
            if self.squares[self.selected_square].handle_selected_click(mouse_position):                
                self.selected_square = -1
                self.selected = False

                return True

        return False


    def handle_click(self, mouse_position, player_id: PlayerId):
        
        if self.blocked:
            return False
        
        if not GeneralUtils.verify_click((self.x_position, self.y_position), self.size, self.size, mouse_position):
            return False
                    
        for index in range(16):
            
            if self.squares[index].handle_click(mouse_position, player_id):
                self.selected_square = index
                self.selected = True

                return True       

        return False          