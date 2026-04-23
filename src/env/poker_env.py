from typing import NamedTuple

import numpy as np

from env.poker_engine import PokerEngine
from utils.loss_functions import kendall_tau_b

class StateEnv(NamedTuple):
    table: np.ndarray
    phase: int
    private_cards: np.ndarray
    mask: np.ndarray
    reward: np.float64
    done: bool
    agent_ranking: np.ndarray
    true_ranking: np.ndarray

class PokerEnv:
    def __init__(self, n_players: int):
        self.n_players = n_players
        self.engine = PokerEngine(n_players)
    
    def reset(self):
        self.engine.reset()
    
    def step(self, state: StateEnv, actions_positions: np.ndarray, actions_votes: np.ndarray) -> StateEnv:
        # TODO: implement the step logic. should return the new state, rewards, observations(idk how), done boolean, etc. for each player. also should handle the logic of advancing the phase of the game (flop, turn, river) based on the actions taken by the players.
        # 2 cases: either we switch phase bc unique ranking and everyone is agreeing to go next, or we don't bc the conditions to do so are not met.
        if self.check_unique_position(actions_positions) and np.all(actions_votes == 1):
            self.engine.deal_table() # advance phase
            done = self.engine.round == 5 # if we have dealt the river, the game
            reward = np.float64(self.compute_rewards(state)) if done else np.float64(0)
            new_state = StateEnv(
                table=np.array(self.engine.table),
                phase=self.engine.round,
                private_cards=np.array(self.engine.hands),
                mask=np.array(self.engine.table_mask),
                reward=reward,
                done=done,
                agent_ranking=state.agent_ranking,
                true_ranking=state.true_ranking
            )
            return new_state
        else:

            new_state = StateEnv(
                table=np.array(self.engine.table),
                phase=self.engine.round,
                private_cards=np.array(self.engine.hands),
                mask=np.array(self.engine.table_mask),
                reward=np.float64(0),
                done=False,
                agent_ranking=state.agent_ranking,
                true_ranking=state.true_ranking
            )
            return new_state
        
    def compute_rewards(self, state: StateEnv) -> np.ndarray:
        # Everyone is supposed to have agreed, we hence only check if the hands ranking are correctly assigned. The reward will be 1 if the hand ranking is correct, and kendall tau b if not.
        agent_ranking = state.agent_ranking
        true_ranking = state.true_ranking
        reward = kendall_tau_b(agent_ranking, true_ranking)
        return reward
    
    @staticmethod
    def check_unique_position(action_positions: np.ndarray) -> bool:
        if len(action_positions) != len(set(action_positions)):
            return False
        return True
    

