class Board: 
    def __init__(self, era, focus_players): 
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self._era = era
        self._who_there = focus_players # int input 
        if era == "past": 
            self.board[0][0] = 1
            self.board[3][3] = "A"
        elif era == "present": 
            self.board[0][0] = 2
            self.board[3][3] = "B"          
        elif era == "future": 
            self.board[0][0] = 3
            self.board[3][3] = "C"

    def move_player(self, copy, move1, move2): 
        index = None
        for i, row in enumerate(self.board): 
            for j, value in enumerate(row): 
                if value == copy: 
                    index = (i, j)
        print(index)
    
    def update_era_players(self, player): 
        self._who_there.append(player)
    
    def remove_player_from_era(self, player): 
        self._who_there.remove(player)
                

if __name__ == "__main__": 
    board = Board("past", 1)
    board.update_board("A", move1=None, move2=None)
    