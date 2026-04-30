import unittest
import numpy as np
from src.env.poker_env import PokerEnv, StateEnv

class TestPokerEnv(unittest.TestCase):
    def setUp(self):
        self.env = PokerEnv(n_players=4)

    def test_reset(self):
        self.env.reset()
        self.assertEqual(len(self.env.engine.hands), 4)
        self.assertEqual(len(self.env.engine.table), 5)
        assert(self.env.engine.table_mask == [False]*5)
        self.assertEqual(self.env.engine.round, 2)

    def test_step(self):
        self.env.reset()
        state = StateEnv(
            table=np.array(self.env.engine.table),
            phase=self.env.engine.round,
            private_cards=np.array(self.env.engine.hands),
            mask=np.array(self.env.engine.table_mask),
            reward=np.float64(0),
            done=False,
            agent_ranking=np.array([0, 1, 2, 3]),
            true_ranking=np.array([0, 1, 2, 3])
        )
        actions_positions = np.array([0, 1, 2, 3])
        actions_votes = np.array([1, 1, 1, 1])
        new_state = self.env.step(state, actions_positions, actions_votes)
        self.assertEqual(new_state.phase, 3) # should have advanced to the flop
    
    def test_vote_not_agreeing(self):
        self.env.reset()
        state = StateEnv(
            table=np.array(self.env.engine.table),
            phase=self.env.engine.round,
            private_cards=np.array(self.env.engine.hands),
            mask=np.array(self.env.engine.table_mask),
            reward=np.float64(0),
            done=False,
            agent_ranking=np.array([0, 1, 2, 3]),
            true_ranking=np.array([0, 1, 2, 3])
        )
        actions_positions = np.array([0, 1, 2, 3])
        actions_votes = np.array([1, 0, 1, 1]) # one player does not agree
        new_state = self.env.step(state, actions_positions, actions_votes)
        self.assertEqual(new_state.phase, 2) # should not have advanced to the flop
    
    def test_position_not_agreeing(self):
        self.env.reset()
        state = StateEnv(
            table=np.array(self.env.engine.table),
            phase=self.env.engine.round,
            private_cards=np.array(self.env.engine.hands),
            mask=np.array(self.env.engine.table_mask),
            reward=np.float64(0),
            done=False,
            agent_ranking=np.array([0, 1, 2, 3]),
            true_ranking=np.array([0, 1, 2, 3])
        )
        actions_positions = np.array([0, 1, 1, 3]) # two players do not agree on the position
        actions_votes = np.array([1, 1, 1, 1]) 
        new_state = self.env.step(state, actions_positions, actions_votes)
        self.assertEqual(new_state.phase, 2) # should not have advanced to the flop
    
    def test_full_run(self):
        self.env.reset()
        state = StateEnv(
            table=np.array(self.env.engine.table),
            phase=self.env.engine.round,
            private_cards=np.array(self.env.engine.hands),
            mask=np.array(self.env.engine.table_mask),
            reward=np.float64(0),
            done=False,
            agent_ranking=np.array([0, 1, 2, 3]),
            true_ranking=np.array([0, 1, 2, 3])
        )
        for _ in range(3): # we will go through all the phases
            self.assertFalse(state.done) # should not be done until the river
            actions_positions = np.array([0, 1, 2, 3])
            actions_votes = np.array([1, 1, 1, 1]) 
            state = self.env.step(state, actions_positions, actions_votes)
            self.assertEqual(state.phase, self.env.engine.round) # should have advanced to the next phase
            self.assertEqual(self.env.engine.table_mask, [True]*(state.phase+1) + [False]*(4-state.phase)) # should have the correct number of cards unmasked
        self.assertTrue(state.done) # should be done after the river
        print(state.reward)
