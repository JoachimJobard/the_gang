import unittest
from src.env.poker_engine import PokerEngine
class TestPokerEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PokerEngine(n_players=2)

    def test_create_deck(self):
        deck = self.engine.create_deck()
        self.assertEqual(len(deck), 52)
        self.assertIn((0, 'Heart'), deck)
        self.assertIn((12, 'Spade'), deck)
    
    def test_draw_hands(self):
        self.engine.draw_hands()
        for player in range(self.engine.n_players):
            self.assertEqual(len(self.engine.hands[player]), 2)

    def test_deal_table(self):
        self.engine.deal_table()
        self.assertEqual(len(self.engine.table), 3)  # Flop
        self.engine.deal_table()
        self.assertEqual(len(self.engine.table), 4)  # Turn
        self.engine.deal_table()
        self.assertEqual(len(self.engine.table), 5)  # River

    def test_reset(self):
        self.engine.draw_hands()
        self.engine.deal_table()
        self.engine.reset()
        self.assertEqual(len(self.engine.deck), 52)
        self.assertEqual(len(self.engine.table), 0)
    
    def test_evaluation_hand(self):
        self.engine.reset()
        self.engine.draw_hands()
        self.engine.deal_table()
        self.engine.deal_table()
        self.engine.deal_table()
        print(self.engine.hands)
        print(self.engine.table)
        list_rankings = self.engine.rank_hands()
        print(list_rankings)
    
    def test_check_straight(self):
        hand = [(0, 'Heart'), (1, 'Diamond')]
        self.engine.table = [(2, 'Club'), (3, 'Spade'), (4, 'Heart')]
        is_straight, straight_hand = self.engine.check_straight(hand + self.engine.table)
        self.assertTrue(is_straight)
        self.assertEqual(straight_hand, [(0, 'Heart'), (1, 'Diamond'), (2, 'Club'), (3, 'Spade'), (4, 'Heart')])

    def test_straight_flush(self):
        self.engine.reset()
        self.engine.draw_hands()
        hand = [(0, 'Heart'), (12, 'Heart')]
        self.engine.hands[0] = hand
        self.engine.table = [(1, 'Heart'), (2, 'Heart'), (3, 'Heart'), (6, 'Space'), (7, 'Diamond')]
        list_hands = self.engine.rank_hands()
        print(list_hands)
    
    def test_extensive(self):
        for _ in range(10000):
            self.engine.reset()
            self.engine.draw_hands()
            for _ in range(3):
                self.engine.deal_table()
            _ = self.engine.rank_hands()