from enum import Enum

# Jogador 1 -> controla pedras brancas
# Jogador 2 -> controla pedras pretas
class GameState(Enum):
    Player1 = 1,
    Player2 = 2,
    NotOver = 3