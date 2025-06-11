from pygame import Surface, Rect, draw, font
from enuns.game_type import GameType

class Menu(object):

    def __init__(self, display: Surface, current_screen: GameType):
        self.screen_width = display.get_width()
        self.screen_height = display.get_height()        
        self.display = display
        self.current_screen = current_screen
        
        self.button_background_color = (153, 65, 16)
        
        self.buttons_width = self.screen_width * 0.3
        self.buttons_height = self.screen_height * 0.15
        
        self.center_margin_horizontal = self.screen_width * 0.10
        self.center_margin_vertical = self.screen_height * 0.05
        
        self.first_column_x = (self.screen_width / 2) - self.center_margin_horizontal - self.buttons_width
        self.second_column_x = (self.screen_width / 2) + self.center_margin_horizontal
        
        self.start_button_y = (self.screen_height / 2) - self.buttons_height

        self.buttons = []
        self.font = font.SysFont("Segoe UI Emoji", 32)

        self.texts = [
            '👤 Player vs Player 👤',
            '👤 Player vs Minimax 🤖',
            '👤 Player vs QLearning 🦾',
            '🤖 Minimax vs QLearning 🦾',
            '🤖 Minimax vs Minimax 🤖',
            '🦾 QLearning vs QLearning 🦾'
        ]

        training_button_y = 0
        
        for i in range(6):

            position_x = self.first_column_x
            position_y = self.start_button_y

            if i > 2:
                position_x = self.second_column_x

            iterator = i % 3
            position_y += self.center_margin_vertical * iterator
            position_y += self.buttons_height * iterator

            temp_rect = Rect(position_x, position_y, self.buttons_width, self.buttons_height)

            self.buttons.append(temp_rect)
            
            if i == 5:
                training_button_y = position_y + self.buttons_height + 10
            
        
        self.training_button = Rect(
                (self.screen_width / 2) - (self.buttons_width * 0.25), 
                training_button_y, 
                self.buttons_width * 0.5, 
                self.buttons_height * 0.5
            )

    def draw_button(self, index):

        rect = self.buttons[index]
        text = self.texts[index]

        draw.rect(self.display, self.button_background_color, rect, border_radius=10)
        
        text_render = self.font.render(text, True, (0, 0, 0))
        
        text_rect = text_render.get_rect(center=rect.center)

        self.display.blit(text_render, text_rect)        


    def draw(self):
        for i in range(6):
            self.draw_button(i)
            
        draw.rect(self.display, self.button_background_color, self.training_button, border_radius=10)

        text_training = self.font.render("Treinamento", True, (0, 0, 0))
        
        training_rect = text_training.get_rect(center=self.training_button.center)
        
        self.display.blit(text_training, training_rect)


    def handle_click(self, position) -> GameType | None:
        for i in range(6):            
            if self.buttons[i].collidepoint(position):
                match i:
                    case 0:
                        return GameType.PlayerVsPlayer
                    case 1:
                        return GameType.PlayerVsMinimax                    
                    case 2:
                        return GameType.PlayerVsQLearning
                    case 3:
                        return GameType.MinimaxVsQLearning            
                    case 4:
                        return GameType.MinimaxVsMinimax
                    case 5:
                        return GameType.QLearningVsQLearning
        
        return None

    def handle_click_training(self, position) -> bool:
        
        if self.training_button.collidepoint(position):
            return True
    
        return False

