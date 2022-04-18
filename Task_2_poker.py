#  Задача:
#  написать функцию, которая берёт на вход набор карт (строго говоря, 7 карт, но на самом деле, это не важно)
#  и возвращает старшую пятикарточную комбинацию в этом наборе.
#
#  Обозначения:
#  2,3,4,5,6,7,8,9,10,11,12,13,14 - 2,3,4,5,6,7,8,9,10,J,Q,K,A соответственно
#  'H', 'S', 'C', 'D' - Hearts, Spades, Clubs, Diamonds соответственно


# import random
from itertools import combinations
from collections import Counter


def define_winner_hand(scs: list) -> tuple:

    # Список всех возможных 5-карточных комбинаций в руке
    all_combo_in_hand = list(combinations(scs, 5))

    print(all_combo_in_hand)

    # Сортировка по масти
    ordered_all_combo_in_hand_by_suits = []

    for hnd in all_combo_in_hand:
        shnd = sorted(hnd, key=lambda crd: crd[1])
        ordered_all_combo_in_hand_by_suits.append(shnd)

    hands_scores = scoring_for_a_combination(ordered_all_combo_in_hand_by_suits)

    # Найти максимум в полученном списке оцененных рук и количество рук с максимумом очков
    max_score = max(hands_scores)

    ind_max = []
    count_ind = 0
    for s in hands_scores:
        if s == max_score:
            ind_max.append(count_ind)
        count_ind += 1

    # Собираем список рук с выигрышными по баллу комбинациями и сортируем по номиналу
    hand_max = []
    for i in ind_max:
        hand_max.append(sorted(all_combo_in_hand[i], key=lambda crd: crd[0]))

    # Определяем итоговую выигрышную комбинацию
    if len(hand_max) == 1:
        win_hand = hand_max[0]

        return win_hand, max_score

    else:
        win_hand = ()
        if max_score == 10:
            pass

        if max_score == 9:
            hand_max_without_suit = clean_of_card_suit(hand_max)

            for hand in hand_max_without_suit:
                if 14 in hand and 2 in hand:
                    hand.insert(0, 14)
                    hand.pop(5)

            find_winner_hand(hand_max_without_suit, hand_max, max_score)

        if max_score == 8:
            pass

        if max_score == 7:
            hand_max_without_suit = clean_of_card_suit(hand_max)

            nominals = []
            for hand in hand_max_without_suit:
                count_start = hand.count(hand[0])
                if count_start == 3:
                    nominals.append([hand[0], hand[4]])
                else:
                    nominals.append([hand[4], hand[0]])

            win_hand = ()
            for i in range(len(nominals) - 1):
                if nominals[i][0] == nominals[i + 1][0]:
                    if nominals[i][1] == nominals[i + 1][1]:
                        win_hand = hand_max[i]
                    else:
                        if nominals[i][1] > nominals[i + 1][1]:
                            win_hand = hand_max[i]
                        else:
                            win_hand = hand_max[i + 1]
                else:
                    if nominals[i][0] > nominals[i + 1][0]:
                        win_hand = hand_max[i]
                    else:
                        win_hand = tuple(hand_max[i + 1])

        if max_score == 6:
            hand_max_without_suit = clean_of_card_suit(hand_max)
            find_winner_hand(hand_max_without_suit, hand_max, max_score)

        if max_score == 5:
            hand_max_without_suit = clean_of_card_suit(hand_max)

            for hand in hand_max_without_suit:
                if 14 in hand and 2 in hand:
                    hand.insert(0, 14)
                    hand.pop(5)

            find_winner_hand(hand_max_without_suit, hand_max, max_score)

        if max_score == 4:
            hand_max_without_suit = clean_of_card_suit(hand_max)

            for hand in hand_max_without_suit:
                value_of_three = hand[2]
                ind = hand_max_without_suit.index(hand)
                for i in range(3):
                    hand_max_without_suit[ind].remove(value_of_three)

            find_winner_hand(hand_max_without_suit, hand_max, max_score)

        if max_score == 3:
            hand_max_without_suit = clean_of_card_suit(hand_max)
            find_winner_hand(hand_max_without_suit, hand_max, max_score)

        if max_score == 2:
            hand_max_without_suit = clean_of_card_suit(hand_max)
            find_winner_hand(hand_max_without_suit, hand_max, max_score)

        if max_score == 1:
            hand_max_without_suit = clean_of_card_suit(hand_max)
            win_hand = find_winner_hand(hand_max_without_suit, hand_max, max_score)

        return win_hand, max_score


