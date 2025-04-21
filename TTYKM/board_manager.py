from board import Board

class BoardManager: 
    """
    Manages all the boards
    """
    def __init__(self):
        """initalize the boards"""
        self.past_board = Board("past")
        self.present_board = Board("present")
        self.future_board = Board("future")

    def print_boards(self): 
        """
        Print the boards
        """
        for i, row in enumerate(self.past_board.board):
            print("+-+-+-+-+   +-+-+-+-+   +-+-+-+-+")
            for value in row:
                print(f"|{value if value != None else ' '}", end="")
            print("|   ", end="")

            for value in self.present_board.board[i]:
                print(f"|{value if value != None else ' '}", end="")
            print("|   ", end="")

            for value in self.future_board.board[i]:
                print(f"|{value if value != None else ' '}", end="")
            print("|") 

        print("+-+-+-+-+   +-+-+-+-+   +-+-+-+-+")
    
    def is_piece_in_era(self, copy, current_era): 
        """
        Check if the pieces are in the correct board for the era selected
        """
        if current_era == "past": 
            return copy in self.past_board.current_pieces
        elif current_era == "present": 
            return copy in self.present_board.current_pieces
        elif current_era == "future": 
            return copy in self.future_board.current_pieces
        else:
            return False

    def get_board(self, era): 
        """
        Returns a board object based on the era
        """
        if era == "past": 
            return self.past_board
        elif era == "present": 
            return self.present_board
        elif era == "future": 
            return self.future_board
        

if __name__ == "__main__": 
    game = BoardManager()
    game.print_boards()
