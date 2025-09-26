from collections import Counter
from itertools import combinations
from hand_rank import HandRank

# It's helpful to have mappings for ranks to values for comparisons.
# Ace can be high (14) or low (1), which we'll handle in straight checks.
RANK_TO_VALUE = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
}
VALUE_TO_RANK = {v: k for k, v in RANK_TO_VALUE.items()}

class Card:
    """
    A class to represent a playing card.
    
    Attributes:
        rank (str): The rank of the card (e.g., 'A', 'K', 'T').
        suit (str): The suit of the card (e.g., 'S', 'H').
        value (int): The numerical value of the rank for comparisons. 
    """
    def __init__(self, card_str):
        """
        Initializes a Card from a 2-character string (e.g., 'KH').
        """
        self.rank = card_str[0]
        self.suit = card_str[1]
        self.value = RANK_TO_VALUE[self.rank]
        self.card_str = card_str

    def __repr__(self):
        """
        String representation of the card.
        """
        return self.card_str

    def __lt__(self, other):
        """
        Compare cards based on their value.
        """
        return self.value < other.value

    def __eq__(self, other):
        """
        Check if two cards are equal in value and suit.
        """
        return self.value == other.value and self.suit == other.suit

def parse_cards(card_strings):
    """
    Parses a list of card strings into a list of Card objects.
    """
    return sorted([Card(cs) for cs in card_strings], reverse=True)

# The functions below will be implemented in the next steps.
# They are placeholders for now.

def find_best_hand(card_strings):
    """
    Finds the best possible 5-card poker hand from a list of 7 cards.
    This is the main entry point for the analysis.
    """
    all_cards = parse_cards(card_strings)
    
    # Check for hands in descending order of rank.
    # Each checker function will return a tuple of (HandRank, [Card, ...]) or None.
    if (hand := find_royal_flush(all_cards)): return hand
    if (hand := find_straight_flush(all_cards)): return hand
    if (hand := find_four_of_a_kind(all_cards)): return hand
    if (hand := find_full_house(all_cards)): return hand
    if (hand := find_flush(all_cards)): return hand
    if (hand := find_straight(all_cards)): return hand
    if (hand := find_three_of_a_kind(all_cards)): return hand
    if (hand := find_two_pair(all_cards)): return hand
    if (hand := find_one_pair(all_cards)): return hand
    
    # If no other hand is found, the best hand is determined by the highest card.
    return find_high_card(all_cards)

# --- Placeholder Hand-Checking Functions ---
# These will be implemented in the next step. They analyze the 7 cards
# and return the best 5-card hand of that type if found.

def _get_groups(cards):
    """
    A helper function to group cards by rank and count them.
    Returns a list of tuples, where each tuple is (count, rank_value, cards).
    The list is sorted by count (descending) and then rank_value (descending).
    e.g., [(3, 14, [AS, AD, AH]), (2, 10, [TC, TH]), ...]
    """
    if not cards:
        return []
    
    # Group cards by rank value
    card_groups = {}
    for card in cards:
        if card.value not in card_groups:
            card_groups[card.value] = []
        card_groups[card.value].append(card)
    
    # Create a list of (count, rank_value, cards)
    groups = [(len(group), value, group) for value, group in card_groups.items()]
    
    # Sort by count, then by rank value, both descending
    groups.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return groups

def find_royal_flush(cards):
    """Checks for A, K, Q, J, T of the same suit."""
    # A royal flush is just a special case of a straight flush.
    # We can reuse that logic and check the rank of the high card.
    result = find_straight_flush(cards)
    if result and result[1][0].value == 14: # Check if the high card is an Ace
        return HandRank.ROYAL_FLUSH, result[1]
    return None

