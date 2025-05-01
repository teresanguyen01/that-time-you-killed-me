from human import Human
from random_ai import RandomAI
from heuristic_ai import HeuristicAI

class PlayerFactory:
    """
    Produces familities of related objects without specifying concrete classes
    """
    def create_player(self, p_num, era): pass

class HumanFactory(PlayerFactory):
    """
    Returns a Human
    """
    def create_player(self, p_num, era):
        return Human(p_num, era)

class RandomAIFactory(PlayerFactory):
    """
    Returns a RandomAI
    """
    def create_player(self, p_num, era):
        return RandomAI(p_num, era)

class HeuristicAIFactory(PlayerFactory):
    """
    Returns a HeuristicAI
    """
    def create_player(self, p_num, era):
        return HeuristicAI(p_num, era)