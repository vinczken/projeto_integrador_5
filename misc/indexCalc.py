from math import floor
class IndexCalculator:
    @staticmethod
    def calculate(row, column):
        return row * 4 + column
    
    @staticmethod
    def calculate_row_column(index):
        row = floor(index / 4)
        column = index % 4
        
        return (row, column)
        