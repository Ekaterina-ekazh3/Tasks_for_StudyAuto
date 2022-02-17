# Задание:
# Необходимо написать функцию, которая получает на вход натуральное число N, а возвращает число нулей на конце N!
def count_zeros(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("Вы ввели не число!")
    if n < 0:
        raise ValueError("Вы ввели отрицательное число!")
    zeros = 0  # стартовое значение счетчика нулей
    m = 1  # стартовая степень для 5
    while (n // (5 ** m)) > 0:
        tmp_count = n // (5 ** m)
        m += 1
        zeros += tmp_count
    return zeros
