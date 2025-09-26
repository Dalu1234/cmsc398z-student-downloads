from hand_rank import HandRank
from poker_analysis import find_best_hand


def get_best_hand(cards):
    """
    Given a list of 7 cards, returns a tuple (HandRank, cards_used).
    cards_used is either None (if returning cards has not been implemented) 
    or a list of 5 cards that make up the best hand. If you want to be able to 
    compare two hands to see which one is stronger, the returned hands should be 
    listed from most significant to least significant card. 

    Args:
        cards (list of str): List of 7 card strings, e.g. ['KC', 'KS', 'QH', 'TD', '7S', '2C', '3D']

    Returns:
        tuple: (HandRank, None or list of 5 card strings)

    Example:
        >>> get_best_hand(['KC', 'KS', 'QH', 'TD', '7S', '2C', '3D'])
        (<HandRank.ONE_PAIR: 1>, ['KC', 'KS', 'QH', 'TD', '7S'])
    """
    # Call the main analysis function from poker_analysis.py
    hand_rank, best_cards = find_best_hand(cards)
    
    # Convert the list of Card objects back to a list of strings for the test harness
    card_strings = [card.card_str for card in best_cards]
    
    return hand_rank, card_strings
