from human import Human 
# from heuristic_ai import HeuristicAI
# from random_ai import RandomAI
import tkinter as tk 
from caretaker import Caretaker
from board_manager import BoardManager
# from memento import Memento
from tkinter import messagebox
from originator import Originator
from factory import HumanFactory, RandomAIFactory, HeuristicAIFactory

class GameManager: 
    """Manages the game"""

    # player 1 is white and player 2 is black
    def __init__(self, player1, player2, history_status, score_status):
        self._window = tk.Tk()
        self._window.title("That Time You Killed Me")
        self._window.geometry("1000x500")
        self._top = tk.Frame(self._window)
        self._top.pack(pady=10)
        self.frames = {}
        self.buttons = {}

        # self._white_era_label = tk.Label(self._top, text="White Era: ")
        # self._white_era_label.pack()

        self._boards_frame = tk.Frame(self._window)
        self._boards_frame.pack() 
        for era in ["past", "present", "future"]:
            frame = tk.LabelFrame(self._boards_frame, text=era, padx=5, pady=5)
            frame.pack(side="left", padx=10)
            self.frames[era] = frame
            self.buttons[era] = []
            for r in range(4):
                row = []
                for c in range(4):
                    btn = tk.Button(frame, text="", width=4, height=2,
                                    command=lambda e=era, row=r, col=c: self.on_board_click(e, row, col))
                    btn.grid(row=r, column=c)
                    row.append(btn)
                self.buttons[era].append(row)

        self._bottom_frame = tk.Frame(self._window)
        self._bottom_frame.pack(pady=10)

        self._valid_moves_list = ['n', 'e', 's', 'w', 'f', 'b']
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
        self.player2.start_place_pieces(self.boards)
        self.player1.start_place_pieces(self.boards)
        self.update_board_display()

        # originator takes in the game manager --> state 
        self.originator = Originator(self)
        # caretaker takes in the originator 
        self.caretaker = Caretaker(self.originator)
        self.turn_label = tk.Label(self._top, text="Turn Info", font=("Helvetica", 14))
        self.turn_label.pack()
        self.turn_label.config(
            text=f"Turn {self.num_turns}: {self.current_player}\nCurrent Era: {self.get_current_player_obj()._current_era}"
        )
        self._undo_button = tk.Button(self._bottom_frame, text="Undo", command=self.undo_and_update)
        self._undo_button.grid(row=0, column=0, padx=5)

        self._redo_button = tk.Button(self._bottom_frame, text="Redo", command=self.redo_and_update)
        self._redo_button.grid(row=0, column=1, padx=5)

        self._next_button = tk.Button(self._bottom_frame, text="Bruh", command=self.next)
        self._next_button.grid(row=0, column=2, padx=5)
        self._print_score(self._score_status)


    def undo_and_update(self):
        self.caretaker.undo()
        self.update_turn_label()
        self.update_board_display()
        self.update_score()

    def redo_and_update(self):
        self.caretaker.redo()
        self.update_turn_label()
        self.update_board_display()
        self.update_score()

    def update_turn_label(self):
        current_player_obj = self.get_current_player_obj()
        turn_text = f"Turn {self.num_turns}: {self.current_player}\nCurrent Era: {current_player_obj._current_era}"
        self.turn_label.config(text=turn_text)

    def get_current_player_obj(self):
        return self.player1 if self.current_player == "white" else self.player2
    
    def update_board_display(self):
        """Updates the GUI buttons to show the pieces on the board."""
        for era in ["past", "present", "future"]:
            board = self.boards.get_board(era)
            for r in range(4):
                for c in range(4):
                    piece = board.whos_on_board(r, c)
                    if piece is not None:
                        self.buttons[era][r][c].config(text=piece.denotation, bg="pink" if piece.color == "white" else "purple")
                    else:
                        self.buttons[era][r][c].config(text="", bg="SystemButtonFace")

    def next(self):
        """Performs the next move in the game (no undo/redo here)"""
        if self.ended:
            return

        print(f"Turn: {self.num_turns}, Current player: {self.current_player}")

        # Check if game ended
        self.ended = self._check_game_end()
        if self.ended:
            print("Game Over.")
            return

        # Setup current player
        current_player_obj = self.player1 if self.current_player == "white" else self.player2
        is_human = isinstance(current_player_obj, Human)
        current_era = current_player_obj._current_era

        # Check if there are movable pieces
        has_movable = any(self.boards.is_piece_in_era(piece, current_era) for piece in current_player_obj.pieces_on_board)

        if not has_movable:
            print("No copies to move")
            copy = move1 = move2 = None
        else:
            # Select copy
            if is_human:
                print("Select a copy to move")

                popup = tk.Toplevel(self._window)
                popup.title("Select Copy")

                entry = tk.Entry(popup, width=20)
                entry.pack(pady=10)

                def submit_copy():
                    user_input = entry.get()
                    if self._valid_copy(user_input):
                        self.selected_copy = user_input
                        popup.destroy()
                    else:
                        messagebox.showerror("Error", "Not a valid copy.")

                submit_button = tk.Button(popup, text="Submit", command=submit_copy)
                submit_button.pack()

                self._window.wait_window(popup)

                copy = self.selected_copy
            else:
                copy = current_player_obj.select_copy(self.boards, self)

            # Select first move
            while True:
                if is_human:
                    print(f"Select the first direction to move {self._valid_moves_list}")
                    popup1 = tk.Toplevel(self._window)
                    popup1.title("Select First Move")

                    entry1 = tk.Entry(popup1, width=20)
                    entry1.pack(pady=10)

                    def submit_move1():
                        move = entry1.get()
                        if move in self._valid_moves_list:
                            self.selected_move1 = move
                            popup1.destroy()
                        else:
                            messagebox.showerror("Error", "Not a valid direction.")

                    submit_button1 = tk.Button(popup1, text="Submit", command=submit_move1)
                    submit_button1.pack()

                    self._window.wait_window(popup1)

                    move1 = self.selected_move1
                else:
                    move1 = current_player_obj.select_direction(self.boards, copy, self) if self.player1_arg == "heuristic" else current_player_obj.select_direction(self.boards, copy)
                    if move1 not in self._valid_moves_list:
                        continue

                if current_player_obj.make_move(self.boards, copy, move1):
                    break
                else:
                    messagebox.showinfo("Move", f"Cannot move {move1}")
                    print(f"Cannot move {move1}")

            # Select second move
            while True:
                if is_human:
                    print(f"Select the second direction to move {self._valid_moves_list}")
                    popup2 = tk.Toplevel(self._window)
                    popup2.title("Select Second Move")

                    entry2 = tk.Entry(popup2, width=20)
                    entry2.pack(pady=10)

                    def submit_move2():
                        move = entry2.get()
                        if move in self._valid_moves_list:
                            self.selected_move2 = move
                            popup2.destroy()
                        else:
                            messagebox.showerror("Error", "Not a valid direction.")

                    submit_button2 = tk.Button(popup2, text="Submit", command=submit_move2)
                    submit_button2.pack()

                    self._window.wait_window(popup2)

                    move2 = self.selected_move2
                else:
                    move2 = current_player_obj.select_direction(self.boards, copy, self) if self.player1_arg == "heuristic" else current_player_obj.select_direction(self.boards, copy)
                    if move2 not in self._valid_moves_list:
                        continue

                if current_player_obj.make_move(self.boards, copy, move2):
                    break
                else:
                    messagebox.showinfo("Move", f"Cannot move {move2}")
                    print(f"Cannot move {move2}")

        # Select next era
        while True:
            if is_human:
                print("Select the next era to focus on ['past', 'present', 'future']")
                popup3 = tk.Toplevel(self._window)
                popup3.title("Select Era")

                entry3 = tk.Entry(popup3, width=20)
                entry3.pack(pady=10)

                def submit_era():
                    era_input = entry3.get()
                    if self._valid_era(current_player_obj, era_input):
                        self.selected_era = era_input
                        popup3.destroy()
                    else:
                        messagebox.showerror("Error", "Invalid era selected.")

                submit_button3 = tk.Button(popup3, text="Submit", command=submit_era)
                submit_button3.pack()

                self._window.wait_window(popup3)

                era = self.selected_era
            else:
                era = current_player_obj.select_era()

            if self._valid_era(current_player_obj, era):
                break

        self._handle_turn(era)
        print(f"Selected move: {copy},{move1},{move2},{era}")

        if self._history == "on":
            self.caretaker.backup()

        self.update_board_display()
        self.update_score()


    def _start_game(self):
        """Starts the game and handles the gameplay"""
        self.player2.start_place_pieces(self.boards)
        self.player1.start_place_pieces(self.boards)

        if self._history == "on":
            self.caretaker.backup()

        while not self.ended:
            if self._history == "on":
                if (isinstance(self.player1, Human) and self.current_player == "white") or (isinstance(self.player2, Human) and self.current_player == "black"):
                    while True:
                        print("undo, redo, or next")
                        choice = input()
                        if choice == "undo":
                            self.caretaker.undo()
                            break  # go back to top of while loop
                        elif choice == "redo":
                            self.caretaker.redo()
                            break
                        elif choice == "next":
                            self.next()
                            break
                        else:
                            print("Invalid choice. Please type 'undo', 'redo', or 'next'.")
                else:
                    self.next()
            else:
                self.next()
            
        self.ended = self._check_game_end()
        print(self.ended)
        if self.ended:
            answer = messagebox.askyesno("Game Over", "Play again?")
            if answer:  # answer is True if "Yes", False if "No"
                self.reset_game()
                self._start_game()

    def reset_game(self):
        """
        Resets the game state for a new game.
        """
        self.__init__(self.player1_arg, self.player2_arg, self._history, self._score_status)

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
        self.update_turn_label()
        
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
                    messagebox.showerror("Copy Selection Error", "That is not your copy")    
                    print("That is not your copy")
                else:
                    messagebox.showerror("Copy Selection Error", "Not a valid copy")    
                    print("Not a valid copy")
                return False
            if copy not in self.player1.pieces_on_board: 
                messagebox.showerror("Copy Selection Error", "Not a valid copy")    
                print("Not a valid copy")
                return False
            if not self.boards.is_piece_in_era(copy, self.player1._current_era): 
                messagebox.showerror("Copy Selection Error", "Cannot select a copy from an inactive era")    
                print("Cannot select a copy from an inactive era")
                return False
        elif self.current_player == "black": 
            if copy not in player2_pieces:
                if copy in player1_pieces:
                    messagebox.showerror("Copy Selection Error", "That is not your copy")                        
                    print("That is not your copy")
                else:
                    messagebox.showerror("Copy Selection Error", "Not a valid copy")    
                    print("Not a valid copy")
                return False
            if copy not in self.player2.pieces_on_board: 
                messagebox.showerror("Copy Selection Error", "Not a valid copy")    
                print("Not a valid copy")
                return False
            if not self.boards.is_piece_in_era(copy, self.player2._current_era): 
                messagebox.showerror("Copy Selection Error", "Cannot select a copy from an inactive era")                    
                print("Cannot select a copy from an inactive era")
                return False
        return True

    def _print_score(self, status):
        """
        Prints and updates the score depending on the status ("on" or "off").
        """
        if status != "on":
            return  # just skip if not "on"

        # Prepare updated text
        white_score_text = (
            f"white's score: {self.calculate_era_presence(self.player1)} eras, "
            f"{self.calculate_piece_advantage(self.player1, self.player2)} advantage, "
            f"{self.calculate_supply(self.player1)} supply, "
            f"{self.calculate_centrality(self.player1)} centrality, "
            f"{self.calculate_focus(self.player1)} in focus"
        )
        black_score_text = (
            f"black's score: {self.calculate_era_presence(self.player2)} eras, "
            f"{self.calculate_piece_advantage(self.player2, self.player1)} advantage, "
            f"{self.calculate_supply(self.player2)} supply, "
            f"{self.calculate_centrality(self.player2)} centrality, "
            f"{self.calculate_focus(self.player2)} in focus"
        )

        # Print to console
        print(white_score_text)
        print(black_score_text)

        # Create labels if they don't exist yet
        if not hasattr(self, 'white_score_label'):
            self.white_score_label = tk.Label(self._top, text="White Score", font=("Helvetica", 14))
            self.white_score_label.pack()

        if not hasattr(self, 'black_score_label'):
            self.black_score_label = tk.Label(self._top, text="Black Score", font=("Helvetica", 14))
            self.black_score_label.pack()

        # Update the label texts
        self.white_score_label.config(text=white_score_text)
        self.black_score_label.config(text=black_score_text)

    def update_score(self):
        """
        Updates the white and black score labels in the GUI.
        """
        # Generate the score texts
        white_score_text = self._generate_score_text(self.player1, self.player2)
        black_score_text = self._generate_score_text(self.player2, self.player1)

        if not hasattr(self, 'white_score_label'):
            self.white_score_label = tk.Label(self._top, text="", font=("Helvetica", 14))
            self.white_score_label.pack()

        if not hasattr(self, 'black_score_label'):
            self.black_score_label = tk.Label(self._top, text="", font=("Helvetica", 14))
            self.black_score_label.pack()

        self.white_score_label.config(text=white_score_text)
        self.black_score_label.config(text=black_score_text)

    def _generate_score_text(self, player, opponent):
        """
        Generates the score text for a player.
        """
        return (
            f"{player.color}'s score: {self.calculate_era_presence(player)} eras, "
            f"{self.calculate_piece_advantage(player, opponent)} advantage, "
            f"{self.calculate_supply(player)} supply, "
            f"{self.calculate_centrality(player)} centrality, "
            f"{self.calculate_focus(player)} in focus"
        )

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
