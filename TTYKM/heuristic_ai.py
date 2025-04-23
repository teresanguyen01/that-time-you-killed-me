from player import Player
import random 

class HeuristicAI(Player): 
    def __init__(self, p_num, era): 
        super().__init__(p_num, era)
    
    def heuristic_function(self, gameManager): 
        c1 = 1
        c2 = 2
        c3 = 3
        c4 = 4
        c5 = 5
        heuristic_score = c1*gameManager.calculate_era_presence(self) + c3*gameManager.calculate_supply(self) + c4*gameManager.calculate_centrality(self) + c5*gameManager.calculate_focus(self)
        return heuristic_score

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


    def select_direction(self, boardManager, piece, gameManager):
        """
        selects a direction
        """
        piece_selected = self.get_piece(piece)
        if piece_selected is None:
            return random.choice(['n', 'e', 's', 'w', 'f', 'b'])
        valid_moves = piece_selected.valid_moves(boardManager)
        max_heur_score = 0
        best_move = None
        for move in valid_moves: 
            heur_score = self.heuristic_function(gameManager)
            if heur_score > max_heur_score: 
                max_heur_score = heur_score
                best_move = move
        if not valid_moves or not best_move:
            return None
        return best_move

    def select_era(self):
        """
        selects a era
        """
        eras = ["past", "present", "future"]
        eras.remove(self._current_era)
        return random.choice(eras)
