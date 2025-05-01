# gui.py
import sys
import tkinter as tk
from tkinter import messagebox
from game_manager import GameManager

class GUI:
    def __init__(self, root, player1_type, player2_type, history, score_display):
        self.root = root
        self.root.title("Time Travel Chess")

        # Start the Game Manager with passed arguments
        self.game = GameManager(player1_type, player2_type, history, score_display)
        self.game.player2.start_place_pieces(self.game.boards)
        self.game.player1.start_place_pieces(self.game.boards)

        # Layout setup
        self.frames = {}
        self.buttons = {}
        self.selected_piece = None
        self.selected_piece_obj = None
        self.selected_era = None
        self.available_moves = []
        self.phase = "select_piece"  # 'select_move', 'select_era'

        
        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.white_era_label = tk.Label(top_frame, text="White Era: ", font=("Helvetica", 12))
        self.white_era_label.pack()

        self.black_era_label = tk.Label(top_frame, text="Black Era: ", font=("Helvetica", 12))
        self.black_era_label.pack()

        self.turn_label = tk.Label(top_frame, text="Turn Info", font=("Helvetica", 14))
        self.turn_label.pack()

        self.score_label = tk.Label(top_frame, text="", font=("Helvetica", 12))
        self.score_label.pack()


        boards_frame = tk.Frame(self.root)
        boards_frame.pack()

        for era in ["past", "present", "future"]:
            frame = tk.LabelFrame(boards_frame, text=era.capitalize(), padx=5, pady=5)
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

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        self.undo_button = tk.Button(bottom_frame, text="Undo", command=self.undo)
        self.undo_button.grid(row=0, column=0, padx=5)

        self.redo_button = tk.Button(bottom_frame, text="Redo", command=self.redo)
        self.redo_button.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(bottom_frame, text="Next", command=self.next_turn)
        self.next_button.grid(row=0, column=2, padx=5)

    def update_board(self):
        """Update all buttons with pieces"""
        for era in ["past", "present", "future"]:
            board = self.game.boards.get_board(era)
            for r in range(4):
                for c in range(4):
                    piece = board.whos_on_board(r, c)
                    text = piece.denotation if piece else ""
                    self.buttons[era][r][c].config(text=text, state="normal", bg="SystemButtonFace")

        self.turn_label.config(
            text=f"Turn {self.game.num_turns} - {self.game.current_player.capitalize()} to move - "
                 f"Era: {self.get_current_player_obj()._current_era.capitalize()}"
        )
        if self.game._score_status == "on":
            white_score = self.get_score_text(self.game.player1)
            black_score = self.get_score_text(self.game.player2)
            self.score_label.config(text=f"White: {white_score} | Black: {black_score}")
        else:
            self.score_label.config(text="")
        self.white_era_label.config(text=f"White Era: {self.game.player1._current_era.capitalize()}")
        self.black_era_label.config(text=f"Black Era: {self.game.player2._current_era.capitalize()}")


    def on_board_click(self, era, row, col):
        """Handle board button click"""
        if self.phase == "select_piece":
            piece = self.game.boards.get_board(era).whos_on_board(row, col)
            if piece and piece.owner.p_num == (1 if self.game.current_player == "white" else 2):
                if piece.current_era == self.get_current_player_obj()._current_era:
                    if piece.valid_moves(self.game.boards):
                        # Only select if the piece actually has legal moves
                        self.selected_piece = piece.denotation
                        self.selected_piece_obj = piece
                        self.highlight_moves(piece)
                        self.phase = "select_move"
                    else:
                        messagebox.showinfo("No moves", "This piece has no legal moves!")
        elif self.phase == "select_move":
            if (era, row, col) in self.available_moves:
                # Move the selected piece to this location
                self.move_piece_to(era, row, col)
                self.ask_next_era()

    def highlight_moves(self, piece):
        """Highlight valid moves"""
        self.clear_highlights()
        moves = piece.valid_moves(self.game.boards)
        current_era = piece.current_era
        r, c = piece.location_on_board
        self.available_moves = []

        for move in moves:
            if move in ['n', 'e', 's', 'w']:
                dr, dc = {'n': (-1, 0), 'e': (0, 1), 's': (1, 0), 'w': (0, -1)}[move]
                new_r, new_c = r + dr, c + dc
                self.buttons[current_era][new_r][new_c].config(bg="lightgreen")
                self.available_moves.append((current_era, new_r, new_c))
            elif move in ['f', 'b']:
                next_era = piece._get_next_era(move)
                if next_era:
                    self.buttons[next_era][r][c].config(bg="lightblue")
                    self.available_moves.append((next_era, r, c))

    def clear_highlights(self):
        for era in ["past", "present", "future"]:
            for r in range(4):
                for c in range(4):
                    self.buttons[era][r][c].config(bg="SystemButtonFace")

    def move_piece_to(self, era, row, col):
        """Move selected piece"""
        target_era = era
        target_row, target_col = row, col
        current_r, current_c = self.selected_piece_obj.location_on_board
        current_era = self.selected_piece_obj.current_era

        if current_era == target_era:
            # Spatial move (n, e, s, w)
            if target_row < current_r:
                move = 'n'
            elif target_row > current_r:
                move = 's'
            elif target_col < current_c:
                move = 'w'
            elif target_col > current_c:
                move = 'e'
        else:
            # Time move (f, b)
            move = 'f' if ["past", "present", "future"].index(target_era) > ["past", "present", "future"].index(current_era) else 'b'

        if not self.get_current_player_obj().make_move(self.game.boards, self.selected_piece, move):
            messagebox.showerror("Error", "Move failed. Try again.")
            self.reset_selection()
            return

        self.reset_selection()

    def ask_next_era(self):
        """Ask user to pick next era"""
        self.phase = "select_era"
        top = tk.Toplevel(self.root)
        top.title("Choose next era")

        tk.Label(top, text="Select next era:").pack(pady=10)

        for era in ["past", "present", "future"]:
            if era != self.get_current_player_obj()._current_era:
                tk.Button(top, text=era.capitalize(),
                          command=lambda e=era, window=top: self.set_next_era(e, window)).pack(pady=5)

    def set_next_era(self, era, window):
        """Set player's next era"""
        player = self.get_current_player_obj()
        player.update_current_era(era)
        self.game.num_turns += 1
        self.game.current_player = "white" if self.game.current_player == "black" else "black"
        self.check_end_game()
        window.destroy()
        self.update_board()

    def get_current_player_obj(self):
        return self.game.player1 if self.game.current_player == "white" else self.game.player2

    def get_score_text(self, player):
        return (f"Eras: {self.game.calculate_era_presence(player)}, "
                f"Adv: {self.game.calculate_piece_advantage(player, self.game.player2 if player.p_num == 1 else self.game.player1)}, "
                f"Supply: {self.game.calculate_supply(player)}, "
                f"Center: {self.game.calculate_centrality(player)}, "
                f"Focus: {self.game.calculate_focus(player)}")

    def next_turn(self):
        """Advance the game state properly (for Human and AI players)"""
        current_player_obj = self.get_current_player_obj()
        is_human = current_player_obj.__class__.__name__.lower() == "human"

        if self.phase != "select_piece":
            # User hasn't finished moving yet
            messagebox.showinfo("Info", "You must select a piece, make a move, and pick an era first!")
            return

        if not is_human:
            # AI Move
            copy = current_player_obj.select_copy(self.game.boards)
            if copy is None:
                messagebox.showerror("AI Error", "AI failed to select a piece!")
                return

            move1 = current_player_obj.select_direction(self.game.boards, copy)
            if move1:
                current_player_obj.make_move(self.game.boards, copy, move1)

            move2 = current_player_obj.select_direction(self.game.boards, copy)
            if move2:
                current_player_obj.make_move(self.game.boards, copy, move2)

            era = current_player_obj.select_era()
            if era:
                current_player_obj.update_current_era(era)

        # After AI or human, advance turn
        self.game.num_turns += 1
        self.game.current_player = "white" if self.game.current_player == "black" else "black"

        if self.game._history == "on":
            self.game.caretaker.backup()

        self.check_end_game()
        self.update_board()
        self.reset_selection()


    def undo(self):
        """Undo last move if possible"""
        self.game.caretaker.undo()
        self.update_board()
        self.reset_selection()

    def redo(self):
        """Redo last undone move if possible"""
        self.game.caretaker.redo()
        self.update_board()
        self.reset_selection()


    def reset_selection(self):
        self.selected_piece = None
        self.selected_piece_obj = None
        self.available_moves = []
        self.phase = "select_piece"
        self.clear_highlights()


    def check_end_game(self):
        if self.game._check_game_end():
            winner = "White" if self.game.current_player == "black" else "Black"
            play_again = messagebox.askyesno("Game Over", f"{winner} wins! Play again?")
            if play_again:
                self.game.__init__("human", "human", "on", "on")
                self.update_board()
            else:
                self.root.destroy()

if __name__ == "__main__":
    # Read command-line arguments
    try:
        player1_type = sys.argv[1]
        player2_type = sys.argv[2]
        history = sys.argv[3]
        score_display = sys.argv[4]
    except IndexError:
        # Not enough arguments, set defaults
        player1_type = "human"
        player2_type = "human"
        history = "off"
        score_display = "off"

    root = tk.Tk()
    gui = GUI(root, player1_type, player2_type, history, score_display)
    root.mainloop()
