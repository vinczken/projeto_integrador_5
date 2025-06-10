from enum import Enum

class GameType(Enum):
    PlayerVsPlayer = 1,
    PlayerVsMinimax = 2,
    PlayerVsQLearning = 3,
    MinimaxVsQLearning = 4,
    MinimaxVsMinimax = 5,
    QLearningVsQLearning = 6,
    MainMenu = 7