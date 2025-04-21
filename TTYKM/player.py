from board import Board
from piece import Piece
# what it is capable of doing and where it can move on the board 
# this is how I would like to move

class Player:
    """
    Represents a player -- manages pieces, interacts with the board,
    and executes moves.
    """
    # white = 1 | black = 2
    def __init__(self, p_num, era): 
        self._board = Board(era)
        self.p_num = p_num
        self._current_era = era
        self.num_placed = 0
        self._num_on_board = 0
        self.pieces = []
        self.pieces_supply = []
        self._initalize_pieces()
        self.pieces_on_board = []
        self.num_dead_pieces = 0

    def _initalize_pieces(self): 
        """
        initalizes the pieces: if player 1, then all the pieces are represented as letters.
        if player 2, then all the pieces are represented as numbers (string numbers)
        """
        if self.p_num == 1:
            self.pieces = [Piece(None, None, f"{chr(64 + i)}", self) for i in range(1, 8)]
        else:
            self.pieces = [Piece(None, None, f"{str(i)}", self) for i in range(1, 8)]
        # for keeping track of the supply 
        self.pieces_supply = self.pieces.copy()
    
    def start_place_pieces(self, BoardManager): 
        """
        Takes in the boardmananger and places and sets the pieces to start the game 
        """
        # player 1 is white (A, B, C)
        # player 2 is black (1, 2, 3)
        if self.p_num == 1:
            self.place_and_set_piece(self.pieces[0], BoardManager.past_board, 3, 3, "past")
            self.place_and_set_piece(self.pieces[1], BoardManager.present_board, 3, 3, "present")
            self.place_and_set_piece(self.pieces[2], BoardManager.future_board, 3, 3, "future")
        elif self.p_num == 2:
            self.place_and_set_piece(self.pieces[0], BoardManager.past_board, 0, 0, "past")
            self.place_and_set_piece(self.pieces[1], BoardManager.present_board, 0, 0, "present")
            self.place_and_set_piece(self.pieces[2], BoardManager.future_board, 0, 0, "future")
    
    def place_and_set_piece(self, piece, board, row, col, era):
        """
        takes in a board, piece, row, col, and era to initalize
        - place piece on the board
        - set the position of the piece
        - set the era of the piece
        - increment the number of pieces on the board
        - append the pieces to pieces_on_board
        """
        board.place_piece(piece, row, col)
        piece.set_position(row, col)
        piece.set_era(era)
        self._num_on_board += 1
        self.num_placed += 1
        if piece in self.pieces_supply: 
            self.pieces_supply.remove(piece)
        self.pieces_on_board.append(piece.denotation)
    
    def make_move(self, boards, copy, move):
        """
        Takes in a boardManager, copy (String), and move (String) and executes the move
        uses functions 
        - Player: get_piece
        - BoardManager: get_board
        - Piece: move_piece
        - Player: place_and_set
        """
        # get the piece based on the copy denotation
        piece = self.get_piece(copy)
        if piece is None:
            return False

        board = boards.get_board(piece.current_era)

        # Track old position BEFORE moving
        old_row, old_col = piece.location_on_board
        old_era = piece.current_era

        if move == "b":
            if piece.move_piece(boards, board, move):
                # Now piece has moved, we can use the previous info to leave a copy
                if self.num_placed < 7:
                    new_piece = self.pieces_supply[0]
                    self.pieces_supply.remove(new_piece)
                    old_board = boards.get_board(old_era)
                    if old_board.whos_on_board(old_row, old_col) is None:
                        self.place_and_set_piece(new_piece, old_board, old_row, old_col, old_era)
                return True
        else:
            return piece.move_piece(boards, board, move)

        return False
    def get_piece(self, picked_piece): 
        """
        Get the piece from the user based on a String denotation (ex: n, e, w, s)
        """
        for piece in self.pieces: 
            if piece.denotation == picked_piece: 
                return piece
        else: 
            return None
    
    def update_current_era(self, era): 
        """
        Update the player's current era 
        """
        self._current_era = era

    def print_era(self): 
        """
        print which era the player is on
        """
        if self.p_num == 1: 
            if self._current_era == "past": 
                print("  white  ")
            elif self._current_era == "present": 
                print("              white  ")
            elif self._current_era == "future": 
                print("                          white  ")
        elif self.p_num == 2: 
            if self._current_era == "past": 
                print("  black  ")
            elif self._current_era == "present": 
                print("              black  ")
            elif self._current_era == "future": 
                print("                          black  ")
        
    def remove_piece_from_board_from_player(self, piece): 
        """
        remove the piece from the board based on the piece given
        """
        # remove the piece denotation from the board
        if piece.denotation in self.pieces_on_board:
            self.pieces_on_board.remove(piece.denotation)
            self._num_on_board -= 1
            self.num_dead_pieces += 1




    
            
            
    



