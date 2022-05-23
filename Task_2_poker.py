#  Задача:
#  написать функцию, которая берёт на вход набор карт (строго говоря, 7 карт, но на самом деле, это не важно)
#  и возвращает старшую пятикарточную комбинацию в этом наборе.
#
#  Обозначения:
#  2,3,4,5,6,7,8,9,10,11,12,13,14 - 2,3,4,5,6,7,8,9,10,J,Q,K,A соответственно
#  'H', 'S', 'C', 'D' - Hearts, Spades, Clubs, Diamonds соответственно


from collections import Counter
from itertools import combinations
# import random


class SevenCards:
    def __init__(self, k_c=None):
        self.list_of_cards = k_c or []

        if not SevenCards.check_quantity(k_c=self.list_of_cards, quantity=7):
            raise RuntimeError(f"Invalid quantity of cards: {len(set(self.list_of_cards))}!")

        if not SevenCards.check_duplicates(k_c=self.list_of_cards):
            raise RuntimeError(f"Card deck has duplicates: {self.list_of_cards}!")

        if not SevenCards.check_card_attributes(k_c=self.list_of_cards):
            raise RuntimeError("Invalid card attributes!")

        if not SevenCards.check_nominal(k_c=self.list_of_cards):
            raise ValueError("Invalid value of card nominal!")

        if not SevenCards.check_suit(k_c=self.list_of_cards):
            raise ValueError("Invalid value of card suit!")

    @staticmethod
    def check_quantity(k_c: list, quantity: int) -> bool:
        return len(set(k_c)) == quantity

    @staticmethod
    def check_duplicates(k_c: list) -> bool:
        return True

    @staticmethod
    def check_card_attributes(k_c: list) -> bool:
        def check_card(card: tuple) -> bool:
            return len(card) == 2 and type(card[0]) == int and type(card[1]) == str

        return False not in list(map(check_card, k_c))

    @staticmethod
    def check_nominal(k_c: list) -> bool:
        return False not in [True if c[0] in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14) else False for c in k_c]

    @staticmethod
    def check_suit(k_c: list) -> bool:
        return False not in [True if c[1] in ('H', 'S', 'C', 'D') else False for c in k_c]


def define_winner_hand(scs: SevenCards) -> tuple:
    if not isinstance(scs, SevenCards):
        raise TypeError("В функцию define_winner_hand передан аргумент некорректного типа!")
    if not scs.list_of_cards:
        raise ValueError("Содержимое аргумента, переданного в функцию define_winner_hand не корректно!")

    all_combo_in_hand = list(combinations(scs.list_of_cards, 5))

    ordered_all_combo_in_hand_by_suits = [sorted(hnd, key=lambda crd: crd[1]) for hnd in all_combo_in_hand]

    hands_scores = score_for_a_combination(ordered_all_combo_in_hand_by_suits)

    max_score = max(hands_scores)

    ind_max = [i for i, s in enumerate(hands_scores) if s == max_score]

    hand_max = [sorted(all_combo_in_hand[i], key=lambda crd: crd[0]) for i in ind_max]

    if len(hand_max) == 1:
        win_hand = hand_max[0]
    else:
        win_hand = compare_of_equal_combos(hand_max, max_score)

    return win_hand, max_score


def score_combo_with_same_suit(shnd: list) -> int:
    shnd = sorted(shnd, key=lambda crd: crd[0])
    if shnd[4][0] - shnd[0][0] == 4:
        if shnd[0][0] == 10:
            return 10  # Royal flush
        else:
            return 9  # Straight flush
    else:
        if 14 in shnd and shnd[3][0] - shnd[0][0] == 3 and shnd[0] == 2:
            return 5  # Straight
        else:
            return 6  # Flush


def score_combo_without_same_suit(shnd: list) -> int:
    shnd = sorted(shnd, key=lambda crd: crd[0])
    sorted_list_of_values = [shnd[n][0] for n in range(0, 5)]
    ace = 14

    if sorted_list_of_values[4] - sorted_list_of_values[0] == 4 and len(sorted_list_of_values) == len(set(sorted_list_of_values)):
        return 5  # Straight
    elif ace in sorted_list_of_values and sorted_list_of_values[3] - sorted_list_of_values[0] == 3 and sorted_list_of_values[0] == 2:
        return 5  # Straight
    else:
        counter_values = Counter(sorted_list_of_values)
        values = list(counter_values.values())

        if 4 in values:
            return 8  # Four of a kind
        elif 3 in values:
            if 2 in values:
                return 7  # Full house
            else:
                return 4  # Three of a kind
        elif 2 in values:
            vc = values.count(2)
            if vc == 2:
                return 3  # Two pairs
            else:
                return 2  # Pair
        else:
            return 1  # Highcard


