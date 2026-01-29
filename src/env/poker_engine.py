import random
from collections import Counter

class PokerEngine:
    def __init__(self, n_players):
        self.deck = self.create_deck()
        self.n_players = n_players
        self.hands = {player: [] for player in range(n_players)}
        self.table = []
        self.round = 0

    def create_deck(self):
        suits = ['Heart', 'Diamond', 'Club', 'Spade']
        ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]# 11 = Jack, 12 = Queen, 13 = King
        return [(rank, suit) for suit in suits for rank in ranks]
    
    def draw_hand(self):
        hands = []
        random.shuffle(self.deck)
        for _ in range(self.n_players):
            individual_hands = [self.deck.pop() for _ in range(2)]
            hands.append(individual_hands)
        return hands
    
    def deal_table(self):
        if self.round == 0:
            # Flop
            self.table.extend([self.deck.pop() for _ in range(3)])
        elif self.round in [1, 2]:
            # Turn or River
            self.table.append(self.deck.pop())
        self.round += 1
    
    def reset(self):
        self.deck = self.create_deck()
        self.hands = {player: [] for player in range(self.n_players)}
        self.table = []
        self.round = 0
    
    def evaluate_hand(self, hand):
        total_deck = hand + self.table.copy()
        suits = [suit for rank, suit in total_deck]
        ranks = [rank for rank, suit in total_deck]
        rank_count = Counter(ranks)
        is_flush = any(suits.count(suit) >= 5 for suit in set(suits))
        flush_cards = []
        if is_flush:
            flush_suit = max(set(suits), key=suits.count)
            flush_cards = [card for card in total_deck if card[1] == flush_suit]
            if 1 in [card[0] for card in flush_cards]:
                flush_cards.append((14, flush_suit))  # Ace can be high
            flush_cards = sorted(flush_cards, key=lambda x: x[0], reverse=True)[:5]
        is_straight, max_card = self.check_straight(ranks)
        max_card = max(max_card, flush_cards[0][0]) if flush_cards else max_card
        if is_flush and is_straight:
            return ("Straight Flush",0, (max_card, 0))
        elif 4 in rank_count.values():
            return ("Four of a Kind", 1, (rank_count.most_common(1)[0][0], 0))
        elif 3 in rank_count.values() and 2 in rank_count.values():
            return ("Full House",2, [ranks for ranks, count in rank_count.most_common(2)][0])
        elif is_flush:
            return ("Flush",3, (max_card, 0))
        elif is_straight:
            return ("Straight",4, (max_card, 0))
        elif 3 in rank_count.values():
            return ("Three of a Kind", 5, (rank_count.most_common(1)[0][0], 0))
        elif list(rank_count.values()).count(2) >= 2:
            return ("Two Pair",6, [ranks for ranks, count in rank_count.most_common(2)])
        elif 2 in rank_count.values():
            return ("One Pair", 7, (rank_count.most_common(1)[0][0], 0))
        else:
            return ("High Card", 8, (max(ranks), 0)) #mettre la somme plutot ???
    
    def check_straight(self, ranks):
        """Cheks if there is 5 cards following each other in ranks"""
        unique_ranks = sorted(set(ranks))
        if 1 in unique_ranks:
            unique_ranks.append(14)  # Ace can be high
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i + 4] - unique_ranks[i] == 4:
                return True, unique_ranks[i + 4] # Return highest card in straight
        return False, 0
    
    def rank_hands(self):
        rankings = {}
        list_evalutations = []
        for player, hand in self.hands.items():
            list_evalutations.append(self.evaluate_hand(hand))
        list_player = list(self.hands.keys())
        sorted_evaluations = zip(list_player, list_evalutations)

        return rankings
    
