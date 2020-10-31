from random import randint
from time import perf_counter
import random



def gcd(a, b):
    '''An implementation of extended Euclidean algorithm.
    Returns integer x, y and gcd(a, b) for Bezout equation:
        ax + by = gcd(a, b).
    '''
    x0, x1, y0, y1 = 1, 0, 0, 1
    step = 0
    while b:
        # 12741

        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - x1*q
        y, y1 = y1, y0 - y1*q
        step += 1
    # return (a, x0, y0)
    return a


def fast_pow(base, degree, module):
    degree = bin(degree)[2:]
    r = 1

    for i in range(len(degree) - 1, -1, -1):
        r = (r * base ** int(degree[i])) % module
        base = (base ** 2) % module
    return r


def test_Rabin_Miller(n, k):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for i in range(k):
        a = random.randint(2, n - 2)
        x = fast_pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for j in range(1, s):
            x = fast_pow(x, 2, n)
            # print('x = {0}'.format(x))

            if x == 1:
                return False
            if x == n - 1:
                return True
        return False
    return True


def miller_rabin_test(a, n, s, d):
    """Один тест Миллера-Рабина.
    Является ли число 2 <= a <= n-2 свидетелем простоты для числа n (n-1 = d * 2**s)
    Если вдруг среди чисел a**(d*2**0), ..., a**(d*2**s) перед какой-то 1 идёт не -1,
    то число n — составное, а a — не является свидетелем простоты."""
    x = pow(a, d, n)  # x = a**(d*2**0)
    if x in (1, n - 1):
        return True
    for r in range(s - 1):
        x = (x * x) % n  # Из числа a**(d*2**r) вычисляем a**(d*2**(r+1))
        if x == 1:  # Ну всё, число составное
            return False
        elif x == n - 1:  # Нашлась -1. Число a — свидетель простоты для n
            return True
    return False  # Даже тест Ферма не пройден: a**(n-1) != 1


def miller_rabin(n):
    """Проверяет простоту числа n>3, выполняя log2(n) тестов Миллера-Рабина"""
    # Ищем разложение n-1 = n-1 = d * 2**s
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for _ in range(n.bit_length()):  # Повторяем тест log2(n) раз.
        a = randint(2, n - 2)  # берём случайное число
        if not miller_rabin_test(a, n, s, d):  # Если тест не пройден, то число составное
            return False
    return True  # С вероятностью 1/n**2 число простое


def pollards_rho_iter(n):
    """Поиск делителя у нечётного составного числа"""
    # Начинаем с функции F(x) = x**2 + 1 из точки x=2. Обычно это срабатывает
    x = y = 2
    a = 1       # случайное число х0
    while True:
        d = 1
        while d == 1:  # Если 1 < d < n, то мы нашли делитель d
            x = (x ** 2 - a) % n  # x = F(F(..(F(x)..))
            y = (y ** 2 - a) % n
            y = (y ** 2 - a) % n  # y = F(F(F(F(..(F(F(x))..))))   (в два раз больше раз F)
            d = gcd(n, abs(x - y))
        if d < n:  # Если 1 < d < n, то мы нашли делитель d
            return d
        # Редко бывает так, что для функции x**2 + 1 при старте с 2 делитель не находится
        # В этом случае используем F(x) = x**2 + a, и стартуем с другого случайного числа
        x = y = randint(1, n - 1)
        a = randint(-100, 100) % n

# def pollards_rho_iter(n):
#     def fun(x, n):
#         base = x ** 2 - 1 % n
#         return base
#     j = 1
#     x = random.randint(0, n-1)
#     while True:
#         _x = x
#         for i in range(j):
#             x = fun(x, n)
#             d = gcd(x - _x, n)
#             if d > 1:
#                 return d
#         j = 2 * j


def factor(n):
    """Факторизация числа при помощи ро-метода Полларда и тестов Миллера-Рабина"""
    # Избавляемся от всех двоек, троек и пятёрок
    ans = []
    for x in (2, 3, 5):
        while n % x == 0:
            ans.append(x)
            n //= x
    if n == 1:
        pass  # n = 2**a * 3**b * 5**c
    elif miller_rabin(n):  # Остаток простой
        ans.append(n)
    else:  # Ищем делители
        d = pollards_rho_iter(n)
        ans.extend(factor(d))
        ans.extend(factor(n // d))
    return sorted(ans)


# nums = [10, 437, 3127, 23707, 1752967, 6682189, 12659363, 494370889, 1435186847, 11843161246077928296]
# for num in nums:
#     st = perf_counter()
#     fct = factor(num)
#     en = perf_counter()
#     print('Число {} разложено на множители {} за {:02f}c'.format(num, fct, en-st))
def get_factor_n(n):
    fct = factor(n)
    return fct