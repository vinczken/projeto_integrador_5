class GeneralUtils:
    
    @staticmethod
    def verify_click(item_position, item_width, item_height, mouse_position):
        
        item_x, item_y = item_position
        mouse_x, mouse_y = mouse_position
        
        if item_x <= mouse_x <= item_x + item_width and item_y <= mouse_y <= item_y + item_height:
            return True 
        
        return False
        