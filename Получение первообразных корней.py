# -- Программа реализации алгоритма генерации первообразных ключей --


def algoritm_Euclid(a, b):
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


# Получение первообразных корней
def primitive_root(m):                                                             # функция принимает модуль m
    result = []
    counter = 0
    required_set = set(num for num in range (1, m) if algoritm_Euclid(num, m) == 1)
    # создаем множество из num для которых НОД (num и m) равны 1
    for g in range(1, m):                                                          # g от 1 до m
        actual_set = set(pow(g, powers) % m for powers in range (1, m))
        if required_set == actual_set:
            result.append(g)
            counter += 1
            if counter == 100:
                return result
            # print(g)
    return result


# Точка входа для основной программы
def main():
    m = int(input("Введите m = "))
    result = primitive_root(m)
    k = 0
    # 317
    for i in result:
        print("{0}: {1}".format(k+1, i))
        k += 1

# Вызов программы
main()