#  Задача:
#  написать функцию, которая берёт на вход набор карт (строго говоря, 7 карт, но на самом деле, это не важно)
#  и возвращает старшую пятикарточную комбинацию в этом наборе.
#
#  Обозначения:
#  2,3,4,5,6,7,8,9,10,11,12,13,14 - 2,3,4,5,6,7,8,9,10,J,Q,K,A соответственно
#  'H', 'S', 'C', 'D' - Hearts, Spades, Clubs, Diamonds соответственно

#  import random
from itertools import combinations
from collections import Counter

#  Создаем колоду с картами (кортеж кортежей)
#  all_cards = tuple([(x, y) for x in range(2, 15) for y in ('H', 'S', 'C', 'D')])

#  Создаем случайную руку из 7 карт
#  seven_cards = tuple(random.sample(all_cards, 7))

seven_cards = [(5, 'S'), (4, 'D'), (6, 'D'), (12, 'C'), (4, 'S'), (7, 'D'), (2, 'D')]

# def define_winner_hand(scs: list) -> list:

#  Список всех возможных 5-карточных комбинаций в руке
all_combo_in_hand = list(combinations(seven_cards, 5))

print(all_combo_in_hand)

combo_names = {1: 'Highcard', 2: 'Pair', 3: 'Two pairs', 4: 'Three of a kind', 5: 'Straight',
               6: 'Flush', 7: 'Full house', 8: 'Four of a kind', 9: 'Straight flush', 10: 'Royal flush'}

#  Сортировка по масти
ordered_all_combo_in_hand_by_suits = []

for hnd in all_combo_in_hand:
    shnd = sorted(hnd, key=lambda crd: crd[1])
    ordered_all_combo_in_hand_by_suits.append(shnd)

#  Ранжирование рук (создание списка с очками для всех комбинаций в руке)
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

# Подсчет количества карт одинакового номинала
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

# Найти максимум в полученном списке оцененных рук и количество рук с максимумом очков
max_score = max(hands_scores)
count_of_max = hands_scores.count(max_score)

ind_max = []
count_ind = 0
for s in hands_scores:
    if s == max_score:
        ind_max.append(count_ind)
    count_ind += 1

# Собираем список рук с выигрышными по баллу комбинациями
hand_max = []
for i in ind_max:
    hand_max.append(all_combo_in_hand[i])

hand_max = sorted(hand_max, key=lambda crd: crd[0])

# Определяем итоговую выигрышную комбинацию
if len(hand_max) == 1:
    print("Winner:", hand_max[0], "-", combo_names.get(max_score))

else:
    if max_score == 10:
        pass

    if max_score == 9:
        winner = 0
        winner_hand = []
        for hand in hand_max:
            if hand[4][0] > winner:
                winner = hand[4][0]
                winner_hand = hand
        print("Winner:", winner_hand, "-", combo_names.get(max_score))

    if max_score == 8:
        pass

    if max_score == 7:
        winner_hand = []
        nominals = []
        for hand in hand_max:
            count_start = hand.count(hand[0][0])
            if count_start == 3:
                nominals.append([hand[0][0], hand[4][0]])
            else:
                nominals.append([hand[4][0], hand[0][0]])

        if nominals[0][0] == nominals[1][0]:
            if nominals[0][1] > nominals[1][1]:
                winner_hand = hand_max[0]
            else:
                winner_hand = hand_max[1]

        else:
            if nominals[0][0] > nominals[1][0]:
                winner_hand = hand_max[0]
            else:
                winner_hand = hand_max[1]
        print("Winner:", winner_hand, "-", combo_names.get(max_score))

    if max_score == 6:
        hand_max_without_suit = []
        for hand in hand_max:
            hand_max_without_suit.append([hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]])

        winner_hand_without_suit = max(hand_max_without_suit)
        windex = hand_max_without_suit.index(winner_hand_without_suit)
        winner_hand = hand_max[windex]
        print("Winner:", winner_hand, "-", combo_names.get(max_score))

    if max_score == 5:
        hand_max_without_suit = []
        for hand in hand_max:
            hand_max_without_suit.append([hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]])

        for hand in hand_max_without_suit:
            if 14 in hand and 2 in hand:
                hand.insert(0, 14)
                hand.pop(5)

        winner = 0
        winner_hand_without_suit = 0
        for hand in hand_max_without_suit:
            if hand[4] > winner:
                winner = hand[4]
                winner_hand_without_suit = hand

        windex = hand_max_without_suit.index(winner_hand_without_suit)
        winner_hand = hand_max[windex]
        print("Winner:", winner_hand, "-", combo_names.get(max_score))

    if max_score == 4:
        hand_max_without_suit = []
        for hand in hand_max:
            hand_max_without_suit.append([hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]])

        for hand in hand_max_without_suit:
            value_of_three = hand[2]
            for i in range(3):
                hand.remove(value_of_three)

        winner_hand_without_suit = max(hand_max_without_suit)
        windex = hand_max_without_suit.index(winner_hand_without_suit)
        winner_hand = hand_max[windex]
        print("Winner:", winner_hand, "-", combo_names.get(max_score))

    if max_score == 3:
        hand_max_without_suit = []
        for hand in hand_max:
            hand_max_without_suit.append([hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]])

        winner_hand_without_suit = max(hand_max_without_suit)
        windex = hand_max_without_suit.index(winner_hand_without_suit)
        winner_hand = hand_max[windex]
        print("Winner:", winner_hand, "-", combo_names.get(max_score))

    if max_score == 2:
        hand_max_without_suit = []
        for hand in hand_max:
            hand_max_without_suit.append([hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]])

        winner_hand_without_suit = max(hand_max_without_suit)
        windex = hand_max_without_suit.index(winner_hand_without_suit)
        winner_hand = hand_max[windex]
        print("Winner:", winner_hand, "-", combo_names.get(max_score))

    if max_score == 1:
        hand_max_without_suit = []
        for hand in hand_max:
            hand_max_without_suit.append([hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]])

        winner_hand_without_suit = max(hand_max_without_suit)
        windex = hand_max_without_suit.index(winner_hand_without_suit)
        winner_hand = hand_max[windex]
        print("Winner:", winner_hand, "-", combo_names.get(max_score))

print(max_score, count_of_max)

# Сделать чтение набора карт из файла?
# Обернуть код в функцию
# Предусмотреть возможные экспешены.
# Некоторые повторяющиеся действия можно бы переписать в функции, и вызывать по необходимости.
# Переписать Йода-условия на человеческий.