def find_straight_flush(cards):
    """Checks for 5 cards in sequence of the same suit."""
    # First, find potential flushes
    suits = Counter(c.suit for c in cards)
    for suit, count in suits.items():
        if count >= 5:
            # If we have a flush, check if those cards also form a straight
            flush_cards = sorted([c for c in cards if c.suit == suit], reverse=True)
            # The find_straight logic can be reused on this subset of cards
            straight_flush = find_straight(flush_cards)
            if straight_flush:
                return HandRank.STRAIGHT_FLUSH, straight_flush[1]
    return None

def find_four_of_a_kind(cards):
    """Checks for four cards of the same rank."""
    groups = _get_groups(cards)
    if groups and groups[0][0] == 4:
        four_of_a_kind = groups[0][2]
        # Find the highest kicker from the remaining cards
        remaining_cards = [c for c in cards if c not in four_of_a_kind]
        kicker = remaining_cards[0]
        return HandRank.FOUR_OF_A_KIND, four_of_a_kind + [kicker]
    return None

def find_full_house(cards):
    """Checks for three of a kind and a pair."""
    groups = _get_groups(cards)
    if len(groups) >= 2 and groups[0][0] == 3 and groups[1][0] >= 2:
        three_of_a_kind = groups[0][2]
        pair = groups[1][2][:2]
        return HandRank.FULL_HOUSE, three_of_a_kind + pair
    return None

def find_flush(cards):
    """Checks for five cards of the same suit."""
    suits = Counter(c.suit for c in cards)
    for suit, count in suits.items():
        if count >= 5:
            flush_cards = sorted([c for c in cards if c.suit == suit], reverse=True)
            return HandRank.FLUSH, flush_cards[:5]
    return None

def find_straight(cards):
    """Checks for five cards in sequence."""
    unique_cards = []
    seen_values = set()
    for card in cards:
        if card.value not in seen_values:
            unique_cards.append(card)
            seen_values.add(card.value)
    
    # Handle Ace-low straight (A, 2, 3, 4, 5)
    if all(v in seen_values for v in [14, 2, 3, 4, 5]):
        straight_cards = [c for c in unique_cards if c.value in [5, 4, 3, 2]]
        ace = [c for c in unique_cards if c.value == 14][0]
        return HandRank.STRAIGHT, straight_cards + [ace]

    # Check for other straights
    for i in range(len(unique_cards) - 4):
        # Check if the next 4 cards form a sequence
        is_straight = True
        for j in range(4):
            if unique_cards[i+j].value != unique_cards[i+j+1].value + 1:
                is_straight = False
                break
        if is_straight:
            return HandRank.STRAIGHT, unique_cards[i:i+5]
            
    return None

def find_three_of_a_kind(cards):
    """Checks for three cards of the same rank."""
    groups = _get_groups(cards)
    if groups and groups[0][0] == 3:
        three_of_a_kind = groups[0][2]
        remaining_cards = [c for c in cards if c not in three_of_a_kind]
        kickers = remaining_cards[:2]
        return HandRank.THREE_OF_A_KIND, three_of_a_kind + kickers
    return None

def find_two_pair(cards):
    """Checks for two different pairs."""
    groups = _get_groups(cards)
    if len(groups) >= 2 and groups[0][0] == 2 and groups[1][0] == 2:
        pair1 = groups[0][2]
        pair2 = groups[1][2]
        remaining_cards = [c for c in cards if c not in pair1 and c not in pair2]
        kicker = remaining_cards[0]
        return HandRank.TWO_PAIR, pair1 + pair2 + [kicker]
    return None

def find_one_pair(cards):
    """Checks for one pair."""
    groups = _get_groups(cards)
    if groups and groups[0][0] == 2:
        pair = groups[0][2]
        remaining_cards = [c for c in cards if c not in pair]
        kickers = remaining_cards[:3]
        return HandRank.ONE_PAIR, pair + kickers
    return None

def find_high_card(cards):
    """Finds the high card hand (top 5 cards)."""
    # By definition, the cards are already sorted high-to-low.
    return HandRank.HIGH_CARD, cards[:5]

  