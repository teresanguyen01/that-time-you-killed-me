class Memento:
    """
    the state of the last turn
    """
    def __init__(self, boards_data, player1_data, player2_data, current_player, num_turns):
        self.boards_data = boards_data
        self.player1_data = player1_data
        self.player2_data = player2_data
        self.current_player = current_player
        self.num_turns = num_turns
