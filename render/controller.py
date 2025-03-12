from misc.indexCalc import IndexCalculator
from pygame import Surface
from render.field import Field

class Controller(object):
    
    # O init da classe recebe o display geral, sendo ele a tela principal do jogo
    def __init__(self, display: Surface):                
        self.screen_width = display.get_width()
        self.screen_height = display.get_height()
        self.display = display
        self.field = Field(display, self.screen_width, self.screen_height)
        
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
        
    def draw(self):
        self.field.draw()        
        return
    
    def handle_click(self, mouse_position):
        self.field.handle_click(mouse_position)

        if len(self.field.selected_indexes) == 2:
            print(f"Primeira seleção: Board index: {self.field.selected_indexes[0].board_index}; Square index: {self.field.selected_indexes[0].square_index}")
            print(f"Primeira seleção: Board index: {self.field.selected_indexes[1].board_index}; Square index: {self.field.selected_indexes[1].square_index}")

        if len(self.field.selected_indexes) == 2:
            boardA = self.field.selected_indexes[0].board_index
            boardB = self.field.selected_indexes[1].board_index

            boardA_state = self.game_state[(16 * boardA) : (16 * (boardA + 1))]
            boardB_state = self.game_state[(16 * boardB) : (16 * (boardB + 1))]
            
            self.calculate_valid_moves(self.field.selected_indexes[0].square_index, boardA_state)
            self.calculate_valid_moves(self.field.selected_indexes[1].square_index, boardB_state)

        return
    
    def calculate_valid_moves(self, square_index, board_state):
        row_square = int(square_index / 4)
        column_square = square_index % 4
        moves_index = []
        for row in range(4):
            if abs(row - row_square) == 2:
                moves_index.append(IndexCalculator.calculate(row, column_square))
                if column_square - 2 >= 0:
                    moves_index.append(IndexCalculator.calculate(row, column_square - 2))
                if column_square + 2 < 4:
                    moves_index.append(IndexCalculator.calculate(row, column_square + 2))
                    
            elif abs(row - row_square) == 1:
                moves_index.append(IndexCalculator.calculate(row, column_square))
                if column_square - 1 >= 0:
                    moves_index.append(IndexCalculator.calculate(row, column_square - 1))
                if column_square + 1 < 4:
                    moves_index.append(IndexCalculator.calculate(row, column_square + 1))
                    
            elif row == row_square:
                if column_square - 2 >= 0:
                    moves_index.append(IndexCalculator.calculate(row, column_square - 2))
                if column_square - 1 >= 0:
                    moves_index.append(IndexCalculator.calculate(row, column_square - 1))
                if column_square + 1 < 4:
                    moves_index.append(IndexCalculator.calculate(row, column_square + 1))
                if column_square + 2 < 4:
                    moves_index.append(IndexCalculator.calculate(row, column_square + 2))

        print(moves_index)