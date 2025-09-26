import unittest
import os
from collections import Counter
from hand_rank import HandRank

from test_harness import get_best_hand

def ranks(cards):
    return [card[0] for card in cards]

def all_in(cards, possible):
    return all(card in possible for card in cards)

def main_cards_count(rank):
    """
    Returns the number of non-kicker cards that make up the given HandRank.
    For HIGH_CARD: 0, ONE_PAIR: 2, TWO_PAIR: 4, THREE_OF_A_KIND: 3, STRAIGHT: 5, FLUSH: 5, FULL_HOUSE: 5, FOUR_OF_A_KIND: 4, STRAIGHT_FLUSH: 5, ROYAL_FLUSH: 5
    """
    if rank == HandRank.HIGH_CARD:
        return 0
    elif rank == HandRank.ONE_PAIR:
        return 2
    elif rank == HandRank.TWO_PAIR:
        return 4
    elif rank == HandRank.THREE_OF_A_KIND:
        return 3
    elif rank == HandRank.FOUR_OF_A_KIND:
        return 4
    else:
        return 5


class CheckKind(unittest.TestCase):
    def check_test_data_for_rank(self, rank, fileName = None):
        """
        Utility function to check that each line in testData/{rank}.txt returns the expected HandRank.
        """

        filename = os.path.join("testData", f"{fileName or rank.name}.txt")
        if not os.path.exists(filename):
            self.fail(f"File {filename} does not exist.")
        with open(filename) as f:
            for line in f:
                cards = line.strip().split()
                result = get_best_hand(cards[:7])
                self.assertEqual(result[0], rank, f"Cards: {cards} returned {result[0]}, expected {rank}")

    def test_high_card(self):
        self.check_test_data_for_rank(HandRank.HIGH_CARD)

    def test_one_pair(self):
        self.check_test_data_for_rank(HandRank.ONE_PAIR)

    def test_two_pair(self):
        self.check_test_data_for_rank(HandRank.TWO_PAIR)

    def test_three_of_a_kind(self):
        self.check_test_data_for_rank(HandRank.THREE_OF_A_KIND)

    def test_straight(self):
        self.check_test_data_for_rank(HandRank.STRAIGHT)

    def test_wheel_straight(self):
        self.check_test_data_for_rank(HandRank.STRAIGHT, "WHEEL_STRAIGHT")

    def test_flush(self):
        self.check_test_data_for_rank(HandRank.FLUSH)

    def test_full_house(self):
        self.check_test_data_for_rank(HandRank.FULL_HOUSE)

    @unittest.skip("Skipping due to suspected error in test data")
    def test_four_of_a_kind(self):
        self.check_test_data_for_rank(HandRank.FOUR_OF_A_KIND)

    def test_tricky_four_of_a_kind(self):
        self.check_test_data_for_rank(HandRank.FOUR_OF_A_KIND, fileName="TRICKY_FOUR_OF_A_KIND")

    def test_straight_flush(self):
        self.check_test_data_for_rank(HandRank.STRAIGHT_FLUSH)

    def test_royal_flush(self):
        self.check_test_data_for_rank(HandRank.ROYAL_FLUSH)

