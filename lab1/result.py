import random
from copy import deepcopy
import numpy as np


def input_int(l_boundary: int, r_boundary: int, msg: str):
    result = None
    while result < l_boundary or result > r_boundary:
        result = int(input(msg))
    return result


def init_matrix(n_rows: int, n_columns: int, fill=None) -> list[list]:
    result = list()
    for _ in range(n_rows):
        result.append([fill] * n_columns)
    return result


def get_matrix_size(matrix: list[list]) -> tuple[int, int]:
    return len(matrix), len(matrix[0])


def print_matrix(matrix: list[list]) -> None:
    for row in matrix:
        print(' '.join(map(str, row)))


def _expand_rows_len(matrix: list[list], row_len: int, fill) -> None:
    _, n_column = get_matrix_size(matrix)
    print(f'{n_column=}')
    for row in matrix:
        row += [fill] * (row_len - n_column)


def _expand_rows_count(matrix: list[list], row_count: int, fill) -> None:
    _, row_len = get_matrix_size(matrix)
    for _ in range(row_count - len(matrix)):
        matrix.append([fill] * row_len)


def expand_matrix(matrix: list[list], n_rows: int, n_columns: int, fill=None) -> list[list]:
    new_matrix = deepcopy(matrix)
    _expand_rows_len(new_matrix, n_columns, fill)
    _expand_rows_count(new_matrix, n_rows, fill)
    return new_matrix


def input_matrix(n_rows: int, n_columns: int) -> list[list]:
    result = list()
    for _ in range(n_rows):
        result.append(
            list(int(input()) for _ in range(n_columns))
        )
    return result


def randomize_matrix(n_rows: int, n_columns: int, interval: tuple[int, int]) -> list[list]:
    result = list()
    for _ in range(n_rows):
        result.append(
            list(random.randint(*interval) for _ in range(n_columns))
        )
    return result


def input_matrix_size(msg=None):
    n_rows = n_columns = -1
    while n_rows <= 0 or n_columns <= 0:
        n_rows, n_columns = map(int, input(msg).split())
    return n_rows, n_columns