def scoring_for_a_combination(ordered_all_combo_in_hand_by_suits):
    hands_scores = []

    for shnd in ordered_all_combo_in_hand_by_suits:
        if shnd[0][1] == shnd[4][1]:
            shnd = sorted(shnd, key=lambda crd: crd[0])
            if shnd[4][0] - shnd[0][0] == 4:
                if shnd[0][0] == 10:
                    hands_scores.append(10)  # Royal flush
                else:
                    hands_scores.append(9)  # Straight flush
            else:
                if 14 in shnd and shnd[3][0] - shnd[0][0] == 3 and shnd[0] == 2:
                    hands_scores.append(5)  # Straight
                else:
                    hands_scores.append(6)  # Flush

        else:
            shnd = sorted(shnd, key=lambda crd: crd[0])
            sorted_list_of_values = []
            for n in range(0, 5):
                sorted_list_of_values.append(shnd[n][0])

            if sorted_list_of_values[4] - sorted_list_of_values[0] == 4 \
                    and len(sorted_list_of_values) == len(set(sorted_list_of_values)):
                hands_scores.append(5)  # Straight
                continue

            elif 14 in sorted_list_of_values and sorted_list_of_values[3] - sorted_list_of_values[0] == 3 \
                    and sorted_list_of_values[0] == 2:
                hands_scores.append(5)  # Straight
                continue

            else:
                counter_values = Counter(sorted_list_of_values)
                values = list(counter_values.values())

                if 4 in values:
                    hands_scores.append(8)  # Four of a kind
                    continue

                elif 3 in values:
                    if 2 in values:
                        hands_scores.append(7)  # Full house
                        continue
                    else:
                        hands_scores.append(4)  # Three of a kind
                        continue

                elif 2 in values:
                    vc = values.count(2)
                    if vc == 2:
                        hands_scores.append(3)  # Two pairs
                        continue
                    else:
                        hands_scores.append(2)  # Pair
                        continue
                else:
                    hands_scores.append(1)  # Highcard
    print(hands_scores)
    return hands_scores


def clean_of_card_suit(hand_max):
    hand_max_without_suit = []
    for hand in hand_max:
        hand_max_without_suit.append([hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]])
    return hand_max_without_suit


def find_winner_hand(hand_max_without_suit, hand_max, max_score):
    if max_score == 9 or max_score == 5:
        winner = 0
        winner_hand_without_suit = []
        for hand in hand_max_without_suit:
            if hand[4] > winner:
                winner = hand[4]
                winner_hand_without_suit = hand

        windex = hand_max_without_suit.index(winner_hand_without_suit)
        win_hand = hand_max[windex]
        return win_hand

    else:
        winner_hand_without_suit = max(hand_max_without_suit)
        windex = hand_max_without_suit.index(winner_hand_without_suit)
        win_hand = hand_max[windex]
        return win_hand


combo_names = {1: 'Highcard', 2: 'Pair', 3: 'Two pairs', 4: 'Three of a kind', 5: 'Straight',
               6: 'Flush', 7: 'Full house', 8: 'Four of a kind', 9: 'Straight flush', 10: 'Royal flush'}

# seven_cards = [(5, 'S'), (4, 'D'), (6, 'D'), (12, 'C'), (4, 'S'), (7, 'D'), (2, 'D')]
# seven_cards = [(5, 'S'), (5, 'D'), (3, 'D'), (5, 'C'), (3, 'S'), (7, 'D'), (2, 'D')]
# seven_cards = [(6, 'C'), (3, 'D'), (14, 'C'), (6, 'D'), (6, 'S'), (9, 'S'), (13, 'C')]
seven_cards = [(12, 'D'), (13, 'S'), (7, 'S'), (11, 'S'), (14, 'D'), (6, 'C'), (4, 'D')]

#  Создаем колоду с картами (кортеж кортежей)
# all_cards = tuple([(x, y) for x in range(2, 15) for y in ('H', 'S', 'C', 'D')])

#  Создаем случайную руку из 7 карт
# seven_cards = random.sample(all_cards, 7)

winner_hand, maximum_score = define_winner_hand(seven_cards)
print("Winner:", winner_hand, "-", combo_names.get(maximum_score))


# Исправить места вызова функции find_winner_hand
# Разобраться, нужно или нет возвращать max_score (из функции find_winner_hand вроде бы нет, а из
# "определения итоговой выигрышной комбинации" - да, ее еще нужно обернуть в функцию.
# Обернуть код в функцию
# Некоторые повторяющиеся действия можно бы переписать в функции, и вызывать по необходимости.
# Предусмотреть возможные экспешены (isinstance)
# Добавить проверки типов вводимого и возвращаемого значения для каждой функции
# Для проверки вводимого значения головной функции возможно есть смысл создать класс (возможно, унаследовать от list),
# объект которого будет представлять собой список-руку состоящую из таплов-карт
# (иначе слишком много нужно навернуть условий, чтобы проверить список такой степени вложенности)
