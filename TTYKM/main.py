import os
import sys
from board_manager import BoardManager

class Cli:
    """Display a board, choices, etc."""

    def __init__(self): 
        self.white_player = None
        self.black_player = None
        self.history = History("off")
        self.score_display = "off"

        try:
            if sys.argv[1] == "human":
                self.white_player = Human(1, "past")
            elif sys.argv[1] == "heuristic":
                self.white_player = Heuristic(1, "past")
            elif sys.argv[1] == "random":
                self.white_player = Random(1, "past")
            else:
                self.white_player = Human(1, "past")
            if sys.argv[2] == "human":
                self.black_player = Human(2, "future")
            elif sys.argv[2] == "heuristic":
                self.black_player = Heuristic(2, "future")
            elif sys.argv[2] == "random":
                self.black_player = Random(2, "future")
            else:
                self.black_player = Human(2, "future")
            if sys.argv[3] == "on":
                self.history = History("on")
            elif sys.argv[3] == "off":
                self.history = History("off")
            else:
                print("Invalid history setting. Defaulting to 'off'.")
                self.history = History("off")
            if sys.argv[4] == "on":
                self.score_display = "on"
            elif sys.argv[4] == "off":
                self.score_display = "off"
            else:
                print("Invalid score display setting. Defaulting to 'off'.")
                self.score_display = "off"
        except IndexError:
            if self.white_player is None:
                self.white_player = Human()
            if self.black_player is None:
                self.black_player = Human()
        
        self.boards = BoardManager()

    
    def run(self):
        """Runs when "CLI" is started"""        
        while True: 
            print("---------------------------------")
            print(f"Currently selected account: {self._bank.selected_print()}")
            self.display_board()

    
    def display_board(self): 
        
        self.boards.print_boards
        

if __name__ == "__main__":
    Cli().run()
