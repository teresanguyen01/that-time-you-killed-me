import sys
from game_manager import GameManager

class Cli:
    """Reading in the type of players, history, and score display"""

    def __init__(self): 
        self.white_player = None
        self.black_player = None
        self.history = "off"
        self.score_display = "off"

        try:
            self.white_player = sys.argv[1]
            self.black_player = sys.argv[2]
            self.history = sys.argv[3]
            self.score_display = sys.argv[4]
        except IndexError:
            self.white_player = None
            self.black_player = None
            self.history = "off"
            self.score_display = "off"        
        
        # start the game manager
        self._game = GameManager(self.white_player, self.black_player, self.history, self.score_display)

if __name__ == "__main__":
    starting_game = Cli()
    starting_game._game._start_game()

