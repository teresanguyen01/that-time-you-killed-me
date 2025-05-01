from player import Player
import random

class RandomAI(Player): 
    """
    RandomAI that inherits from player
    selects a random copy, direction, and era
    """
    def __init__(self, p_num, era): 
        super().__init__(p_num, era)

    def select_copy(self, boardManager):
        """
        selects a copy
        """
        board_current_pieces = boardManager.get_board(self._current_era).current_pieces
        player1_pieces = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        player2_pieces = ['1', '2', '3', '4', '5', '6', '7']
        if self.p_num == 1:
            available_pieces = []
            for piece in player1_pieces:
                if piece in board_current_pieces:
                    available_pieces.append(piece)
        elif self.p_num == 2:
            available_pieces = []
            for piece in player2_pieces:
                if piece in board_current_pieces:
                    available_pieces.append(piece)
        if available_pieces == []: 
            return None
        return random.choice(available_pieces)

    def select_direction(self, boardManager, piece):
        """
        selects a direction
        """
        piece_selected = self.get_piece(piece)
        if piece_selected is None:
            return random.choice(['n', 'e', 's', 'w', 'f', 'b'])
        valid_moves = piece_selected.valid_moves(boardManager)
        if not valid_moves:
            return None
        return random.choice(valid_moves)

    def select_era(self):
        """
        selects a era
        """
        eras = ["past", "present", "future"]
        eras.remove(self._current_era)
        return random.choice(eras)
