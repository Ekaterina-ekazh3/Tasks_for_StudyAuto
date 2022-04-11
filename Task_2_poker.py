#  Задача: написать функцию, которая берёт на вход набор карт (строго говоря, 7 карт, но на самом деле, это не важно)
#  и возвращает старшую пятикарточную комбинацию в этом наборе.
#
#  Обозначения:
#  2,3,4,5,6,7,8,9,10,11,12,13,14 - 2,3,4,5,6,7,8,9,10,J,Q,K,A соответственно
#  'H', 'S', 'C', 'D' - Hearts, Spades, Clubs, Diamonds соответственно

#  import random
import itertools
from collections import Counter

#  Создаем колоду с картами (кортеж кортежей)
#  all_cards = tuple([(x, y) for x in range(2, 15) for y in ('H', 'S', 'C', 'D')])

#  Создаем случайную руку из 7 карт
#  hand = tuple(random.sample(all_cards, 7))

hand = ((5, 'S'), (4, 'D'), (6, 'D'), (12, 'C'), (4, 'S'), (7, 'D'), (2, 'D'))

#  Список всех возможных 5-карточных комбинаций в руке
all_combo_in_hand = list(itertools.combinations(hand, 5))

#  Сортировка по масти
ordered_all_combo_in_hand_by_suits = []

for hnd in all_combo_in_hand:
    shnd = sorted(hnd, key=lambda crd: crd[1])
    ordered_all_combo_in_hand_by_suits.append(shnd)

#  Ранжирование рук
hands_scores = []

for shnd in ordered_all_combo_in_hand_by_suits:
    if shnd[0][1] == shnd[4][1]:
        shnd = sorted(shnd, key=lambda crd: crd[0])
        if shnd[4][0] - shnd[0][0] != 4:
            hands_scores.append(6)  # Flush
        elif shnd[0][0] == 10:
            hands_scores.append(10)  # Royal flush
        else:
            hands_scores.append(9)  # Straight flush
        continue
    else:
        shnd = sorted(shnd, key=lambda crd: crd[0])
        sorted_list_of_values = []
        for n in range(0, 5):
            sorted_list_of_values.append(shnd[n][0])

        if sorted_list_of_values[4] - sorted_list_of_values[0] == 4:
            hands_scores.append(5)  # Straight
            continue

        elif 14 in sorted_list_of_values and sorted_list_of_values[3] - sorted_list_of_values[0] == 3 and sorted_list_of_values[0] == 2:
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

# Найти максимум в полученном списке оцененных рук и количество рук с максимумом очков
max_score = max(hands_scores)
count_of_max = hands_scores.count(max_score)

# Найти список индексов рук с максимумом очков (можно упростить - использовать код после else и для единичного случая)
if count_of_max == 1:
    ind_max = list(hands_scores.index(max_score))
else:
    ind_max = []
    count_ind = 0
    for s in hands_scores:
        if s == max_score:
            ind_max.append(count_ind)
        count_ind += 1

# Сделать список кортежей выигравших рук (комбинаций)
hand_max = []
for i in ind_max:
    hand_max.append(all_combo_in_hand[i])

combo_names = {1: 'Highcard', 2: 'Pair', 3: 'Two pairs', 4: 'Three of a kind', 5: 'Straight',
               6: 'Flush', 7: 'Full house', 8: 'Four of a kind', 9: 'Straight flush', 10: 'Royal flush'}

if len(hand_max) == 1:
    print(hand_max[0], "-", combo_names[max_score])

else:
    if max_score == 9:
        tops = []
        for hand in hand_max:
            nominals = []
            for card in hand:
                nominals.append(card[0])
            tops.append(max(nominals))
        winner = max(tops)
        winner_hand = hand_max.index(winner)
        print(hand_max[winner_hand], "-", combo_names[max_score])

    if max_score == 7:
        common_list = []
        for hand in hand_max:
            nominals = []
            for card in hand:
                nominals.append(card[0])
            dict_nominals = Counter(nominals)
            common_list.append(dict_nominals)

        max_nominal_3 = 0
        max_nominal_2 = 0
        for counter in common_list:
            for k, v in counter.items():
                if v == 3:
                    if max_nominal_3 < k:
                        max_nominal_3 = k
                    else:
                        continue
                if v == 2:
                    if max_nominal_2 < k:
                        max_nominal_2 = k
                    else:
                        continue

        winner = 0
        for c in range(0, len(common_list)):
            if max_nominal_3 in common_list[c]:
                if max_nominal_3 in common_list[c+1 : ]:
                    if max_nominal_2 in common_list[c]:
                        winner = c
                else:
                    winner = c
            else:
                continue

        winner_hand = hand_max.index(winner)
        print(hand_max[winner_hand], "-", combo_names[max_score])

    if max_score == 6:

    if max_score == 5:

    if max_score == 4:

    if max_score == 3:

    if max_score == 2:

    if max_score == 1:

    # нужно сравнить номинал 2х элементов (рук) из hand_max, комбинация известна
    #  если 1, то... для каждого типа комбинации свое сравнение?
    # можно снова использовать Counter создать словарь номинал:количество, а потом сравнить словари (Counter лучше
    # применять к отсортированному списку). словари будут одинаковой длины, раз комбинация совпала

# решает номинал старшей карты в комбинации, если равны,
# смотрят номинал младшей
# Сделать вывод названия старшей 5-карточной комбинации и самой комбинации
# Сделать чтение набора карт из файла?
# Обернуть код в функцию
# Предусмотреть возможные экспешены.

# Некоторые повторяющиеся действия можно бы переписать в функции, и вызывать по необходимости.