from pygame import Surface
from enuns.playerId import PlayerId
from render.board import Board
from misc.generalUtils import GeneralUtils
from misc.selectionProperties import SelectionProperties
from misc.movimentProperties import MovimentProperties

class Field(object):

    def __init__(self, display: Surface, screen_width, screen_height, game_state, update_game_state):
        self.display = display
        self.size = 0.86 * screen_height        
        self.x_position = (screen_width - self.size) / 2
        self.y_position = (screen_height - self.size) / 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_id = PlayerId.Player1
        self.game_state = game_state
        self.selected_indexes = []
        self.raw_moviments = []
        self.moviments = []
        self.boards = []
        
        self.update_game_state = update_game_state
        
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
        
        self.raw_moviments = []
        
        for selected_index in self.selected_indexes:
            self.boards[selected_index.board_index].clean_moviments()
                    
                    
    def handle_moviment(self, selected_index: SelectionProperties, moviment_index: int):        
        index_selected = self.selected_indexes.index(selected_index)
        
        selected_item = self.moviments[moviment_index]
    
        selected_square = selected_item[index_selected]
                
        item = next((i for i, obj in enumerate(self.raw_moviments[index_selected]) if obj is not None and (obj[0] == selected_square or obj[1] == selected_square)), -1)
    
        tuple_item_index = self.raw_moviments[index_selected][item].index(selected_square)
    
        moviment_A = MovimentProperties(self.selected_indexes[0], self.raw_moviments[0][item], item, tuple_item_index)
        moviment_B = MovimentProperties(self.selected_indexes[1], self.raw_moviments[1][item], item, tuple_item_index)
                
        self.update_game_state(moviment_A, moviment_B)
        
        for selected_index in self.selected_indexes:
            board_index = selected_index.board_index 
            self.boards[board_index].update_game_state(self.game_state[(16 * board_index) : 16 * (board_index + 1)])
            
        for i in range(4):
            self.boards[i].blocked = False           
            
        self.selected_indexes = []
        self.raw_moviments = []
        self.moviments = []
    
        if self.player_id == PlayerId.Player1:
            self.player_id = PlayerId.Player2
        
        else:
            self.player_id = PlayerId.Player1
    
        return
                            
    
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
                    
                    if blocked_board_index % 2 == 0:
                        next_to_blocked_board_index = (index + 3) % 4
                    else:
                        next_to_blocked_board_index = (index + 1) % 4
                
                    print(f"\ni: {index}, b: {blocked_board_index}, n: {next_to_blocked_board_index}\n")
                    
                    if self.player_id == PlayerId.Player1:
                        if index > 1:
                            self.boards[blocked_board_index].blocked = False
                            if index == 2:
                                if (len(self.selected_indexes) == 0) or (self.selected_indexes[0].board_index != 1):
                                    self.boards[3].blocked = False
                                    print(f"o que foi desbloqueado board: {blocked_board_index}, {3}, id: {self.player_id}\n")
                            else:
                                if (len(self.selected_indexes) == 0) or (self.selected_indexes[0].board_index != 0):
                                    self.boards[2].blocked = False
                                    print(f"o que foi desbloqueado board: {blocked_board_index}, {2}, id: {self.player_id}\n")
                        else:
                            if not any(obj.board_index == next_to_blocked_board_index for obj in self.selected_indexes):
                                self.boards[blocked_board_index].blocked = False
                                print(f"o que foi desbloqueado board: {blocked_board_index}, id: {self.player_id}\n")

                    if self.player_id == PlayerId.Player2:
                        if index < 2:
                            self.boards[blocked_board_index].blocked = False
                            if index == 0:
                                if (len(self.selected_indexes) == 0) or (self.selected_indexes[0].board_index != 3):
                                    self.boards[1].blocked = False
                                    print(f"o que foi desbloqueado board: {blocked_board_index}, {1}, id: {self.player_id}\n")
                            else:
                                if (len(self.selected_indexes) == 0) or (self.selected_indexes[0].board_index != 2):
                                    self.boards[0].blocked = False
                                    print(f"o que foi desbloqueado board: {blocked_board_index}, {0}, id: {self.player_id}\n")
                        else:
                            if not any(obj.board_index == next_to_blocked_board_index for obj in self.selected_indexes):
                                self.boards[blocked_board_index].blocked = False
                                print(f"o que foi desbloqueado board: {blocked_board_index}, id: {self.player_id}\n")
                    return
                
                if len(self.selected_indexes) == 2:
                    moviment_index = self.boards[index].handle_moviment_click(mouse_position, self.player_id)
                
                    if moviment_index != None:
                        self.handle_moviment(selected_index, moviment_index)
                        return 
            
            if self.boards[index].handle_click(mouse_position, self.player_id):

                selected_square = self.boards[index].selected_square

                self.selected_indexes.append(SelectionProperties(index, selected_square))

                blocked_board_index = (index + 2) % 4
                
                self.boards[blocked_board_index].blocked = True
                
                if self.player_id == PlayerId.Player1 and index > 1:
                    if index == 2:
                        self.boards[3].blocked = True
                    
                    else:
                        self.boards[2].blocked = True
                        
                if self.player_id == PlayerId.Player2 and index < 2:
                    if index == 0:
                        self.boards[1].blocked = True
                    
                    else:
                        self.boards[0].blocked = True
                                                
                return
    
    
    def set_moviments(self, moviments, raw_moviments):
        
        self.moviments = moviments
        self.raw_moviments = raw_moviments
        
        for i in range(2):
            selected_board_index = self.selected_indexes[i].board_index                
            self.boards[selected_board_index].set_moviments([moviment[i] for moviment in moviments])