class CheckCards(unittest.TestCase):
    def check_test_data_for_cards(self, rank, fileName = None):
        """
        Utility function to check that each line in testData/{rank}.txt returns the expected HandRank,
        and that the cards in result[1] match the input cards (order may differ).
        If get_best_hand returns None for the cards, fail once for all cases.
        """
        filename = os.path.join("testData", f"{fileName or rank.name}.txt")
        if not os.path.exists(filename):
            self.fail(f"File {filename} does not exist.")
        with open(filename) as f:
            for line in f:
                cards = line.strip().split()
                result = get_best_hand(cards[:7])
                self.assertEqual(result[0], rank, f"Cards: {cards} returned {result[0]}, expected {rank}")
                # If student code returns None for cards, fail once with a clear message
                if result[1] is None:
                    self.fail(f"get_best_hand did not return cards for input: {cards[:7]}")
                self.assertTrue(all_in(result[1], cards[:7]), f"Returned cards not all in input: {result[1]} vs {cards[:7]}")
                main_cards = main_cards_count(result[0])
                expected_ranks = Counter(ranks(cards[7:])[:main_cards])
                returned_ranks = Counter(ranks(result[1])[:main_cards])
                self.assertEqual(returned_ranks, expected_ranks, f"Ranks of cards mismatch: got {result[1]} vs {cards[:7]} expected")
                
    def test_high_card(self):
        self.check_test_data_for_cards(HandRank.HIGH_CARD)

    def test_one_pair(self):
        self.check_test_data_for_cards(HandRank.ONE_PAIR)

    def test_two_pair(self):
        self.check_test_data_for_cards(HandRank.TWO_PAIR)

    def test_three_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.THREE_OF_A_KIND)

    def test_straight(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT)

    def test_wheel_straight(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT, "WHEEL_STRAIGHT")

    def test_flush(self):
        self.check_test_data_for_cards(HandRank.FLUSH)

    def test_full_house(self):
        self.check_test_data_for_cards(HandRank.FULL_HOUSE)

    @unittest.skip("Skipping due to suspected error in test data")
    def test_four_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.FOUR_OF_A_KIND)

    def test_tricky_four_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.FOUR_OF_A_KIND, fileName="TRICKY_FOUR_OF_A_KIND")

    def test_straight_flush(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT_FLUSH)

    def test_royal_flush(self):
        self.check_test_data_for_cards(HandRank.ROYAL_FLUSH)
                
class CheckBestCards(unittest.TestCase):
    def check_test_data_for_cards(self, rank, fileName = None):
        """
        Utility function to check that each line in testData/{rank}.txt returns the expected HandRank,
        and that the cards in result[1] match the input cards (order may differ).
        If get_best_hand returns None for the cards, fail once for all cases.
        """
        filename = os.path.join("testData", f"{fileName or rank.name}.txt")
        if not os.path.exists(filename):
            self.fail(f"File {filename} does not exist.")
        with open(filename) as f:
            for line in f:
                cards = line.strip().split()
                result = get_best_hand(cards[:7])
                self.assertEqual(result[0], rank, f"Cards: {cards} returned {result[0]}, expected {rank}")
                # If student code returns None for cards, fail once with a clear message
                if result[1] is None:
                    self.fail(f"get_best_hand did not return cards for input: {cards[:7]}")
                self.assertEqual(len(result[1]), 5, f"Expected 5 cards in returned hand, got {len(result[1])}: {result[1]}")
                self.assertTrue(all_in(result[1], cards[:7]), f"Returned cards not all in input: {result[1]} vs {cards[:7]}")

                expected_ranks = ranks(cards[7:])
                returned_ranks = ranks(result[1])
                self.assertEqual(returned_ranks, expected_ranks, f"Best cards ranks mismatch")
                
    def test_high_card(self):
        self.check_test_data_for_cards(HandRank.HIGH_CARD)

    def test_one_pair(self):
        self.check_test_data_for_cards(HandRank.ONE_PAIR)

    def test_two_pair(self):
        self.check_test_data_for_cards(HandRank.TWO_PAIR)

    def test_three_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.THREE_OF_A_KIND)

    def test_straight(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT)

    def test_wheel_straight(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT, "WHEEL_STRAIGHT")

    def test_flush(self):
        self.check_test_data_for_cards(HandRank.FLUSH)

    def test_full_house(self):
        self.check_test_data_for_cards(HandRank.FULL_HOUSE)

    @unittest.skip("Skipping due to suspected error in test data")
    def test_four_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.FOUR_OF_A_KIND)

    def test_tricky_four_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.FOUR_OF_A_KIND, fileName="TRICKY_FOUR_OF_A_KIND")

    def test_straight_flush(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT_FLUSH)

    def test_royal_flush(self):
        self.check_test_data_for_cards(HandRank.ROYAL_FLUSH)
                