def score_for_a_combination(ordered_acih_by_suits: list) -> list:
    if not isinstance(ordered_acih_by_suits, list):
        raise TypeError("В функцию scoring_for_a_combination передан аргумент некорректного типа!")
    if not ordered_acih_by_suits:
        raise ValueError("Содержимое аргумента, переданного в функцию scoring_for_a_combination не корректно!")

    hands_scores = [score_combo_with_same_suit(shnd) if shnd[0][1] == shnd[4][1] else score_combo_without_same_suit(shnd) for shnd in ordered_acih_by_suits]
    return hands_scores


def clean_of_card_suit(hand_max: list) -> list:
    if not isinstance(hand_max, list):
        raise TypeError("В функцию clean_of_card_suit передан аргумент некорректного типа!")
    if not hand_max:
        raise ValueError("Содержимое аргумента, переданного в функцию clean_of_card_suit не корректно!")

    return [[hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]] for hand in hand_max]


def find_win_hand(hand_max_without_suit: list, hand_max: list, max_score: int) -> list:
    if not isinstance(hand_max_without_suit, list) or not isinstance(hand_max, list) or not isinstance(max_score, int):
        raise TypeError("В функцию find_win_hand передан аргумент некорректного типа!")
    if not hand_max_without_suit or not hand_max or not max_score:
        raise ValueError("Содержимое аргумента, переданного в функцию find_win_hand не корректно!")

    if max_score == 9 or max_score == 5:
        winner = 0
        winner_hand_without_suit = []
        for hand in hand_max_without_suit:
            if hand[-1] > winner:
                winner = hand[-1]
                winner_hand_without_suit = hand
        windex = hand_max_without_suit.index(winner_hand_without_suit)
        win_hand = hand_max[windex]

    else:
        winner_hand_without_suit = max(hand_max_without_suit)
        windex = hand_max_without_suit.index(winner_hand_without_suit)
        win_hand = hand_max[windex]

    return win_hand


def change_for_rare_case(hand_max_without_suit: list) -> list:
    for hand in hand_max_without_suit:
        if 14 in hand and 2 in hand:
            hand.insert(0, 14)
            hand.pop(5)
    return hand_max_without_suit


def change_of_a_kind(hand_max_without_suit: list) -> list:
    for hand in hand_max_without_suit:
        value_of_the_same = hand[2]
        ind = hand_max_without_suit.index(hand)
        for i in range(3):
            hand_max_without_suit[ind].remove(value_of_the_same)
    return hand_max_without_suit


def check_equals_for_fullhouse(hand_max_without_suit: list, hand_max: list) -> list:
    nominals = [[hand[0], hand[4]] if hand.count(hand[0]) == 3 else [hand[4], hand[0]] for hand in
                hand_max_without_suit]
    tmp_three = [n[0] for n in nominals]
    max_of_three = max(tmp_three)
    tmp_hand = [nominals[i] for i in range(len(nominals)) if nominals[i][0] == max_of_three]
    count_list = [i for i, s in enumerate(nominals) if nominals[i][0] == max_of_three]
    win_hand = [hand_max[count_list[i]] if tmp_hand[i][1] >= tmp_hand[i + 1][1] else hand_max[count_list[i + 1]] for
                i in range(len(tmp_hand) - 1)]
    return win_hand


