from gen_primitive_root import pollard, root


def get_roots(n):
    list_dividers = pollard.get_factor_n(n)
    print(list_dividers)
    list_dividers = list(set(list_dividers))
    result = []
    # counter = 0
    print(list_dividers)
    for g in range(2, n+1):
        if pollard.gcd(n+1, g) != 1:
            print("Выполнилось!")
            continue
        res = root.is_root(g, list_dividers, n)
        # print("Res: {0}".format(res))
        if res:
            result.append(res)
            # counter += 1
            # if counter == 100:
            # return result
    return result

def main():
    n = int(input("Введите модуль n: "))
    result = get_roots(n-1)
    counter = 0
    print(result)
    for i in result:
        print("counter {0}: {1}".format(counter, i))
        counter += 1


main()