def _split_matrix_to_half(matrix: list[list]) -> tuple[list[list], list[list]]:
    _, n_columns = get_matrix_size(matrix)
    left_matrix_half = list()
    for row in matrix:
        left_matrix_half.append(row[:n_columns // 2])
    right_matrix_half = list()

    for row in matrix:
        right_matrix_half.append(row[n_columns // 2:])
    return left_matrix_half, right_matrix_half


def split_matrix_to_corners(matrix: list[list]) -> tuple[list[list], list[list], list[list], list[list]]:
    n_rows, _ = get_matrix_size(matrix)
    left_matrix_half, right_matrix_half = _split_matrix_to_half(matrix)
    left_top_corner = left_matrix_half[:n_rows // 2]
    left_bottom_corner = left_matrix_half[n_rows // 2:]
    right_top_corner = right_matrix_half[:n_rows // 2]
    right_bottom_corner = right_matrix_half[n_rows // 2:]
    return left_top_corner, right_top_corner, left_bottom_corner, right_bottom_corner


def _find_matrix_down_boundary(matrix: list[list]) -> int:
    n_rows, n_columns = get_matrix_size(matrix)
    result = 0
    for row_num in range(n_rows - 1, -1, -1):
        if matrix[row_num].count(0) != n_columns:
            result = row_num
            break
    return result + 1


def _find_matrix_right_boundary(matrix: list[list]) -> int:
    n_rows, n_columns = get_matrix_size(matrix)
    result = 0
    for column_num in range(n_columns - 1, -1, -1):
        column = [matrix[row_n][column_num] for row_n in range(n_rows)]
        if column.count(0) != n_rows:
            result = column_num
            break
    return result + 1


def align_matrix(matrix: list[list[int]]) -> list[list]:
    new_height = _find_matrix_down_boundary(matrix)
    new_length = _find_matrix_right_boundary(matrix)
    result = list()
    for row in matrix[:new_height]:
        result.append(row[:new_length])
    return result


def join_corners(
        left_top_corner: list[list],
        right_top_corner: list[list],
        left_bottom_corner: list[list],
        right_bottom_corner: list[list]
) -> list[list]:
    result = list()
    for i in range(middle_l):
        result.append(left_top_corner[i] + right_top_corner[i])
    for i in range(middle_l):
        result.append(left_bottom_corner[i] + right_bottom_corner[i])
    return result


if __name__ == '__main__':
    print('Вас приветствует программа\n'
          'быстрого перемножения матриц методом Штрассена\n')

    n_rows_A, n_cols_A = input_matrix_size('Введите размеры первой матрицы\n')
    n_rows_B, n_cols_B = input_matrix_size('Введите размеры второй матрицы\n')
    fill_type = input_int(
        l_boundary=1,
        r_boundary=2,
        msg='Выберите способ заполнения матриц\n'
                        '1 - Вручную \n'
                        '2 - Случайным образом\n')

    """Заполнение матриц."""
    match fill_type:
        case 1:
            A = input_matrix(n_rows_A, n_cols_A)
            B = input_matrix(n_rows_B, n_cols_B)

        case 2:
            A = randomize_matrix(n_rows_A, n_cols_A, (1, 10))
            B = randomize_matrix(n_rows_B, n_cols_B, (1, 10))

        case _:
            raise ValueError(f'{fill_type=} must be 1 or 2')

    print('\nМатрица 1:\n')
    print_matrix(A)

    print('\nМатрица 2:\n')
    print_matrix(B)

    """Приведение матриц к требуемому размеру"""
    expand_size = 2
    while expand_size < max(n_rows_A, n_rows_B, n_cols_A, n_cols_B):
        expand_size *= 2

    expanded_A = expand_matrix(A, expand_size, expand_size, 0)
    expanded_B = expand_matrix(B, expand_size, expand_size, 0)

    print('Приведенные матрицы\n')
    print('Матрица 1:\n')
    print_matrix(expanded_A)

    print('\nМатрица 2:\n')
    print_matrix(expanded_B)

    A11, A12, A21, A22 = split_matrix_to_corners(expanded_A)
    B11, B12, B21, B22 = split_matrix_to_corners(expanded_B)

    """Вычисление значений промежуточных матриц"""
    middle_l = expand_size // 2
    D = init_matrix(middle_l, middle_l, 0)
    D1 = init_matrix(middle_l, middle_l, 0)
    D2 = init_matrix(middle_l, middle_l, 0)
    H1 = init_matrix(middle_l, middle_l, 0)
    H2 = init_matrix(middle_l, middle_l, 0)
    V1 = init_matrix(middle_l, middle_l, 0)
    V2 = init_matrix(middle_l, middle_l, 0)

    for i in range(middle_l):
        for j in range(middle_l):
            for z in range(middle_l):
                D[i][j] += (A11[i][z] + A22[i][z]) * (B11[z][j] + B22[z][j])

            for z in range(middle_l):
                D1[i][j] += (A12[i][z] - A22[i][z]) * (B21[z][j] + B22[z][j])

            for z in range(middle_l):
                D2[i][j] += (A21[i][z] - A11[i][z]) * (B11[z][j] + B12[z][j])

            for z in range(middle_l):
                H1[i][j] += (A11[i][z] + A12[i][z]) * B22[z][j]

            for z in range(middle_l):
                H2[i][j] += (A21[i][z] + A22[i][z]) * B11[z][j]

            for z in range(middle_l):
                V1[i][j] += A22[i][z] * (B21[z][j] - B11[z][j])

            for z in range(middle_l):
                V2[i][j] += A11[i][z] * (B12[z][j] - B22[z][j])

    """Подсчет значений вспомогательных матриц из промежуточных"""
    R11 = init_matrix(middle_l, middle_l)
    R12 = init_matrix(middle_l, middle_l)
    R21 = init_matrix(middle_l, middle_l)
    R22 = init_matrix(middle_l, middle_l)

    for i in range(middle_l):
        for j in range(middle_l):
            R11[i][j] = D[i][j] + D1[i][j] - H1[i][j] + V1[i][j]
            R12[i][j] = V2[i][j] + H1[i][j]
            R21[i][j] = V1[i][j] + H2[i][j]
            R22[i][j] = D[i][j] + D2[i][j] + V2[i][j] - H2[i][j]

    preR = join_corners(R11, R12, R21, R22)
    R = align_matrix(preR)

    print('\nРезультирующая матрица\n')
    print_matrix(R)

    assert np.matrix(R) == np.matmul(np.matrix(expanded_A), np.matrix(expanded_B))
    input('\n')
