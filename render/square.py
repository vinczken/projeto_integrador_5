from math import floor
from pygame import Surface, draw, SRCALPHA
from enuns.squareState import SquareState
from enuns.playerId import PlayerId
from misc.generalUtils import GeneralUtils

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
        self.base_background_color = base_background_color
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


    # Verifica se houve um click em uma casa ja selecionada
    def handle_selected_click(self, mouse_position):
        
        if self.square_state not in (SquareState.Selected_Black, SquareState.Selected_White):
            return False

        if not GeneralUtils.verify_click((self.x_position, self.y_position), self.size, self.size, mouse_position):
            return False
            
        if self.square_state == SquareState.Selected_Black:
            self.square_state = SquareState.Black
                        
        if self.square_state == SquareState.Selected_White:
            self.square_state = SquareState.White
        
        print(f"Uma peça deixou de ser selecionada -> index {self.square_index}")
        self.base.fill(self.base_background_color)
        draw.rect(self.base, (0, 0, 0), (0, 0, self.size, self.size), 5)
        
        return True


    def handle_click(self, mouse_position, player_id: PlayerId):

        if not GeneralUtils.verify_click((self.x_position, self.y_position), self.size, self.size, mouse_position):
            return False
        
        if self.square_state == SquareState.Empty:
            return False
        
        assignment_flag = False
        
        if self.square_state == SquareState.Black and player_id == PlayerId.Player2:
            self.square_state = SquareState.Selected_Black
            assignment_flag = True                       
                        
        if self.square_state == SquareState.White and player_id == PlayerId.Player1:
            self.square_state = SquareState.Selected_White
            assignment_flag = True


        if assignment_flag:
            print(f"Uma peça foi selecionada: -> index: {self.square_index}")
            self.base.fill((178, 216, 220))
            draw.rect(self.base, (0, 0, 0), (0, 0, self.size, self.size), 5)

        return assignment_flag