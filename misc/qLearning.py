from collections import defaultdict
from misc.iaMoviment import IaMoviment
import pickle
import os

class QLearning(object):
    
    def __init__(self):
                
        self.q_table = defaultdict(dict)
        
        self.load_table()        
        
        self.exploratory = True
        self.ALPHA = 0.1
        self.GAMMA = 0.8
    
    
    def select_state(self, current_game_state, generated_moviments: dict[tuple, list[IaMoviment]], player_id):
        
        best_utility = float("-inf")
        best_moviment = None        
        
        for selected_indexes in generated_moviments.keys():
            
            copy_game_state = current_game_state.copy()

            for index in selected_indexes:
                
                if copy_game_state[index] == 'W':
                    copy_game_state[index] = 'w'

                if copy_game_state[index] == 'B':
                    copy_game_state[index] = 'b'

            for i in range(len(copy_game_state)):
                if copy_game_state[i] == '':
                    copy_game_state[i] = '_'
                    
            copy_game_state = ''.join(copy_game_state)

            q_state = self.q_table.get(copy_game_state, None)

            for moviment in generated_moviments[selected_indexes]:
                
                direction_index = moviment.moviment_a.direction_index
                selection_index = moviment.moviment_a.selection_index
                utility = 0
                    
                if q_state == None:
                
                    utility = moviment.handle_utility_calculator()
                    self.q_table[copy_game_state][(direction_index, selection_index)] = utility 
                    if self.exploratory:
                        best_utility = 999999
                        best_moviment = moviment
                else:
                    
                    utility = moviment.handle_utility_calculator()
                    
                    q_action = q_state.get((direction_index, selection_index), None)
                    
                    if q_action is None:                        
                        self.q_table[copy_game_state][(direction_index, selection_index)] = utility 
                        if self.exploratory:
                            best_utility = 999999
                            best_moviment = moviment
                    
                    else:                        
                        max_value = max(q_state.values())
                        
                        q_action_new_value = q_action + self.ALPHA * (moviment.handle_utility_calculator() + self.GAMMA * max_value - q_action)
                        
                        self.q_table[copy_game_state][(direction_index, selection_index)] = q_action_new_value   
                        
                if (best_utility < utility):
                    best_utility = utility
                    best_moviment = moviment
                    
        return best_moviment
    
    
    def load_table(self):
        if os.path.exists("q_table.pkl") and os.path.getsize("q_table.pkl") > 0:    
            with open("q_table.pkl", 'rb') as file:
                q_table_loaded = pickle.load(file)
                self.q_table = defaultdict(dict, q_table_loaded)
        
    def save_table(self):
        with open("./q_table.pkl", "wb") as file:
            pickle.dump(dict(self.q_table), file)    