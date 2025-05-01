import tkinter as tk
from tkinter import messagebox
from human import Human
from caretaker import Caretaker
from board_manager import BoardManager
from originator import Originator
from factory import HumanFactory, RandomAIFactory, HeuristicAIFactory

class GameManager:
    def __init__(self, player1, player2, history_status, score_status):
        self._window = tk.Tk()
        self._window.title("That Time You Killed Me")
        self._window.geometry("1000x700")

        self._top = tk.Frame(self._window)
        self._top.pack(pady=10)

        self._boards_frame = tk.Frame(self._window)
        self._boards_frame.pack()

        self._bottom_frame = tk.Frame(self._window)
        self._bottom_frame.pack(pady=10)

        self.frames = {}
        self.buttons = {}
        for era in ["past", "present", "future"]:
            frame = tk.LabelFrame(self._boards_frame, text=era, padx=5, pady=5)
            frame.pack(side="left", padx=10)
            self.frames[era] = frame
            self.buttons[era] = []
            for r in range(4):
                row = []
                for c in range(4):
                    btn = tk.Button(frame, text="", width=6, height=3,
                                    command=lambda e=era, r=r, c=c: self.on_board_click(e, r, c))
                    btn.grid(row=r, column=c)
                    row.append(btn)
                self.buttons[era].append(row)

        self._valid_moves_list = ['n', 'e', 's', 'w', 'f', 'b']
        self.player1_arg = player1
        self.player2_arg = player2

        factory_map = {"human": HumanFactory(), "random": RandomAIFactory(), "heuristic": HeuristicAIFactory()}
        self.player1_factory = factory_map.get(player1, HumanFactory())
        self.player2_factory = factory_map.get(player2, HumanFactory())

        self.player1 = self.player1_factory.create_player(1, "past")
        self.player2 = self.player2_factory.create_player(2, "future")

        self._history = history_status
        self._score_status = "on" if score_status == "on" else "off"

        self.current_player = "white"
        self.num_turns = 1
        self.ended = False
        self.boards = BoardManager()

        self.originator = Originator(self)
        self.caretaker = Caretaker(self.originator)

        self.selected_piece = None
        self.highlighted_moves = []

        self.turn_label = tk.Label(self._top, text="Turn Info", font=("Helvetica", 14))
        self.turn_label.pack()

        self.white_era_label = tk.Label(self._top, text="White's Era: Past", font=("Helvetica", 12))
        self.white_era_label.pack()
        self.black_era_label = tk.Label(self._top, text="Black's Era: Future", font=("Helvetica", 12))
        self.black_era_label.pack()

        self._undo_button = tk.Button(self._bottom_frame, text="Undo", command=self.undo_and_update)
        self._undo_button.grid(row=0, column=0, padx=5)

        self._redo_button = tk.Button(self._bottom_frame, text="Redo", command=self.redo_and_update)
        self._redo_button.grid(row=0, column=1, padx=5)

        self._next_button = tk.Button(self._bottom_frame, text="Next Turn", command=self.next)
        self._next_button.grid(row=0, column=2, padx=5)

        self.era_buttons_frame = tk.Frame(self._window)
        self.era_buttons_frame.pack(pady=5)
        for era in ["past", "present", "future"]:
            btn = tk.Button(self.era_buttons_frame, text=era.title(), command=lambda e=era: self.select_focus_era(e))
            btn.pack(side="left", padx=5)

        self.player2.start_place_pieces(self.boards)
        self.player1.start_place_pieces(self.boards)
        self.update_board_display()
        self._print_score(self._score_status)

        if self._history == "on":
            self.caretaker.backup()

        self._window.mainloop()

    def update_turn_label(self):
        current_player_obj = self.get_current_player_obj()
        self.turn_label.config(
            text=f"Turn {self.num_turns}: {self.current_player}\nCurrent Era: {current_player_obj._current_era}")
        self.white_era_label.config(text=f"White's Era: {self.player1._current_era}")
        self.black_era_label.config(text=f"Black's Era: {self.player2._current_era}")

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

    def get_current_player_obj(self):
        return self.player1 if self.current_player == "white" else self.player2

    def update_board_display(self):
        for era in ["past", "present", "future"]:
            board = self.boards.get_board(era)
            for r in range(4):
                for c in range(4):
                    piece = board.whos_on_board(r, c)
                    if piece is not None:
                        color = "white" if piece.color == "white" else "black"
                        fg_color = "black" if color == "white" else "white"
                        self.buttons[era][r][c].config(text=piece.denotation, bg=color, fg=fg_color)
                    else:
                        self.buttons[era][r][c].config(text="", bg="SystemButtonFace")

    def on_board_click(self, era, r, c):
        pass  # placeholder

    def has_legal_moves(self, piece):
        pass  # placeholder

    def highlight_possible_moves(self, piece):
        pass  # placeholder

    def handle_move(self, dest_era, dest_r, dest_c):
        pass  # placeholder

    def clear_highlights(self):
        pass  # placeholder

    def select_focus_era(self, era):
        pass  # placeholder

    def next(self):
        self.update_turn_label()
        self.update_board_display()
        self.update_score()

    def _print_score(self, status):
        if status != "on":
            return
        self.update_score()

    def update_score(self):
        white_score_text = self._generate_score_text(self.player1, self.player2)
        black_score_text = self._generate_score_text(self.player2, self.player1)
        print(white_score_text)
        print(black_score_text)

    def _generate_score_text(self, player, opponent):
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

    def _valid_era(self, player, era):
        return era in ["past", "present", "future"] and player._current_era != era
