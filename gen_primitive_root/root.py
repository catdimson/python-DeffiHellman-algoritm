def fast_pow(base, degree, module):
    degree = bin(degree)[2:]
    r = 1

    for i in range(len(degree) - 1, -1, -1):
        r = (r * base ** int(degree[i])) % module
        base = (base ** 2) % module
    return r


def is_root(g, list_dividers, n):
    for num in list_dividers:
        power = int(n / num)
        res = fast_pow(g, power, n+1)
        if res == 1:
            return False
    return g