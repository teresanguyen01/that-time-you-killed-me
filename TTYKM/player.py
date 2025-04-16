from board import Board

class Player: 
    # white = 1 | black = 2
    def __init__(self, p_num, era): 
        self.p_num = p_num
        self._current_era = era
        self._num_on_board = 3

    def update_current_era(self, era): 
        self._current_era = era

    def print_era(self): 
        if self.p_num == 1: 
            if self._current_era == "past": 
                print("  white  ")
            elif self._current_era == "present": 
                print("+-+-+-+-+   +-")
                print("              white")
            elif self._current_era == "future": 
                print("                          white")
        elif self.p_num == 2: 
            if self._current_era == "past": 
                print("  black  ")
            elif self._current_era == "present": 
                print("+-+-+-+-+   +-")
                print("              black")
            elif self._current_era == "future": 
                print("                          black")
    
                

