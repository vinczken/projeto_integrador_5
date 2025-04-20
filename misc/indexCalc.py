from math import floor
class IndexCalculator:
    
    @staticmethod
    def aux_positions(distance):
        return {
            0: (-1 * distance, -1 * distance),
            1: (-1 * distance, 0),
            2: (-1 * distance, 1 * distance),
            3: (0, -1 * distance),
            4: (0, 1 * distance),
            5: (1 * distance, -1 * distance),
            6: (1 * distance, 0),
            7: (1 * distance, 1 * distance),          
        }
    
    @staticmethod
    def calculate(row, column):
        return row * 4 + column
    
    @staticmethod
    def calculate_row_column(index):
        row = floor(index / 4)
        column = index % 4
        
        return (row, column)
        
    @staticmethod     
    def calculate_game_state(index, board_index):
        return (board_index * 16) + index
    
    @staticmethod
    def calculate_table(index):
        return floor(index / 16)