from misc.indexCalc import IndexCalculator
from pygame import Surface
from render.field import Field

class Controller(object):
    
    # O init da classe recebe o display geral, sendo ele a tela principal do jogo
    def __init__(self, display: Surface):                
        self.screen_width = display.get_width()
        self.screen_height = display.get_height()
        self.display = display
        
        self.game_state = [
            "W","W","W","W",
            "","","","",
            "","","","",
            "B","B","B","B",
            "W","W","W","W",
            "","","","",
            "","","","",
            "B","B","B","B",
            "W","W","W","W",
            "","","","",
            "","","","",
            "B","B","B","B",
            "W","W","W","W",
            "","","","",
            "","","","",
            "B","B","B","B"
        ]
        
        self.field = Field(display, self.screen_width, self.screen_height, self.game_state)
        
        # row, column
        self.aux_positions = {
            0: (-3, -3),
            1: (-3, 0),
            2: (-3, 3),
            3: (0, -3),
            4: (0, 3),
            5: (3, 3),
            6: (3, 0),
            7: (3, -3),            
        }
    

    def handle_moves(self):
        boardA = self.field.selected_indexes[0].board_index
        boardB = self.field.selected_indexes[1].board_index
        
        boardA_state = self.game_state[(16 * boardA) : (16 * (boardA + 1))]
        boardB_state = self.game_state[(16 * boardB) : (16 * (boardB + 1))]
            
        boardA_moves = self.calculate_valid_moves(self.field.selected_indexes[0].square_index, boardA_state)
        boardB_moves = self.calculate_valid_moves(self.field.selected_indexes[1].square_index, boardB_state)
        
        moviments = self.merge_moves(boardA, boardA_moves, boardB, boardB_moves)
        
        print("Possiveis movimentos:")
        print(moviments)
        
        self.field.set_moviments(moviments)
        
        
    def merge_moves(self, boardA_index, boardA_moves, boardB_index, boardB_moves):
        
        moviments = []
        
        for move_index in range(8):
            
            if not boardA_moves[move_index] or not boardB_moves[move_index]:
                continue
            
            move_A = boardA_moves[move_index]
            move_B = boardB_moves[move_index]
                        
                                    
            if move_A[0] and move_B[0]:

                move_A_index_0 = IndexCalculator.calculate_game_state(move_A[0], boardA_index)
                move_B_index_0 = IndexCalculator.calculate_game_state(move_B[0], boardB_index)                
                
                if not (self.game_state[move_A_index_0] != "" and self.game_state[move_A_index_0] == self.game_state[move_B_index_0]):    
                    moviments.append((move_A[0], move_B[0]))
 
                
            if move_A[1] and move_B[1]:
                
                move_A_index_0 = IndexCalculator.calculate_game_state(move_A[0], boardA_index)
                move_B_index_0 = IndexCalculator.calculate_game_state(move_B[0], boardB_index)
                move_A_index_1 = IndexCalculator.calculate_game_state(move_A[1], boardA_index)
                move_B_index_1 = IndexCalculator.calculate_game_state(move_B[1], boardB_index)
            
                if not (self.game_state[move_A_index_1] != "" and self.game_state[move_A_index_1] == self.game_state[move_B_index_1]):
                    
                    if self.game_state[move_A_index_0] != "" and self.game_state[move_A_index_0] == self.game_state[move_B_index_1]:                
                        continue
                    
                    if self.game_state[move_B_index_0] != "" and self.game_state[move_B_index_0] == self.game_state[move_A_index_1]:
                        continue
                    
                    moviments.append((move_A[1], move_B[1]))

        
        return moviments
    
    
    def calculate_valid_moves(self, square_index, board_state):
        row_square = int(square_index / 4)
        column_square = square_index % 4        
        player_color = board_state[square_index]
        enemy_color = next((item for item in board_state if item != player_color and item != ""), None)
                        
        tuples = []
        
        itemA = 0
        itemB = 0
        
        for row in range(-1, 2):             
             for column in range(- 1, 2):
                    
                if row == 0 and column == 0:
                    continue    
                    
                if 0 <= row_square + row <= 3 and 0 <= column_square + column <= 3:
                    itemA = IndexCalculator.calculate(row_square + row, column_square + column)
                    
                else:
                    itemA = None
                        
                if 0 <= row_square + row * 2 <= 3 and 0 <= column_square + column * 2 <= 3:
                    itemB = IndexCalculator.calculate(row_square + row * 2, column_square + column * 2)
                        
                else:
                    itemB = None
                    
                tuples.append((itemA, itemB))
                         
        tuple = ()      
                      
        for i in range(len(tuples)):
            tuple = tuples[i]
            
            if not tuple[0]:
                tuples[i] = None                
                continue 
                                            
            if board_state[tuple[0]] == player_color:
                tuples[i] = None
                continue
            
            if tuple[1] and board_state[tuple[1]] == player_color:
                tuples[i] = (tuple[0], None)                  
                continue                    
                      
            if tuple[1] and tuple[0] == enemy_color and tuple[1] == enemy_color:
                tuples[i] = None
                continue
        
            if tuple[1] and tuple[1] == enemy_color:
                row, column = IndexCalculator.calculate_row_column(tuple[1])
                sum_row, sum_column = self.aux_positions[i]
                
                if not 0 <= row + sum_row <= 3 or not 0 <= column + sum_column <= 3:
                    continue 
                
                if 0 <= row + sum_row <= 3 and 0 <= column + sum_column <= 3:
                    extra_position = IndexCalculator.calculate(row + sum_row, column + sum_column)

                    if board_state[extra_position] == enemy_color:
                        tuples[i] = (tuple[0], None)
                      
        print(tuples)
        
        return tuples
    
    
    def draw(self):
        self.field.draw()        
        return
    
    
    def handle_click(self, mouse_position):
        self.field.handle_click(mouse_position)

        if len(self.field.selected_indexes) == 2:
            print(f"Primeira seleção: Board index: {self.field.selected_indexes[0].board_index}; Square index: {self.field.selected_indexes[0].square_index}")
            print(f"Primeira seleção: Board index: {self.field.selected_indexes[1].board_index}; Square index: {self.field.selected_indexes[1].square_index}")

        if len(self.field.selected_indexes) == 2:
            self.handle_moves()

        return