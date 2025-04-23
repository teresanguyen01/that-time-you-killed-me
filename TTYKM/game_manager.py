from human import Human 
# from heuristic_ai import HeuristicAI
# from random_ai import RandomAI
from caretaker import Caretaker
from board_manager import BoardManager
# from memento import Memento
from originator import Originator
from factory import HumanFactory, RandomAIFactory, HeuristicAIFactory

class GameManager: 
    """Manages the game"""

    # player 1 is white and player 2 is black
    def __init__(self, player1, player2, history_status, score_status):
        self.valid_moves_list = ['n', 'e', 's', 'w', 'f', 'b']
        self.player1_arg = player1 
        self.player2_arg = player2

        # create a factory map: key is string and value is the method
        factory_map = {"human": HumanFactory(), "random": RandomAIFactory(), "heuristic": HeuristicAIFactory()}

        self.player1_factory = factory_map.get(player1, HumanFactory())
        self.player2_factory = factory_map.get(player2, HumanFactory())

        self.player1 = self.player1_factory.create_player(1, "past")
        self.player2 = self.player2_factory.create_player(2, "future")

        self._history = history_status
        if score_status == "on": 
            self._score_status = "on"
        else: 
            self._score_status = "off"
        self.current_player = "white"
        self.num_turns = 1
        self.ended = False
        self.boards = BoardManager()
        # originator takes in the game manager --> state 
        self.originator = Originator(self)
        # caretaker takes in the originator 
        self.caretaker = Caretaker(self.originator)

    def _start_game(self): 
        """Starts the game and handles the gameplay"""
        self.player2.start_place_pieces(self.boards)
        self.player1.start_place_pieces(self.boards)

        # save the originator's state if history is on
        if self._history == "on":
            self.caretaker.backup()

        while not self.ended:
            print("---------------------------------")
            self.player2.print_era() # prints the eras --> like "    white    " "white     " etc
            self.boards.print_boards() # prints all the boards in their format 
            self.player1.print_era()
            print(f"Turn: {self.num_turns}, Current player: {self.current_player}")
            self._print_score(self._score_status) # only turns on if _score_status is "on"

            # check game ending each run
            self.ended = self._check_game_end()
            if self.ended:
                print("Play again?")
                if input() == "yes":
                    # start the game again by running the gamemanager again
                    self.__init__(self.player1_arg, self.player2_arg, self._history, self._score_status)
                    self._start_game()
                    return
                else:
                    break

            if self._history == "on":
                print("undo, redo, or next")
                if (isinstance(self.player1, Human) and self.current_player == "white") or (isinstance(self.player2, Human) and self.current_player == "black"): 
                    choice = input()
                    if choice == "undo":
                        self.caretaker.undo()
                        continue
                    elif choice == "redo":
                        self.caretaker.redo()
                        continue
                    elif choice == "next":
                        pass
                    else:
                        continue
            
            # set the current player and human checks to make sure we don't run undo/redo/next for the non humans
            current_player_obj = self.player1 if self.current_player == "white" else self.player2
            is_human = isinstance(current_player_obj, Human)
            current_era = current_player_obj._current_era

            # check if there are any movable pieces to begin with --> if not -> no copies to move and pick an era 
            has_movable = False
            for piece in current_player_obj.pieces_on_board:
                if self.boards.is_piece_in_era(piece, current_era):
                    has_movable = True
                    break

            if not has_movable:
                print("No copies to move")
                copy = move1 = move2 = None
            else:
                while True:
                    if is_human:
                        print("Select a copy to move")
                        copy = input()
                    else:
                        # for the non humans
                        copy = current_player_obj.select_copy(self.boards)
                        break 
                    if self._valid_copy(copy):
                        break
                while True:
                    if is_human:
                        print(f"Select the first direction to move {self.valid_moves_list}")
                        move1 = input()
                        if move1 not in self.valid_moves_list:
                            print("Not a valid direction")
                            continue
                    else:
                        if self.player1_arg == "heuristic": 
                            move1 = current_player_obj.select_direction(self.boards, copy, self)
                        else: 
                            move1 = current_player_obj.select_direction(self.boards, copy)
                        if move1 not in self.valid_moves_list: 
                            break
                    if (current_player_obj.make_move(self.boards, copy, move1)): 
                        break 
                    else:
                        print(f"Cannot move {move1}")

                        
                while True:
                    if is_human:
                        print(f"Select the second direction to move {self.valid_moves_list}")
                        move2 = input()
                        if move2 not in self.valid_moves_list:
                            print("Not a valid direction")
                            continue
                    else:
                        if self.player1_arg == "heuristic": 
                            move2 = current_player_obj.select_direction(self.boards, copy, self)
                        else: 
                            move2 = current_player_obj.select_direction(self.boards, copy)
                        if move2 not in self.valid_moves_list: 
                            break
                    if (current_player_obj.make_move(self.boards, copy, move2)): 
                        break
                    else:
                        print(f"Cannot move {move2}")

            while True:
                if is_human:
                    print("Select the next era to focus on ['past', 'present', 'future']")
                    era = input()
                else:
                    era = current_player_obj.select_era()

                if self._valid_era(current_player_obj, era):
                    break

            self._handle_turn(era)
            print(f"Selected move: {copy},{move1},{move2},{era}")
            if self._history == "on":
                self.caretaker.backup()

    def _handle_turn(self, era): 
        """
        Updates the eras, increases the number of turns, and changes the player
        args: era (to update the era)
        1. updates the current era for the player
        2. increments the number of turns
        3. updates the current player 
        """
        if self.current_player == "white":
            self.player1.update_current_era(era)
        else:
            self.player2.update_current_era(era)
        self.num_turns += 1
        self.current_player = "white" if self.current_player == "black" else "black"
        
    def _check_game_end(self): 
        """
        Check if the game ends and decides who wins
        game ends if the pieces are on the board are in one era
        returns True if game has ended and false otherwise
        """
        eras1 = set()
        eras2 = set()
        for pieces in self.player1.pieces_on_board: 
            piece = self.player1.get_piece(pieces)
            if piece != None: 
                eras1.add(piece.current_era)
        for pieces in self.player2.pieces_on_board: 
            piece = self.player2.get_piece(pieces)
            if piece != None: 
                eras2.add(piece.current_era)
        # print("WTF", self.player1.pieces_on_board)
        # print("WTF", self.player2.pieces_on_board)
        # print(len(eras1))
        # print(len(eras2))
        if len(eras2) == 1 and len(eras1) > 1:
            print("white has won")
            return True
        elif len(eras1) == 1 and len(eras2) > 1:
            print("black has won")
            return True
        return False 
        
    def _valid_era(self, player, era): 
        """
        Checks if the player's selected era is valid 
        """
        if era not in ["past", "present", "future"]: 
            print("Not a valid era")
            return False
        if player._current_era == era: 
            print("Cannot select the current era")
            return False
        return True 
    
    def _valid_copy(self, copy): 
        """Check if the player selected a valid copy"""
        player1_pieces = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        player2_pieces = ['1', '2', '3', '4', '5', '6', '7']

        if self.current_player == "white": 
            if copy not in player1_pieces:
                if copy in player2_pieces:
                    print("That is not your copy")
                else:
                    print("Not a valid copy")
                return False
            if copy not in self.player1.pieces_on_board: 
                print("Not a valid copy")
                return False
            if not self.boards.is_piece_in_era(copy, self.player1._current_era): 
                print("Cannot select a copy from an inactive era")
                return False
        elif self.current_player == "black": 
            if copy not in player2_pieces:
                if copy in player1_pieces:
                    print("That is not your copy")
                else:
                    print("Not a valid copy")
                return False
            if copy not in self.player2.pieces_on_board: 
                print("Not a valid copy")
                return False
            if not self.boards.is_piece_in_era(copy, self.player2._current_era): 
                print("Cannot select a copy from an inactive era")
                return False
        return True

    def _print_score(self, status): 
        """
        prints the score depending on the status (on or off)
        """
        if status == "on": 
            print(
                f"white's score: {self.calculate_era_presence(self.player1)} eras, "
                f"{self.calculate_piece_advantage(self.player1, self.player2)} advantage, "
                f"{self.calculate_supply(self.player1)} supply, "
                f"{self.calculate_centrality(self.player1)} centrality, "
                f"{self.calculate_focus(self.player1)} in focus"
            )
            print(
                f"black's score: {self.calculate_era_presence(self.player2)} eras, "
                f"{self.calculate_piece_advantage(self.player2, self.player1)} advantage, "
                f"{self.calculate_supply(self.player2)} supply, "
                f"{self.calculate_centrality(self.player2)} centrality, "
                f"{self.calculate_focus(self.player2)} in focus"
            )
        else: 
            return

    def calculate_era_presence(self, player):
        """
        Calculates the era presence based on the player
        """
        eras1 = set()
        for pieces in player.pieces_on_board: 
            piece = player.get_piece(pieces)
            if piece != None: 
                eras1.add(piece.current_era)
        return len(eras1)

    def calculate_piece_advantage(self, p1, p2):
        """
        Calculates the piece advantage given two players
        """
        return p1._num_on_board - p2._num_on_board
    
    def calculate_supply(self, player):
        """
        Calculates the player's supply (how many pieces the player has left to put on the board)
        """
        return len(player.pieces_supply)

    def calculate_centrality(self, player):
        """
        Calculates how many pieces the player has in the center of the board
        """
        centrality = 0
        for piece in player.pieces: 
            if piece.location_on_board != None and 0 < piece.location_on_board[0] < 3 and 0 < piece.location_on_board[1] < 3: 
                centrality += 1
        return centrality
    
    def calculate_focus(self, player):
        """
        Calculates on how many pieces the player has on the board on their current era
        """
        focus = 0
        board = self.boards.get_board(player._current_era)
        for piece in player.pieces_on_board: 
            if piece in board.current_pieces: 
                focus += 1
        return focus
