from board import Board

class BoardManager: 
    def __init__(self):
        self.past_board = Board("past", "player1")
        self.present_board = Board("present", None)
        self.future_board = Board("future", "player2")

    def print_boards(self): 
        for i, row in enumerate(self.past_board.board):
            # Print top borders for the three boards
            print("+-+-+-+-+   +-+-+-+-+   +-+-+-+-+")

            for value in row:
                print(f"|{value if value != 0 else ' '}", end="")
            print("|   ", end="")
            print
            for value in self.present_board.board[i]:
                print(f"|{value if value != 0 else ' '}", end="")
            print("|   ", end="")

            for value in self.future_board.board[i]:
                print(f"|{value if value != 0 else ' '}", end="")
            print("|") 

        print("+-+-+-+-+   +-+-+-+-+   +-+-+-+-+")




if __name__ == "__main__": 
    game = BoardManager()
    game.print_boards()