def compare_of_equal_combos(hand_max: list, max_score: int) -> list:
    if not isinstance(hand_max, list) or not isinstance(max_score, int):
        raise TypeError("В функцию compare_of_equal_combos передан аргумент некорректного типа!")
    if not hand_max or not max_score:
        raise ValueError("Содержимое аргумента, переданного в функцию clean_of_card_suit не корректно!")

    win_hand = []

    if max_score == 10:
        pass

    if max_score == 9:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        hand_max_without_suit = change_for_rare_case(hand_max_without_suit)
        win_hand = find_win_hand(hand_max_without_suit, hand_max, max_score)

    if max_score == 8:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        hand_max_without_suit = change_of_a_kind(hand_max_without_suit)
        win_hand = find_win_hand(hand_max_without_suit, hand_max, max_score)

    if max_score == 7:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        win_hand = check_equals_for_fullhouse(hand_max_without_suit, hand_max)

    if max_score == 6:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        win_hand = find_win_hand(hand_max_without_suit, hand_max, max_score)

    if max_score == 5:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        hand_max_without_suit = change_for_rare_case(hand_max_without_suit)
        win_hand = find_win_hand(hand_max_without_suit, hand_max, max_score)

    if max_score == 4:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        hand_max_without_suit = change_of_a_kind(hand_max_without_suit)
        win_hand = find_win_hand(hand_max_without_suit, hand_max, max_score)

    if max_score == 3:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        win_hand = find_win_hand(hand_max_without_suit, hand_max, max_score)

    if max_score == 2:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        win_hand = find_win_hand(hand_max_without_suit, hand_max, max_score)

    if max_score == 1:
        hand_max_without_suit = clean_of_card_suit(hand_max)
        win_hand = find_win_hand(hand_max_without_suit, hand_max, max_score)

    return win_hand


# all_cards = tuple([(x, y) for x in range(2, 15) for y in ('H', 'S', 'C', 'D')])
# kit_cards = random.sample(all_cards, 7)

# kit_cards = [(12, 'D'), (13, 'S'), (7, 'S'), (11, 'S'), (14, 'D'), (6, 'C'), (4, 'D')]  # Highcard
# kit_cards = [(5, 'S'), (4, 'D'), (6, 'D'), (12, 'C'), (4, 'S'), (7, 'D'), (2, 'D')]  # Pair
# kit_cards = [(12, 'H'), (9, 'S'), (2, 'C'), (4, 'H'), (9, 'D'), (13, 'S'), (10, 'C')]  # Pair
# kit_cards = [(12, 'H'), (9, 'S'), (12, 'C'), (4, 'H'), (9, 'D'), (13, 'S'), (10, 'C')]  # Two pairs
# kit_cards = [(6, 'C'), (3, 'D'), (14, 'C'), (6, 'D'), (6, 'S'), (9, 'S'), (13, 'C')]  # Three of a kind
# kit_cards = [(2, 'H'), (3, 'S'), (4, 'C'), (5, 'H'), (6, 'D'), (7, 'S'), (8, 'C')]  # Straight
# kit_cards = [(2, 'H'), (4, 'H'), (6, 'H'), (8, 'H'), (10, 'H'), (12, 'H'), (14, 'H')]  # Flush
# kit_cards = [(5, 'S'), (5, 'D'), (3, 'D'), (5, 'C'), (3, 'S'), (7, 'D'), (2, 'D')]  # Full house
# kit_cards = [(12, 'S'), (12, 'D'), (7, 'H'), (12, 'C'), (7, 'S'), (7, 'D'), (2, 'D')]  # Full house
# kit_cards = [(2, 'H'), (6, 'S'), (6, 'C'), (6, 'H'), (6, 'D'), (4, 'S'), (8, 'C')]  # Four of a kind
# kit_cards = [(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H')]  # Straight flush
# kit_cards = [(4, 'H'), (3, 'S'), (10, 'H'), (11, 'H'), (12, 'H'), (13, 'H'), (14, 'H')]  # Royal flush
# kit_cards = [(2, 'S'), (4, 'H'), (6, 'H'), (8, 'H'), (10, 'H'), (12, 'H'), (14, 'C')]
# kit_cards = [(2, 'H'), (4, 'C'), (6, 'C'), (8, 'C'), (10, 'C'), (12, 'H'), (14, 'C')]
# kit_cards = []
# seven_cards = []

seven_cards = SevenCards(kit_cards)

combo_names = {1: 'Highcard', 2: 'Pair', 3: 'Two pairs', 4: 'Three of a kind', 5: 'Straight',
               6: 'Flush', 7: 'Full house', 8: 'Four of a kind', 9: 'Straight flush', 10: 'Royal flush'}

winner_hand, maximum_score = define_winner_hand(seven_cards)
print("Winner:", winner_hand, "-", combo_names.get(maximum_score))
