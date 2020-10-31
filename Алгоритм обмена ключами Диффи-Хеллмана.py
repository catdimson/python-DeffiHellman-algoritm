# -- Программа реализации алгоритма обмена ключами Диффи-Хеллмана --
from gen_simple_numbers import gen_sp, test_rabin_miller
from gen_primitive_root import pollard, root


# Генерируем общеизвестные получаем n, Xa, Xb
def get_start_data():
    choice = int(input("x, Xa, Xb - вводим с клавиатуры, либо генерируем случайным образом? (1/2): "))
    if choice == 1:
        while True:
            n = int(input("Введите x: "))
            if test_rabin_miller.test_Rabin_Miller(n,5) == True:
                break
            else:
                print("х должен быть простым.")
        Xa = int(input("Введите Xa: "))
        Xb = int(input("Введите Xb: "))
    else:
        n = gen_sp.gen_sp(64)
        Xa = gen_sp.gen_sp(40)
        Xb = gen_sp.gen_sp(40)
    return n, Xa, Xb


def get_root(n):
    list_dividers = list(set(pollard.get_factor_n(n-1)))
    print(list_dividers)
    for g in range(2, n):
        g = root.is_root(g, list_dividers, n)
        if g:
            return g


# Точка входа
def main():
    print("---"*20)
    n, Xa, Xb = get_start_data()
    print("---"*20)
    print("n = {0}".format(n))
    print("Xa = {0}".format(Xa))
    print("Xb = {0}".format(Xb))
    print("---"*20)

    g = get_root(n)
    print("g = {0}".format(g))
    print("---"*20)

    Ya = root.fast_pow(g, Xa, n)
    Yb = root.fast_pow(g, Xb, n)
    print("Ya = {0}".format(Ya))
    print("Yb = {0}".format(Yb))
    print("---"*20)

    # Вычисление секретных ключей
    Ka = root.fast_pow(Yb, Xa, n)
    Kb = root.fast_pow(Ya, Xb, n)
    print("Ka = {0}".format(Ka))
    print("Kb = {0}".format(Kb))
    print("Равны ключи?: {0}".format(Ka==Kb))
    print("---"*20)
main()
