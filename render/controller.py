from misc.indexCalc import IndexCalculator
from pygame import Surface
from render.field import Field
from misc.movimentProperties import MovimentProperties
from misc.selectionProperties import SelectionProperties
from enuns.playerId import PlayerId

class Controller(object):
    
    # O init da classe recebe o display geral, sendo ele a tela principal do jogo
    def __init__(self, display: Surface):                
        self.screen_width = display.get_width()
        self.screen_height = display.get_height()        
        self.display = display
        
        self.player_id = PlayerId.Player1
        
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
        
        self.field = Field(self.display, self.screen_width, self.screen_height, self.game_state, self.update_game_state)
        # row, column
        self.aux_positions = {
            0: (-3, -3),
            1: (-3, 0),
            2: (-3, 3),
            3: (0, -3),
            4: (0, 3),
            5: (3, -3),
            6: (3, 0),
            7: (3, 3),            
        }

        self.aux_positions_2 = {

        }

    def handle_moves(self):
        boardA = self.field.selected_indexes[0].board_index
        boardB = self.field.selected_indexes[1].board_index
        
        boardA_state = self.game_state[(16 * boardA) : (16 * (boardA + 1))]
        boardB_state = self.game_state[(16 * boardB) : (16 * (boardB + 1))]
            
        boardA_moves = self.calculate_valid_moves(self.field.selected_indexes[0].square_index, boardA_state)
        boardB_moves = self.calculate_valid_moves(self.field.selected_indexes[1].square_index, boardB_state)
        
        moviments = self.merge_moves(boardA, boardA_moves, boardB, boardB_moves)    
        
        self.field.set_moviments(moviments, [boardA_moves, boardB_moves])
        
        
    def merge_moves(self, boardA_index, boardA_moves, boardB_index, boardB_moves):
        
        moviments = []
        
        for move_index in range(8):
            
            if not boardA_moves[move_index] or not boardB_moves[move_index]:
                continue
            
            move_A = boardA_moves[move_index]
            move_B = boardB_moves[move_index]
                        
                                    
            if move_A[0] is not None and move_B[0] is not None:

                move_A_index_0 = IndexCalculator.calculate_game_state(move_A[0], boardA_index)
                move_B_index_0 = IndexCalculator.calculate_game_state(move_B[0], boardB_index)                
                
                if not (self.game_state[move_A_index_0] != "" and self.game_state[move_A_index_0] == self.game_state[move_B_index_0]):    
                    moviments.append((move_A[0], move_B[0]))
 
                else:
                    continue
                
            if move_A[1] is not None and move_B[1] is not None:
                
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
        iteration = 0
        
        
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
                
                iteration += 1
                         
        tuple = ()      
                      
        for i in range(len(tuples)):
            tuple = tuples[i]
            
            if tuple[0] is None:
                tuples[i] = None                
                continue 
                                            
            if board_state[tuple[0]] == player_color:
                tuples[i] = None
                continue
            
            if tuple[1] is not None and board_state[tuple[1]] == player_color:
                tuples[i] = (tuple[0], None)                  
                continue                    
                      
            if tuple[1] is not None and board_state[tuple[0]] == enemy_color and board_state[tuple[1]] == enemy_color:
                tuples[i] = None
                continue
        
            if tuple[1] is not None and (board_state[tuple[0]] == enemy_color or board_state[tuple[1]] == enemy_color):
                row, column = IndexCalculator.calculate_row_column(tuple[1])
                sum_row, sum_column = self.aux_positions[i]
                
                if not 0 <= row_square + sum_row <= 3 or not 0 <= column_square + sum_column <= 3:
                    continue 
                
                extra_position = IndexCalculator.calculate(row_square + sum_row, column_square + sum_column)
                
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
            self.handle_moves()

        return
    
    def update_game_state(self, moviment_properties_A: MovimentProperties, moviment_properties_B: MovimentProperties):
        
        moviments = [moviment_properties_A, moviment_properties_B]
        
        print(self.player_id)
        
        for moviment in moviments:            
                        
            selected_index = IndexCalculator.calculate_game_state(moviment.selection_properties.square_index, moviment.selection_properties.board_index)
            moviment_index = IndexCalculator.calculate_game_state(moviment.moviment_direction[moviment.selection_index], moviment.selection_properties.board_index)
                    
            if moviment.selection_index == 0:
                                    
                if self.game_state[moviment_index] != "":

                    if moviment.moviment_direction[1] is not None:
                        secondary_moviment_index = IndexCalculator.calculate_game_state(moviment.moviment_direction[1], moviment.selection_properties.board_index)
                    
                        self.game_state[secondary_moviment_index] = self.game_state[moviment_index]

                    else:
                        final_vector = IndexCalculator.calculate_row_column(moviment.moviment_direction[moviment.selection_index])
                        start_vector = IndexCalculator.calculate_row_column(moviment.selection_properties.square_index)
                        variation = (final_vector[0] - start_vector[0], final_vector[1] - start_vector[1])

                        secondary_vector = (final_vector[0] + variation[0], final_vector[1] + variation[1])

                        if 0 <= secondary_vector[0] <= 3 and 0 <= secondary_vector[1] <= 3:
                            secondary_moviment = IndexCalculator.calculate(secondary_vector[0], secondary_vector[1])
                            secondary_moviment_index = IndexCalculator.calculate_game_state(secondary_moviment, moviment.selection_properties.board_index)
                            
                            self.game_state[secondary_moviment_index] = self.game_state[moviment_index]

            else:
                
                row, column = IndexCalculator.calculate_row_column(moviment.selection_properties.square_index)
                
                row_sum, column_sum = self.aux_positions[moviment.direction_index]
                foward_moviment_index = IndexCalculator.calculate_game_state(moviment.moviment_direction[0], moviment.selection_properties.board_index)

                if 0 <= row + row_sum <= 3 and 0 <= column + column_sum <= 3:
                    index_in_board = IndexCalculator.calculate(row + row_sum, column + column_sum)                    
                    
                    if self.game_state[foward_moviment_index] != "":
                        self.game_state[moviment_index] = self.game_state[foward_moviment_index]
                        self.game_state[foward_moviment_index] = ""

                    if self.game_state[moviment_index] != "":            
                        secondary_moviment_index = IndexCalculator.calculate_game_state(index_in_board, moviment.selection_properties.board_index)            
                        self.game_state[secondary_moviment_index] = self.game_state[moviment_index]
                
                else:

                    if self.game_state[foward_moviment_index] != "":
                        self.game_state[moviment_index] = self.game_state[foward_moviment_index]
                        self.game_state[foward_moviment_index] = ""                    


                
            self.game_state[moviment_index] = self.game_state[selected_index]
            self.game_state[selected_index] = ""         
    
        if self.player_id == PlayerId.Player1:
            self.player_id = PlayerId.Player2
        
        else:
            self.player_id = PlayerId.Player1                                                    

        return