from env.poker_env import PokerEnv, StateEnv


class Agent:
    def __init__(self, n_players):
        self.n_players = n_players
        self.env = PokerEnv(n_players)

    def train(self):
        pass
    def ppo_update(self):
        pass