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
        self.utility = IaMoviment.utility_calculator(self.game_state, self.moviment_a, self.moviment_b, self.player_id)
        
        return self.utility
        
    
    @staticmethod                
    def utility_calculator(game_state, moviment_a, moviment_b, player_id) -> int:
        
        player_piece = 'W'
        enemy_piece = 'B'
        
        player_sum = 0
        enemy_sum = 0
        
        if player_id == PlayerId.Player2:
            player_piece = 'B'
            enemy_piece = 'W'        
        
        utility = 0
        
        # BORDA CIMA, BORDA 2 LINHA, BORDA 3 LINHA, BORDA BAIXO
        board_limits = [[0,1,2,3], [4,7], [8,11], [12,13,14,15]]

        moviments = [moviment_a, moviment_b]

        for i in range(0, len(game_state), 16):
            board = game_state[i:i+16]

            if player_piece not in board:
                utility = -10000
                return utility
            
            if enemy_piece not in board:
                utility = 10000
                return utility

        for moviment in moviments:

            selected_index = IndexCalculator.calculate_game_state(moviment.selection_properties.square_index, moviment.selection_properties.board_index)
            moviment_index = IndexCalculator.calculate_game_state(moviment.moviment_direction[moviment.selection_index], moviment.selection_properties.board_index)
            
            #  INCENTIVA A UTILIZAR A SUAS PROPRIAS BOARDS PARA MAIS VANTAGEM DE MOVIMENTO
            if selected_index < 32 and player_id == PlayerId.Player1:
                player_sum += 10
            elif selected_index > 31 and player_id == PlayerId.Player2:
                player_sum += 10
            else:
                enemy_sum += 10
            
            # ESTA INDO PARA A BORDA DE UM TABULEIRO
            if any((moviment_index % 16) in sub for sub in board_limits):
                if game_state[moviment_index] != '':
                    player_sum += 50
                else:
                    enemy_sum += 60
            
            # INCENTIVA MOVER INIMIGOS
            if game_state[moviment_index] != '':
                player_sum += 50
            else:
                enemy_sum += 60

        utility += player_sum - enemy_sum
        return utility