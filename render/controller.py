from collections import defaultdict
from misc.indexCalc import IndexCalculator
from pygame import Surface, Rect, draw, font, SRCALPHA
from render.field import Field
from misc.movimentProperties import MovimentProperties
from misc.selectionProperties import SelectionProperties
from enuns.playerId import PlayerId
from enuns.game_type import GameType
from misc.iaMovimentProperties import IaMovimentProperties
from misc.iaMoviment import IaMoviment
from misc.qLearning import QLearning
import os
import random
import copy

class Controller(object):
    
    # O init da classe recebe o display geral, sendo ele a tela principal do jogo
    def __init__(self, display: Surface, current_screen: GameType):                
        self.screen_width = display.get_width()
        self.screen_height = display.get_height()        
        self.display = display
        self.current_screen = current_screen
        self.q_learning = QLearning()
        self.player_id = PlayerId.Player1
        self.rounds = 0
        self.finished = False
        self.training = False
        self.train_with_other_models = False
        
        self.previous_game_state = []
        
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

        width, height = self.display.get_size()
        self.font = font.SysFont("Segoe UI Emoji", 26)

        self.modal_width = width * 0.4
        self.modal_height = height * 0.2

        self.modal_x = width / 2 - self.modal_width / 2
        self.modal_y = height / 2 - self.modal_height / 2

        self.modal = Rect(self.modal_x, self.modal_y, self.modal_width, self.modal_height)
        self.return_button = Rect(width * 0.05, height * 0.05, width * 0.09, height * 0.05)

        self.modal_title = Rect(self.modal_x, self.modal_y - self.modal_height * 0.05, self.modal_width, self.modal_height)
        self.modal_subtitle = Rect(self.modal_x, self.modal_y + self.modal_height * 0.15, self.modal_width, self.modal_height)

        self.overlay = Surface(display.get_size(), SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

    def reset_game(self, change_type=True):
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
        
        if change_type:
            if self.train_with_other_models:
                if self.current_screen == GameType.MinimaxVsQLearning:
                    self.current_screen = GameType.QLearningVsQLearning
                    
                else:
                    self.current_screen = GameType.MinimaxVsQLearning
        
        self.finished = False
        
        for i in range(4):
            self.field.boards[i].update_game_state(self.game_state[(16 * i) : 16 * (i + 1)])
            
        self.player_id = PlayerId.Player1      
        self.field.player_id = PlayerId.Player1

        self.rounds = 0

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
    
    def handle_qLearning_play(self):
        moviments = self.generate_moviments(self.game_state, self.player_id)
            
        best_moviment = self.q_learning.select_state(self.game_state, moviments, self.player_id)
            
        if best_moviment == None:
            return        
        
        board_a = best_moviment.moviment_a.selection_properties.board_index
        board_b = best_moviment.moviment_b.selection_properties.board_index            

        self.update_game_state(best_moviment.moviment_a, best_moviment.moviment_b, True)
            
        self.field.boards[board_a].update_game_state(self.game_state[(16 * board_a) : 16 * (board_a + 1)])
        self.field.boards[board_b].update_game_state(self.game_state[(16 * board_b) : 16 * (board_b + 1)])

        if best_moviment.utility == 10000 or best_moviment.utility == -10000:
            self.finished = True            
        return
    
    def handle_minimax_play(self):
        best_value = float('-inf') 
        best_move = -1

        moviments = self.generate_moviments(self.game_state, self.player_id)

            
        for moviment_tuple in moviments:
            moviment_list_tmp = moviments[moviment_tuple]
            for moviment in moviment_list_tmp:
                utility = self.generate_minimax(moviment, self.player_id, False, 0, float('-inf'),float('+inf'))
                if utility > best_value:
                    best_value = utility
                    best_move = moviment        

        
        if best_move.handle_utility_calculator() == 10000 or best_move.handle_utility_calculator() == -10000:
            self.finished = True                

        board_a = best_move.moviment_a.selection_properties.board_index
        board_b = best_move.moviment_b.selection_properties.board_index        

        self.update_game_state(best_move.moviment_a, best_move.moviment_b, True)
        
        self.field.boards[board_a].update_game_state(self.game_state[(16 * board_a) : 16 * (board_a + 1)])
        self.field.boards[board_b].update_game_state(self.game_state[(16 * board_b) : 16 * (board_b + 1)])

        self.rounds += 1
        return


    def draw_modal(self):

        self.display.blit(self.overlay, (0, 0))
        draw.rect(self.display, (153, 65, 16), self.modal, border_radius=10)

        winner = ""

        for i in range(4):
            if not 'W' in self.game_state[(i*16) : ((i+1)*16)]:
                winner = "Player 2 - ⚫"                

            if not 'B' in self.game_state[(i*16) : ((i+1)*16)]:
                winner = "Player 1 - ⚪"
    
        title = "Fim de jogo! 🏁"

        subtitle = f"Vitória do: {winner}"        

        draw.rect(self.display, (153, 65, 16), self.modal_title)
        draw.rect(self.display, (153, 65, 16), self.modal_subtitle)
        
        text_render_title = self.font.render(title, True, (0, 0, 0))
        text_render_subtitle = self.font.render(subtitle, True, (0, 0, 0))

        title_rect = text_render_title.get_rect(center=self.modal_title.center)
        subtitle_rect = text_render_subtitle.get_rect(center=self.modal_subtitle.center)

        self.display.blit(text_render_title, title_rect)
        self.display.blit(text_render_subtitle, subtitle_rect)

    def draw_reset(self):

        draw.rect(self.display, (153, 65, 16), self.return_button, border_radius=10)

        text = "🔄 resetar"

        text_render = self.font.render(text, True, (0, 0, 0))
        text_rect = text_render.get_rect(center=self.return_button.center)

        self.display.blit(text_render, text_rect)

    def draw(self):
        self.field.draw()           

        if self.finished == True:
            
            if self.training and GameType.MinimaxVsQLearning:
                winner = self.game_ended_winner()
                self.update_winners(winner)
            
            if self.training:
                self.reset_game()
            
            self.draw_modal()
            self.draw_reset()
            
            return

        if self.rounds % 100 == 0:
            self.q_learning.save_table();
        
        if self.rounds > 10000:
            self.rounds = 0
        
        # IMPLEMENTAÇÃO DA ATUALIZAÇÃO E GERAÇÃO DO MOVIMENTO PELA IA     

        if self.player_id == PlayerId.Player1:
            
            if self.current_screen == GameType.MinimaxVsMinimax or self.current_screen == GameType.MinimaxVsQLearning:
                self.handle_minimax_play()

            if self.current_screen == GameType.QLearningVsQLearning:
                self.handle_qLearning_play()

            return
        
        else:

            if (
                self.current_screen == GameType.MinimaxVsQLearning or 
                self.current_screen == GameType.PlayerVsQLearning or
                self.current_screen == GameType.QLearningVsQLearning
            ):
                self.handle_qLearning_play()
                
            if self.current_screen == GameType.MinimaxVsMinimax or self.current_screen == GameType.PlayerVsMinimax:
                self.handle_minimax_play()

            return
    
    def handle_click(self, mouse_position):

        if not self.finished:
            self.field.handle_click(mouse_position)

        if len(self.field.selected_indexes) == 2:
            self.handle_moves()

        if self.finished and self.return_button.collidepoint(mouse_position):            
            self.reset_game(False)

        return
    
    def update_game_state(self, moviment_properties_A: MovimentProperties, moviment_properties_B: MovimentProperties, update_player: bool = False, game_state: list = None):
        
        moviments = [moviment_properties_A, moviment_properties_B]
        
        
        if game_state is None:
            game_state = self.game_state
        
        self.previous_game_state = game_state

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
    
        if game_state == self.game_state and update_player:

            if self.player_id == PlayerId.Player1:                
                self.player_id = PlayerId.Player2
                self.field.player_id = PlayerId.Player2
            else:
                self.player_id = PlayerId.Player1      
                self.field.player_id = PlayerId.Player1                                              

        flag_finished = False

        for i in range(4):

            if not 'W' in self.game_state[(i*16) : ((i+1)*16)]:
                self.finished = True

            if not 'B' in self.game_state[(i*16) : ((i+1)*16)]:
                self.finished = True
            
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
                moviment.game_state = game_state.copy()
                moviment.updated_game_state = game_state.copy()
                if(self.previous_game_state != []):
                    moviment.previous_game_state = self.previous_game_state.copy()
                
                self.update_game_state(moviment.moviment_a, moviment.moviment_b, False, moviment.updated_game_state)
        
        return generated_moviments
    
    def generate_minimax(self, moviment: IaMoviment = None, player_id: PlayerId = None, max_turn: bool = True, turns: int = 3, alpha = float('-inf'), beta = float('+inf')) -> int:
            
        if player_id is None:
            player_id = self.player_id    
        
        moviments = self.generate_moviments(moviment.updated_game_state, player_id)
        state_of_game = self.game_ended(moviment.game_state)
        if turns == 0 or state_of_game:
            
            # LÓGICA PARA REPETIÇÕES AQUI DENTRO... IRÁ VERIFICAR O SET DO CONTROLLER
            # FUNÇÃO QUE RETORNA TRUE E FALSE E INSERE ESTADO NO SET

            return moviment.handle_utility_calculator()
        
        new_player_id = PlayerId.Player1
        
        if player_id == PlayerId.Player1:
            new_player_id = PlayerId.Player2

        if max_turn:
            for moviment_tuple in moviments:
                moviment_list_tmp = moviments[moviment_tuple]
                for moviment_in_list in moviment_list_tmp:
                    utility = self.generate_minimax(moviment_in_list, new_player_id, False, turns - 1, alpha, beta)
                    alpha = max(utility, alpha)
                if beta <= alpha:
                    continue
                return alpha
            return alpha
        else:
            for moviment_tuple in moviments:
                moviment_list_tmp = moviments[moviment_tuple]
                for moviment_in_list in moviment_list_tmp:
                    utility = self.generate_minimax(moviment_in_list, new_player_id, True, turns - 1, alpha, beta)
                    beta = min(utility, beta)
                if beta <= alpha:
                    continue
                return beta
            return beta
    
    def game_ended(self, local_game_state: list = None) -> bool:
        
        if local_game_state == None:
            local_game_state = self.game_state
        
        for i in range(0, len(local_game_state), 16):
            board = local_game_state[i:i+16]
            non_empty = [piece for piece in board if piece != ""]
            if all(piece == non_empty[0] for piece in non_empty):
                return True
        return False
    
    def game_ended_winner(self, local_game_state: list = None) -> bool:
        
        if local_game_state == None:
            local_game_state = self.game_state
        
        for i in range(0, len(local_game_state), 16):
            board = local_game_state[i:i+16]
            non_empty = [piece for piece in board if piece != ""]
            if all(piece == non_empty[0] for piece in non_empty):
                if non_empty[0] == 'W': return 'minimax'
                else: return 'qlearning'
        return None

    def update_winners(self, winner):
        
        winners = defaultdict(int)
        
        if os.path.exists('./winners.txt'):
            with open('./winners.txt', 'r') as f:
                for line in f:
                    name, qtd = line.strip().split(':')
                    winners[name] = int(qtd)
        
        winners[winner] += 1
        
        with open('./winners.txt', 'w') as f:
            for name, qtd in winners.items():
                f.write(f'{name}:{qtd}\n')