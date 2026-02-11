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
        ranks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # careful! for convinience, 0 = 2, 1 = 3, ..., 9 = Jack, 10 = Queen, 11 = King, 12 = Ace
        return [(rank, suit) for suit in suits for rank in ranks]
    
    def draw_hands(self):
        hands = []
        random.shuffle(self.deck)
        for player in range(self.n_players):
            individual_hands = [self.deck.pop() for _ in range(2)]
            self.hands[player] = individual_hands
    
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
        is_straight, straight_hand = self.check_straight(total_deck)
        # format is (name hand, ranking in hand types, tiebreak determination (higher is better))
        if is_flush and is_straight: #straight flush
            if set(straight_hand).issubset(set(flush_cards)):
                return (8, sum(rank for rank, suit in straight_hand)) # here we can just sum the ranks of the straight cards, since the highest card will have more weight than the others
        elif 4 in rank_count.values(): #four of a kind
            return (7, (rank_count.most_common(1)[0][0])) #here just the most common is enough
        elif 3 in rank_count.values() and 2 in rank_count.values():#full house
            full_house_ranks = [ranks for ranks, count in rank_count.most_common(2) if count >= 2]
            full_house_ranks[0] *= 13 # give more weight to the three of a kind than the pair
            return (6, sum(full_house_ranks)) # here we can just sum the two ranks, since the three of a kind will have more weight than the pair
        elif is_flush: #flush
            return (5,sum(sorted(flush_cards, key=lambda x: x[0], reverse=True)[:5][0])) # here we can just sum the ranks of the flush cards, since the highest card will have more weight than the others
        elif is_straight: #straight
            return (4, sum([rank for rank, suit in straight_hand])) # here we can just sum the ranks of the straight cards, since the highest card will have more weight than the others
        elif 3 in rank_count.values(): #three of a kind
            return (3, (rank_count.most_common(1)[0][0])) #no need to sum here
        elif list(rank_count.values()).count(2) >= 2:#two pair
            double_pair_ranks = [ranks for ranks, count in rank_count.most_common(2) if count == 2]
            return (2, sum(double_pair_ranks)+ max(set(ranks) - set(double_pair_ranks))) #we add the max card that is not in the pairs
        elif 2 in rank_count.values():#one pair
            pair_card_rank = rank_count.most_common(1)[0][0]
            return (1, pair_card_rank*13 + max(set(ranks) - {pair_card_rank})) #we give more weight to the pair than the highest card that is not in the pair
        else:#high card
            return (0, (max(ranks)))
    
    def check_straight(self, deck):
        """Cheks if there is 5 cards following each other in ranks"""
        sorted_deck = sorted(set(deck), key=lambda x: x[0])
        for i in range(len(sorted_deck) - 3): # minus 3 so we check for the ace if in the end
            if (sorted_deck[(i + 4)%7][0] - sorted_deck[i][0])%14 == 4: #in case of ace, will return 4
                return True, sorted_deck[i:(i+5)%7] # Return highest card in straight
        return False, []
    
    def rank_hands(self):
        list_evalutations = []
        for player, hand in self.hands.items():
            list_evalutations.append((player, self.evaluate_hand(hand)))
        list_evalutations.sort(key=lambda x: x[1]) #lexicographical sort, first by hand type, then by tiebreaker
        return [(player, score) for player, score in list_evalutations] #we only return the rankings of the players

#SIX SEVENNNNNNNNNN
    