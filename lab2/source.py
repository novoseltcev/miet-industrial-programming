import numpy as np


def solve(a: float, b: float, c: float, d: float, e: float, f: float):
    if all((a == 0, b == 0, c == 0, d == 0, e == 0, f == 0)):
        return '5'
    elif (
            a * d - c * b != 0 and
            (e * d - b * f != 0 or a * f - c * e != 0)
    ):
        y = (a * f - c * e) / (a * d - c * b)
        x = (-b * f + d * e) / (a * d - c * b)
        return f'2 {x} {y}'
    elif (
            ((a * d - c * b == 0) and ((e * d - b * f != 0) or (a * f - c * e != 0))) or
            (a == 0 and c == 0 and np.float64(e) / np.float64(b) != np.float64(f) / np.float64(d)) or
            (b == 0 and d == 0 and np.float64(e) / np.float64(a) != np.float64(f) / np.float64(c)) or
            (a == 0 and b == 0 and c == 0 and d == 0 and (e / f > 0))
    ):
        if (
                ((a == 0 and b == 0 and c == 0 and d != 0 and e == 0) or
                 (a == 0 and b != 0 and c == 0 and d == 0 and f == 0))
        ):
            if b == 0:
                y = f / d
            elif d == 0:
                y = e / b
            elif e == 0 or f == 0:
                y = 0
            return f'4 {y}'
        elif (
                (a == 0 and b == 0 and c != 0 and d == 0 and e == 0) or
                (a != 0 and b == 0 and c == 0 and d == 0 and f == 0)
        ):
            if a == 0:
                x = f / c
            elif c == 0:
                x = e / a
            elif f == 0 or e == 0:
                x = 0
            return f'3 {x}'
        else:
            return '0'
    elif a == 0 and c == 0:
        if e == 0:
            y = f / d
        elif f == 0:
            y = e / b
        else:
            y = e / b
        return f'4 {y}'
    elif b == 0 and d == 0:
        if e == 0:
            x = f / c
        elif f == 0:
            x = e / a
        else:
            x = e / a
        return f'3 {x}'
    elif b == 0 and e == 0:
        k = -c / d
        n = f / d
        return f'1 {k} {n}'
    elif d == 0 and f == 0:
        k = -a / b
        n = e / b
        return f'1 {k} {n}'
    elif a == 0 and e == 0:
        k = -d / c
        n = f / c
        return f'1 {k} {n}'
    elif c == 0 and f == 0:
        k = -b / a
        n = e / a
        return f'1 {k} {n}'
    elif a / b == c / d:
        k = -c / d
        n = f / d
        return f'1 {k} {n}'
    else:
        return 'Are you kidding me?'


if __name__ == '__main__':
    print(' -- Equal solver --')
    first_equal = map(int, input('Input koeff for equal like `ax + by = e`: ').split()[:3])
    second_equal = map(int, input('Input koeff for equal like `cx + dy = f`: ').split()[:3])
    a, b, e = first_equal
    c, d, f = second_equal
    result = solve(a, b, c, d, e, f)
    print(result)
