class Piece: 
    """
    A singular piece on the board
    """
    def __init__(self, era, location_on_board, denotation, player): 
        self.location_on_board = location_on_board
        self.current_era = era
        self.denotation = denotation
        self.owner = player

    def move_piece(self, boardManager, board, move): 
        """
        moves the piece in the board
        """
        # handle move in time f and b
        if move in ['f', 'b']:
            return self._move_in_time(boardManager, board, move)
        return self._move_in_space(board, move)


    def _move_in_time(self, boardManager, board, move):
        """
        determines if the move needs to move forward or backward
        """
        if move == 'f':
            return self._move_forward_in_time(boardManager, board)
        elif move == 'b':
            return self._move_backward_in_time(boardManager, board)

    def _move_forward_in_time(self, boardManager, board):
        """
        moves the piece forward in time
        """
        # can't move more forward than the future 
        if self.current_era == 'future':
            return False

        if self.current_era == "past": 
            next_era = "present"
        else: 
            next_era = "future"

        # get the board of the next era 
        board2 = boardManager.get_board(next_era)
        
        # if there is a piece on that board, then we cannot move forward 
        if board2.whos_on_board(self.location_on_board[0], self.location_on_board[1]) is not None:
            return False

        # set the piece's current era to the next era 
        self.current_era = next_era

        # place the piece on the new board
        board2.place_piece(self, self.location_on_board[0], self.location_on_board[1])

        # remove the piece on the old board
        board.remove_piece(self.location_on_board[0], self.location_on_board[1])

        return True

    def _move_backward_in_time(self, boardManager, board):
        """
        moves the piece backward in time -- follows the same logic as forward in time 
        """
        if self.current_era == 'past':
            return False

        if self.current_era == 'present':
            next_era = 'past'
        else:
            next_era = 'present'
        
        board2 = boardManager.get_board(next_era)
        
        if board2.whos_on_board(self.location_on_board[0], self.location_on_board[1]) is not None:
            return False

        self.current_era = next_era
        board2.place_piece(self, self.location_on_board[0], self.location_on_board[1])
        board.remove_piece(self.location_on_board[0], self.location_on_board[1])
        return True

    def _get_next_era(self, move):
        """ 
        get the next era based on the move (only for f and b)
        """
        if move == 'f' and self.current_era != 'future':
            if self.current_era == 'past':
                return 'present'
            elif self.current_era == 'present':
                return 'future'
        elif move == 'b' and self.current_era != 'past':
            if self.current_era == 'present':
                return 'past'
            elif self.current_era == 'future':
                return 'present'
        return None

    def _move_in_space(self, board, move):
        """
        represents a normal move (n, e, w, s)
        """
        directions = {
            'n': (-1, 0),
            'e': (0, 1),
            'w': (0, -1),
            's': (1, 0)
        }

        if move not in directions:
            return False

        # calculate the new row and new col based on the direction given 
        new_row = self.location_on_board[0] + directions[move][0]
        new_col = self.location_on_board[1] + directions[move][1]

        # check for out of bounds
        if not (0 <= new_row < 4 and 0 <= new_col < 4):
            return False

        # check if there is a piece at the new row and new col 
        piece_there = board.whos_on_board(new_row, new_col)
        
        if piece_there is None:
            board.remove_piece(self.location_on_board[0], self.location_on_board[1])
            board.place_piece(self, new_row, new_col)
        elif piece_there is not None and piece_there.owner != self.owner: 
            # print("alr so it is working but like...", piece_there.denotation)
            piece_there.owner.remove_piece_from_board_from_player(piece_there)
            board.remove_piece(self.location_on_board[0], self.location_on_board[1])
            board.place_piece(self, new_row, new_col)
            # print("BRO!", piece_there.owner.pieces_on_board)
        else:
            return False

        self.location_on_board = (new_row, new_col)
        return True
    
    def set_era(self, era): 
        """
        sets the era of the piece
        """
        self.current_era = era
    
    def set_position(self, r, c): 
        """
        sets the location of the piece
        """
        self.location_on_board = (r, c)

    def valid_moves(self, boardManager):
        """
        Check all the valid moves
        """
        valid = []
        r, c = self.location_on_board
        board = boardManager.get_board(self.current_era)

        for move, (dr, dc) in {'n': (-1, 0), 'e': (0, 1), 's': (1, 0), 'w': (0, -1)}.items():
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < 4 and 0 <= new_c < 4:
                target = board.whos_on_board(new_r, new_c)
                if target is None or target.owner != self.owner:
                    valid.append(move)

        for move in ['f', 'b']:
            next_era = self._get_next_era(move)
            if next_era is None:
                continue
            target_board = boardManager.get_board(next_era)
            if target_board.whos_on_board(r, c) is None:
                valid.append(move)

        return valid

    def __repr__(self): 
        return f"{self.denotation}"
