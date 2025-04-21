from misc.indexCalc import IndexCalculator
from pygame import Surface
from render.field import Field
from misc.movimentProperties import MovimentProperties
from misc.selectionProperties import SelectionProperties
from enuns.playerId import PlayerId
from misc.iaMovimentProperties import IaMovimentProperties
from misc.iaMoviment import IaMoviment
import random
import copy

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
        
        
    def merge_moves(self, boardA_index, boardA_moves, boardB_index, boardB_moves, game_state: list = None):
        
        moviments = []
        
        if game_state == None:
            game_state = self.game_state
        
        for move_index in range(8):
            
            if not boardA_moves[move_index] or not boardB_moves[move_index]:
                continue
            
            move_A = boardA_moves[move_index]
            move_B = boardB_moves[move_index]
                        
                                    
            if move_A[0] is not None and move_B[0] is not None:

                move_A_index_0 = IndexCalculator.calculate_game_state(move_A[0], boardA_index)
                move_B_index_0 = IndexCalculator.calculate_game_state(move_B[0], boardB_index)                
                
                if not (game_state[move_A_index_0] != "" and game_state[move_A_index_0] == game_state[move_B_index_0]):    
                    moviments.append((move_A[0], move_B[0]))
 
                else:
                    continue
                
            if move_A[1] is not None and move_B[1] is not None:
                
                move_A_index_0 = IndexCalculator.calculate_game_state(move_A[0], boardA_index)
                move_B_index_0 = IndexCalculator.calculate_game_state(move_B[0], boardB_index)
                move_A_index_1 = IndexCalculator.calculate_game_state(move_A[1], boardA_index)
                move_B_index_1 = IndexCalculator.calculate_game_state(move_B[1], boardB_index)
            
                if not (game_state[move_A_index_1] != "" and game_state[move_A_index_1] == game_state[move_B_index_1]):
                    
                    if game_state[move_A_index_0] != "" and game_state[move_A_index_0] == game_state[move_B_index_1]:                
                        continue
                    
                    if game_state[move_B_index_0] != "" and game_state[move_B_index_0] == game_state[move_A_index_1]:
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
        
        return tuples
    
    
    def draw(self):
        self.field.draw()   

        # IMPLEMENTAÇÃO DA ATUALIZAÇÃO E GERAÇÃO DO MOVIMENTO PELA IA     
        
        if self.player_id == PlayerId.Player2:            
            moviment = self.generate_minimax()

            board_a = moviment.moviment_a.selection_properties.board_index
            board_b = moviment.moviment_b.selection_properties.board_index

            print("\n\n")
            print("---- Imprimindo resultado da geração: \n")
            
            print(f"P_ID: {moviment.player_id}")
            print(f"Uti: {moviment.utility}")

            self.update_game_state(moviment.moviment_a, moviment.moviment_b)
            
            self.field.boards[board_a].update_game_state(self.game_state[(16 * board_a) : 16 * (board_a + 1)])
            self.field.boards[board_b].update_game_state(self.game_state[(16 * board_b) : 16 * (board_b + 1)])
            
            self.player_id = PlayerId.Player1
            self.field.player_id = PlayerId.Player1

        return
    
    
    def handle_click(self, mouse_position):
        self.field.handle_click(mouse_position)

        if len(self.field.selected_indexes) == 2:
            self.handle_moves()

        return
    
    def update_game_state(self, moviment_properties_A: MovimentProperties, moviment_properties_B: MovimentProperties, game_state: list = None):
        
        moviments = [moviment_properties_A, moviment_properties_B]
        
        if game_state is None:
            game_state = self.game_state

        for moviment in moviments:            
                        
            selected_index = IndexCalculator.calculate_game_state(moviment.selection_properties.square_index, moviment.selection_properties.board_index)
            moviment_index = IndexCalculator.calculate_game_state(moviment.moviment_direction[moviment.selection_index], moviment.selection_properties.board_index)
                    
            if moviment.selection_index == 0:
                                    
                if game_state[moviment_index] != "":

                    if moviment.moviment_direction[1] is not None:
                        secondary_moviment_index = IndexCalculator.calculate_game_state(moviment.moviment_direction[1], moviment.selection_properties.board_index)
                    
                        game_state[secondary_moviment_index] = game_state[moviment_index]

                    else:
                        final_vector = IndexCalculator.calculate_row_column(moviment.moviment_direction[moviment.selection_index])
                        start_vector = IndexCalculator.calculate_row_column(moviment.selection_properties.square_index)
                        variation = (final_vector[0] - start_vector[0], final_vector[1] - start_vector[1])

                        secondary_vector = (final_vector[0] + variation[0], final_vector[1] + variation[1])

                        if 0 <= secondary_vector[0] <= 3 and 0 <= secondary_vector[1] <= 3:
                            secondary_moviment = IndexCalculator.calculate(secondary_vector[0], secondary_vector[1])
                            secondary_moviment_index = IndexCalculator.calculate_game_state(secondary_moviment, moviment.selection_properties.board_index)
                            
                            game_state[secondary_moviment_index] = game_state[moviment_index]

            else:
                
                row, column = IndexCalculator.calculate_row_column(moviment.selection_properties.square_index)
                
                row_sum, column_sum = self.aux_positions[moviment.direction_index]
                foward_moviment_index = IndexCalculator.calculate_game_state(moviment.moviment_direction[0], moviment.selection_properties.board_index)

                if 0 <= row + row_sum <= 3 and 0 <= column + column_sum <= 3:
                    index_in_board = IndexCalculator.calculate(row + row_sum, column + column_sum)                    
                    
                    if game_state[foward_moviment_index] != "":
                        game_state[moviment_index] = game_state[foward_moviment_index]
                        game_state[foward_moviment_index] = ""

                    if game_state[moviment_index] != "":            
                        secondary_moviment_index = IndexCalculator.calculate_game_state(index_in_board, moviment.selection_properties.board_index)            
                        game_state[secondary_moviment_index] = game_state[moviment_index]
                
                else:

                    if game_state[foward_moviment_index] != "":
                        game_state[moviment_index] = game_state[foward_moviment_index]
                        game_state[foward_moviment_index] = ""                    


                
            game_state[moviment_index] = game_state[selected_index]
            game_state[selected_index] = ""         
    
        if game_state == self.game_state:
            if self.player_id == PlayerId.Player1:
                self.player_id = PlayerId.Player2
            
            else:
                self.player_id = PlayerId.Player1                                                    

        return
    
    def find_secondary_indexes(self, indexes, selected_index, player_id: PlayerId):

        selected_table = IndexCalculator.calculate_table(selected_index)

        possible_indexes = [i for i in indexes if IndexCalculator.calculate_table(i) != selected_table]

        same_color_table = (selected_table + 2) % 4

        possible_indexes = [
                            i for i in possible_indexes 
                            if IndexCalculator.calculate_table(i) != same_color_table
                            ]

        if player_id == PlayerId.Player1 and selected_table >= 2:

            blocked_table = 2

            if selected_table == 2:
                blocked_table = 3

            possible_indexes = [
                                i for i in possible_indexes 
                                if IndexCalculator.calculate_table(i) != blocked_table
                                ]
            
        if player_id == PlayerId.Player2 and selected_table <= 1:

            blocked_table = 0

            if selected_table == 0:
                blocked_table = 1
            
            possible_indexes = [
                                i for i in possible_indexes 
                                if IndexCalculator.calculate_table(i) != blocked_table
                                ]
            
        return possible_indexes


    def generate_moviments(self, game_state: list, player_id: PlayerId) -> dict[tuple, list[IaMoviment]]:
        
        visited_indexes = []
        ia_moviments = []
        
        searched_piece = 'W'

        if player_id == PlayerId.Player2:
            searched_piece = 'B'

        indexes = [i for i, item in enumerate(game_state) if item == searched_piece]


        for i in indexes:
            first_index = i

            secondary_indexes = self.find_secondary_indexes(indexes, first_index, player_id)
            
            tmp_visited = set([i[0] for i in visited_indexes])
            
            secondary_indexes = [item for item in secondary_indexes if item not in tmp_visited]
            
            if len(secondary_indexes) == 0:
                continue
            
            first_index_board = IndexCalculator.calculate_table(first_index)

            first_index_board_state = game_state[(16 * first_index_board) : (16 * (first_index_board + 1))]

            first_index_in_board = first_index % 16

            valid_first_moviments = self.calculate_valid_moves(first_index_in_board, first_index_board_state)


            for secondary_index in secondary_indexes:
                
                second_index_board = IndexCalculator.calculate_table(secondary_index)

                second_index_board_state = game_state[(16 * second_index_board) : (16 * (second_index_board + 1))]

                second_index_in_board = secondary_index % 16

                valid_secondary_moviments = self.calculate_valid_moves(second_index_in_board, second_index_board_state)

                possible_moviments = self.merge_moves(
                        first_index_board, 
                        valid_first_moviments, 
                        second_index_board, 
                        valid_secondary_moviments,
                        game_state
                    )
                
                visited_indexes.append((first_index, secondary_index))
                ia_moviments.append(IaMovimentProperties((first_index, secondary_index), possible_moviments, valid_first_moviments, valid_secondary_moviments))
        
        generated_moviments = IaMoviment.generate_ia_moviments(ia_moviments, player_id)
        
        for item in generated_moviments:
            generated_mov_list = generated_moviments[item]

            for moviment in generated_mov_list:
                moviment.game_state = copy.deepcopy(game_state)
                
                self.update_game_state(moviment.moviment_a, moviment.moviment_b, moviment.game_state)
        
        return generated_moviments
    
    def generate_minimax(self, game_state: list = None, player_id: PlayerId = None, max_turn: bool = True, turns: int = 3, alpha = float('-inf'), beta = float('inf') ) -> IaMoviment:
        if game_state is None:
            game_state = self.game_state
        
        if player_id is None:
            player_id = self.player_id    
        
        turns = turns - 1
        
        #print(f"entrei no minimax, {turns}, {max_turn}")
        #print(f"alfa: {alpha}, beta: {beta}")
        
        moviments = self.generate_moviments(game_state, player_id)
        
        
        if turns == 0:
            #print("turn 0")
            moviment_list: list[IaMoviment] = []
            
            for moviment_tuple in moviments:
                moviment_list_tmp = moviments[moviment_tuple]
                
                for moviment in moviment_list_tmp:
                    moviment.utility_calculator()
                
                moviment_list.extend(moviment_list_tmp)
                
            moviment_list.sort(key=lambda moviment: moviment.utility, reverse=max_turn)
            
            if not moviment_list:
                return IaMoviment(utility=alpha if max_turn else beta)
            
            return moviment_list[0]
        else:
            new_player_id = PlayerId.Player1
            
            if player_id == PlayerId.Player1:
                new_player_id = PlayerId.Player2
            
            best_move = None
            
            for moviment_tuple in moviments:
                moviment_list_tmp = moviments[moviment_tuple]
                
                for moviment in moviment_list_tmp:
                    moviment.utility_calculator()
                moviment_list_tmp.sort(key=lambda m: m.utility, reverse=max_turn)
                
                for moviment in moviment_list_tmp:
                    
                    new_moviment = self.generate_minimax(moviment.game_state, new_player_id, not max_turn, turns, alpha, beta)
                    #print(f"\tsai do minimax, {turns}, {max_turn}")
                    #print(f"\tNM: {new_moviment.utility}")
                    
                    if max_turn:
                        if alpha < new_moviment.utility:
                            #print("alfa trocado")
                            alpha = new_moviment.utility
                            best_move = moviment
                    else:
                        if beta > new_moviment.utility:
                            #print("beta trocado")
                            beta = new_moviment.utility
                            best_move = moviment
                    
                    #print(f"\talfa: {alpha}, beta: {beta}")
                    
                    if alpha >= beta:
                        return best_move
                        #print("Saiu")
                        break
                    
            
            return best_move