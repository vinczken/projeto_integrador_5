class IaMovimentProperties:
    
    # selected_indexes -> Tupla com movimentos A e B de dois tabuleiros diferentes
    # merged_moviments -> Lista de tuplas com os movimentos mesclados possiveis dos dois tabuleiros
    # board_a_moviments -> Lista de movimentos para cada direcao do primeiro tabuleiro
    # board_b_moviments -> Lista de movimentos para cada direcao do segundo tabuleiro
        
    def __init__(self, selected_indexes: tuple, merged_moviments, board_a_moviments, board_b_moviments):
        self.selected_indexes = selected_indexes
        self.merged_moviments = merged_moviments
        self.board_a_moviments = board_a_moviments
        self.board_b_moviments = board_b_moviments    