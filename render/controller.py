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
        return