from memento import Memento

class Originator:
    """
    Saves the state of an object in a snapshot
    """
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def save(self):
        """
        Saves the state of the player
        - current player
        - number of turns 
        - each board
        - save into a memento (returns a Memento) - "friend of the memento"
        """
        current_player = self.game_manager.current_player
        num_turns = self.game_manager.num_turns
        board_state = {}
        for era in ["past", "present", "future"]:
            board = self.game_manager.boards.get_board(era)
            tiles = []
            for row in board.board:
                tile_row = []
                for p in row:
                    if p:
                        tile_row.append(p.denotation)
                    else:
                        tile_row.append(None)
                tiles.append(tile_row)
            board_state[era] = {"tiles": tiles, "current_pieces": list(board.current_pieces)}

        return Memento(
            board_state,
            {
            "p_num": self.game_manager.player1.p_num,
            "current_era": self.game_manager.player1._current_era,
            "num_on_board": self.game_manager.player1._num_on_board,
            "pieces_on_board": list(self.game_manager.player1.pieces_on_board),
            "pieces_supply": [p.denotation for p in self.game_manager.player1.pieces_supply],
            "pieces": [{
                "denotation": p.denotation,
                "era": p.current_era,
                "pos": p.location_on_board
            } for p in self.game_manager.player1.pieces]
            },
            {
            "p_num": self.game_manager.player2.p_num,
            "current_era": self.game_manager.player2._current_era,
            "num_on_board": self.game_manager.player2._num_on_board,
            "pieces_on_board": list(self.game_manager.player2.pieces_on_board),
            "pieces_supply": [p.denotation for p in self.game_manager.player2.pieces_supply],
            "pieces": [{
                "denotation": p.denotation,
                "era": p.current_era,
                "pos": p.location_on_board
            } for p in self.game_manager.player2.pieces]
            },
            current_player,
            num_turns
        )

    def restore(self, memento):
        """
        restores the last state
        """
        self.game_manager.current_player = memento.current_player
        self.game_manager.num_turns = memento.num_turns

        for era in ["past", "present", "future"]:
            board = self.game_manager.boards.get_board(era)
            board.board = [[None for i in range(4)] for i in range(4)]
            board.current_pieces = list(memento.boards_data[era]["current_pieces"])

        # get the current era, num on board, pieces on board based on the memento
        self.game_manager.player1._current_era = memento.player1_data["current_era"]
        self.game_manager.player1._num_on_board = memento.player1_data["num_on_board"]
        self.game_manager.player1.pieces_on_board = list(memento.player1_data["pieces_on_board"])

        # maps the denotation of each piece belonging to player1
        den_to_piece_player1 = {}
        for p in self.game_manager.player1.pieces:
            den_to_piece_player1[p.denotation] = p
        
        # go through all the pieces and set the data of all the pieces
        for piece_data in memento.player1_data["pieces"]:
            p = den_to_piece_player1[piece_data["denotation"]]
            p.set_era(piece_data["era"])
            if piece_data["pos"]:
                p.set_position(piece_data["pos"][0], piece_data["pos"][1])
            else:
                p.location_on_board = None
        self.game_manager.player1.pieces_supply = []
        for den in memento.player1_data["pieces_supply"]:
            self.game_manager.player1.pieces_supply.append(den_to_piece_player1[den])

        # same process for player2
        self.game_manager.player2._current_era = memento.player2_data["current_era"]
        self.game_manager.player2._num_on_board = memento.player2_data["num_on_board"]
        self.game_manager.player2.pieces_on_board = list(memento.player2_data["pieces_on_board"])

        den_to_piece_player2 = {}
        for p in self.game_manager.player2.pieces:
            den_to_piece_player2[p.denotation] = p
        for piece_data in memento.player2_data["pieces"]:
            p = den_to_piece_player2[piece_data["denotation"]]
            p.set_era(piece_data["era"])
            if piece_data["pos"]:
                p.set_position(piece_data["pos"][0], piece_data["pos"][1])
            else:
                p.location_on_board = None

        self.game_manager.player2.pieces_supply = []
        for den in memento.player2_data["pieces_supply"]:
            self.game_manager.player2.pieces_supply.append(den_to_piece_player2[den])
        # get the board era
        for era in ["past", "present", "future"]:
            board = self.game_manager.boards.get_board(era)
            for r in range(4):
                for c in range(4):
                    piece_id = memento.boards_data[era]["tiles"][r][c]
                    if piece_id:
                        piece = None
                        for p in self.game_manager.player1.pieces + self.game_manager.player2.pieces:
                            if p.denotation == piece_id:
                                piece = p
                                break
                        board.board[r][c] = piece
