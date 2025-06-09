from misc.selectionProperties import SelectionProperties
from misc.movimentProperties import MovimentProperties
from misc.iaMovimentProperties import IaMovimentProperties
from enuns.playerId import PlayerId
from misc.indexCalc import IndexCalculator

class IaMoviment:

    distances = [
        IndexCalculator.aux_positions(1),
        IndexCalculator.aux_positions(2),
        IndexCalculator.aux_positions(3)        
    ]

    def __init__(self, moviment_a: MovimentProperties, moviment_b: MovimentProperties, game_state, player_id: PlayerId):
        self.moviment_a = moviment_a
        self.moviment_b = moviment_b
        self.game_state = game_state
        self.player_id = player_id
        self.utility = 0
        
        
    @staticmethod
    def generate_ia_moviments(moviments_properties: list[IaMovimentProperties], player_id: PlayerId) -> dict[tuple, list["IaMoviment"]]:
        
        ia_moviments: dict[tuple, list[IaMoviment]] = {}
        
        for moviment_properties in moviments_properties:
            
            moviment_key = moviment_properties.selected_indexes
            
            moviment_a_index = moviment_key[0] % 16
            moviment_b_index = moviment_key[1] % 16
            moviment_a_index_table = IndexCalculator.calculate_table(moviment_key[0])
            moviment_b_index_table = IndexCalculator.calculate_table(moviment_key[1])
            
            selection_properties_a = SelectionProperties(moviment_a_index_table, moviment_a_index)
            selection_properties_b = SelectionProperties(moviment_b_index_table, moviment_b_index)
            
            for merged_moviment in moviment_properties.merged_moviments:
                
                direction_a_index = next(
                                    (
                                        i for i, obj in enumerate(moviment_properties.board_a_moviments) 
                                        if obj is not None and (obj[0] == merged_moviment[0] or obj[1] == merged_moviment[0])
                                    ), -1
                                    )
                
                direction_b_index = next(
                                    (
                                        i for i, obj in enumerate(moviment_properties.board_b_moviments) 
                                        if obj is not None and (obj[0] == merged_moviment[1] or obj[1] == merged_moviment[1])
                                    ), -1
                                    )
                
                selection_index = moviment_properties.board_a_moviments[direction_a_index].index(merged_moviment[0])
                
                moviment_a = MovimentProperties(
                        selection_properties_a, 
                        moviment_properties.board_a_moviments[direction_a_index], 
                        direction_a_index, 
                        selection_index
                    )
                
                moviment_b = MovimentProperties(
                        selection_properties_b, 
                        moviment_properties.board_b_moviments[direction_b_index], 
                        direction_b_index, 
                        selection_index
                    )

                if moviment_key in ia_moviments:
                    ia_moviments[moviment_key].append(IaMoviment(moviment_a, moviment_b, [], player_id))

                else:                    
                    ia_moviments[moviment_key] = [IaMoviment(moviment_a, moviment_b, [], player_id)]
                
        
        return ia_moviments
    
    
    def handle_utility_calculator(self) -> int:        
        self.utility = IaMoviment.utility_calculator(self.game_state, self.player_id)
        
        return self.utility
        
    
    @staticmethod                
    def utility_calculator(game_state, player_id) -> int:
        
        player_piece = 'W'
        enemy_piece = 'B'
        
        player_sum = 0
        enemy_sum = 0
        
        if player_id == PlayerId.Player2:
            player_piece = 'B'
            enemy_piece = 'W'        
        
        for n in range(0, 4):
            
            board = game_state[(n * 16) : ((n + 1) * 16)]
            
            # caso não exista peça do jogador no tabuleiro, então o jogador perdeu
            if player_piece not in board:
                utility = -10000
                return utility
            
            # caso não exista peça do inimigo no tabuleiro, então o adversário perdeu
            if enemy_piece not in board:
                utility = 10000
                return utility
            
            for piece_index in range(len(board)):
                
                piece = board[piece_index]

                if piece == '':
                    continue
                
                piece_row, piece_column = IndexCalculator.calculate_row_column(piece_index)

                for direction in range(8):
                    
                    distance_1 = piece_row + IaMoviment.distances[0][direction][0], piece_column + IaMoviment.distances[0][direction][1]
                    distance_2 = piece_row + IaMoviment.distances[1][direction][0], piece_column + IaMoviment.distances[1][direction][1]
                    distance_3 = piece_row + IaMoviment.distances[2][direction][0], piece_column + IaMoviment.distances[2][direction][1]
                
                    distance_1_index = -1
                    distance_2_index = -1
                    distance_3_index = -1
                
                    if 0 <= distance_1[0] <= 3 and 0 <= distance_1[1] <= 3:
                        distance_1_index = IndexCalculator.calculate(distance_1[0], distance_1[1])
                    
                    if 0 <= distance_2[0] <= 3 and 0 <= distance_2[1] <= 3:
                        distance_2_index = IndexCalculator.calculate(distance_2[0], distance_2[1])
                    
                    if 0 <= distance_3[0] <= 3 and 0 <= distance_3[1] <= 3:
                        distance_3_index = IndexCalculator.calculate(distance_3[0], distance_3[1])
                
                    if distance_1_index == -1:
                        continue
                    
                    if piece == board[distance_1_index]:
                        
                        if piece == player_piece:
                            player_sum += 5
                        
                        else:
                            enemy_sum += 5
                        
                        continue
                    
                    if board[distance_1_index] != '' and board[distance_1_index] != piece:
                        
                        if distance_2_index == -1:
                            if piece == player_piece:
                                player_sum += 50
                                
                            else:
                                enemy_sum += 50
                                
                            continue
                        
                        # Somado 6 porque a peça pode ser movida ou empurrada do tabuleiro;
                        # O cenario eh: _ X 0 _                                            
                        if board[distance_2_index] == '':
                            
                            if distance_3_index == -1:                                
                                if piece == player_piece:
                                    player_sum += 50
                                
                                else:
                                    enemy_sum += 50
                                    
                            # O cenario é: _ X 0 X ou _ X 0 0
                            # Para o cenário, não possui caso
                            
                            continue                            
                    
                    if board[distance_1_index] == '':
                        
                        if distance_2_index == -1:
                            continue
                        
                        if board[distance_2_index] == '':
                            continue
                        
                        if board[distance_2_index] != '' and board[distance_2_index] != piece:
                            
                            if distance_3_index == -1:
                                if board[distance_2_index] == enemy_piece:
                                    player_sum += 50
                                    
                                else:
                                    enemy_sum += 50
                                    
                                continue
                            
                            if board[distance_3_index] == '':
                                if board[distance_2_index] == enemy_piece:
                                    player_sum += 5
                                    
                                else: 
                                    enemy_sum += 5
                            
                                continue
                        
                            # Talvez aqui haja um caso para quando o terceiro espaço possui uma peça inimiga ou do jogador
                            # cenários: X _ 0 X ou X _ 0 0
                            # não é possivel mover a peça assim, nem contabilizar pontos...
            
        utility = player_sum - enemy_sum
        return utility