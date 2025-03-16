from misc.selectionProperties import SelectionProperties

class MovimentProperties:
    
    def __init__(self, selection_properties: SelectionProperties, moviment_direction: tuple, direction_index: int, selection_index: int):
        self.selection_properties = selection_properties
        self.moviment_direction = moviment_direction
        self.direction_index = direction_index
        self.selection_index = selection_index