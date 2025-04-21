class Board: 
    """
    Represents one board
    """
    def __init__(self, era): 
        self.board = [[None for i in range(4)] for i in range(4)]
        self._era = era
        self.current_pieces = []

    def place_piece(self, piece, row, col): 
        """
        Place the piece on the board and update the current pieces on the board
        """
        if 0 <= row < 4 and 0 <= col < 4: 
            self.board[row][col] = piece
        if piece.denotation not in self.current_pieces: 
            self.current_pieces.append(piece.denotation)
    
    def remove_piece(self, row, col): 
        """
        Remove the piece from the board
        if there was a piece on the board, remove it from the current pieces on the board
        """
        piece_before = self.board[row][col]
        self.board[row][col] = None
        if piece_before and piece_before.denotation in self.current_pieces:
            self.current_pieces.remove(piece_before.denotation)
        
    def whos_on_board(self, row, col): 
        """
        Returns what was on the board
        """
        return (self.board[row][col])
    

if __name__ == "__main__":
    board = Board("past", 1)
    board.update_board("A", move1=None, move2=None)
    