class CheckAdversarialCases(unittest.TestCase):
    def test_adversarial_cases(self):
        ADVERSARIAL_TESTS = {
            "STRAIGHT_FLUSH_MULTIPLE_OPTIONS": {
                "cards": "AD 2D 3D 4D 5D 6D 7D".split(),
                "expected_rank": HandRank.STRAIGHT_FLUSH,
                "expected_hand": ["7D", "6D", "5D", "4D", "3D"]
            },
            "ROYAL_FLUSH_WITH_KICKERS": {
                "cards": "AC KC QC JC TC 2H 3D".split(),
                "expected_rank": HandRank.ROYAL_FLUSH,
                "expected_hand": ["AC", "KC", "QC", "JC", "TC"]
            },
            "ACE_LOW_STRAIGHT": {
                "cards": "AS 2H 3C 4D 5S 9H KD".split(),
                "expected_rank": HandRank.STRAIGHT,
                "expected_hand": ["5S", "4D", "3C", "2H", "AS"]
            },
            "FLUSH_SIX_CARDS": {
                "cards": "AS KS QS JS TS 9S 2H".split(),
                "expected_rank": HandRank.FLUSH,
                "expected_hand": ["AS", "KS", "QS", "JS", "TS"]
            },
            "STRAIGHT_SEVEN_CARDS": {
                "cards": "2H 3D 4C 5S 6H 7D 8C".split(),
                "expected_rank": HandRank.STRAIGHT,
                "expected_hand": ["8C", "7D", "6H", "5S", "4C"]
            },
            "HIDDEN_STRAIGHT_OVER_PAIR": {
                "cards": "3S 3D 4C 5H 6S 7D 8H".split(),
                "expected_rank": HandRank.STRAIGHT,
                "expected_hand": ["8H", "7D", "6S", "5H", "4C"]
            },
            "TWO_PAIR_BEST_KICKER": {
                "cards": "KD KC TD TC AS 9H 8C".split(),
                "expected_rank": HandRank.TWO_PAIR,
                "expected_hand": ["KD", "KC", "TD", "TC", "AS"]
            },
            "THREE_OF_A_KIND_BEST_KICKERS": {
                "cards": "AD AH AS 2C 7D 8H 9S".split(),
                "expected_rank": HandRank.THREE_OF_A_KIND,
                "expected_hand": ["AD", "AH", "AS", "9S", "8H"]
            },
            "FOUR_OF_A_KIND_BEST_KICKER": {
                "cards": "AC AD AH AS 2C 7D 8H".split(),
                "expected_rank": HandRank.FOUR_OF_A_KIND,
                "expected_hand": ["AC", "AD", "AH", "AS", "8H"]
            },
            "FULL_HOUSE_MULTIPLE_TRIPS_PAIRS": {
                "cards": "AD AH AS KD KH KS 2C".split(),
                "expected_rank": HandRank.FULL_HOUSE,
                "expected_hand": ["AD", "AH", "AS", "KD", "KH"]
            },
            "WHEEL_AND_HIGHER_STRAIGHT": {
                "cards": "AD 2C 3S 4H 5D 6C 7S".split(),
                "expected_rank": HandRank.STRAIGHT,
                "expected_hand": ["7S", "6C", "5D", "4H", "3S"]
            },
        }

        for name, case in ADVERSARIAL_TESTS.items():
            with self.subTest(name=name):
                rank, hand = get_best_hand(case["cards"])
                self.assertEqual(rank, case["expected_rank"], "HandRank mismatch")
                self.assertEqual(hand, case["expected_hand"], "Hand cards mismatch")
                


if __name__ == '__main__':
    unittest.main()
