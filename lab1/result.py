from __future__ import annotations
import numpy as np


class Matrix(np.matrix):
    def get_size(self) -> tuple[int, int]:
        return len(self), super().size // len(self)

    def __mul__(self, other):
        return Matrix(super() * other)

    def __add__(self, other):
        return Matrix(super() + other)

    def __sub__(self, other):
        return Matrix(super() - other)

    def __str__(self):
        return super().__str__().replace('[', ' ').replace(']', '')

    def expand(self, n_rows: int, n_columns: int) -> Matrix:
        inc_rows = n_rows - self.get_size()[0]
        inc_cols = n_columns - self.get_size()[1]
        new_columns = np.zeros((self.get_size()[0], inc_cols))
        new_rows = np.zeros((inc_rows, n_columns))
        return Matrix(np.vstack((
            np.hstack((self, new_columns)),
            new_rows
        )))

    def split_by_corners(self) -> tuple[Matrix, Matrix, Matrix, Matrix]:
        left_half, right_half = np.vsplit(self, 2)
        return np.hsplit(left_half, 2) + np.hsplit(right_half, 2)

    def _find_down_boundary(self) -> int:  # TODO
        n_rows, _ = self.get_size()
        result = 0
        for row_num in range(n_rows - 1, -1, -1):
            if np.count_nonzero(self[row_num]) != 0:
                result = row_num
                break
        return result + 1

    def _find_right_boundary(self) -> int:  # TODO
        _, n_columns = self.get_size()
        result = 0
        for column_num in range(n_columns - 1, -1, -1):
            if np.count_nonzero(self[::, column_num]) != 0:
                result = column_num
                break
        return result + 1

    def align(self) -> Matrix:
        new_height = self._find_down_boundary()
        new_length = self._find_right_boundary()
        return self[:new_height, :new_length]

    @staticmethod
    def from_corners(
            left_top_corner: Matrix,
            right_top_corner: Matrix,
            left_bottom_corner: Matrix,
            right_bottom_corner: Matrix
    ) -> Matrix:
        return Matrix(np.concatenate(
            (
                np.concatenate((left_top_corner, right_top_corner), axis=1),
                np.concatenate((left_bottom_corner, right_bottom_corner), axis=1)
            ), axis=0
        ))

    @staticmethod
    def random(n_rows: int, n_columns: int, interval: tuple[int, int]) -> Matrix:
        return Matrix(np.random.randint(*interval, size=(n_rows, n_columns)))


class InputProcessor:
    @staticmethod
    def int(l_boundary: int, r_boundary: int, msg: str):
        result = float('inf')
        while result < l_boundary or result > r_boundary:
            result = int(input(msg))
        return result

    @staticmethod
    def matrix_size(msg=None):
        n_rows = n_columns = -1
        while n_rows <= 0 or n_columns <= 0:
            n_rows, n_columns = map(int, input(msg).split())
        return n_rows, n_columns

    @staticmethod
    def matrix(n_rows: int, n_columns: int) -> Matrix:
        result = list()
        for _ in range(n_rows):
            result.append(list(map(int, input().split()))[:n_columns])
        return Matrix(result)


def fit(first: Matrix, second: Matrix) -> tuple[Matrix, Matrix]:
    expand_size = 2
    while expand_size < max(n_rows_A, n_rows_B, n_cols_A, n_cols_B):
        expand_size *= 2
    result = (
        first.expand(expand_size, expand_size),
        second.expand(expand_size, expand_size),
    )
    return result


def solve(first: Matrix, second: Matrix) -> Matrix:
    A11, A12, A21, A22 = first.split_by_corners()
    B11, B12, B21, B22 = second.split_by_corners()

    D = (A11 + A22) * (B11 + B22)
    D1 = (A12 - A22) * (B21 + B22)
    D2 = (A21 - A11) * (B11 + B12)
    H1 = (A11 + A12) * B22
    H2 = (A21 + A22) * B11
    V1 = A22 * (B21 - B11)
    V2 = A11 * (B12 - B22)

    return Matrix.from_corners(
        D + D1 - H1 + V1,
        V2 + H1,
        V1 + H2,
        D + D2 + V2 - H2
    ).align()


if __name__ == '__main__':
    print('Вас приветствует программа\n'
          'быстрого перемножения матриц методом Штрассена\n')

    n_rows_A, n_cols_A = InputProcessor.matrix_size('Введите размеры первой матрицы\n')
    n_rows_B, n_cols_B = InputProcessor.matrix_size('Введите размеры второй матрицы\n')
    fill_type = InputProcessor.int(
        l_boundary=1,
        r_boundary=2,
        msg='Выберите способ заполнения матриц\n'
            '1 - Вручную \n'
            '2 - Случайным образом\n'
    )

    """Заполнение матриц."""
    match fill_type:
        case 1:
            A = InputProcessor.matrix(n_rows_A, n_cols_A)
            B = InputProcessor.matrix(n_rows_B, n_cols_B)

        case 2:
            A = Matrix.random(n_rows_A, n_cols_A, (1, 10))
            B = Matrix.random(n_rows_B, n_cols_B, (1, 10))

        case _:
            raise ValueError(f'{fill_type=} must be 1 or 2')

    print(f'\nМатрица 1:{A}')
    print(f'\nМатрица 2:{B}')

    A, B = fit(A, B)
    print('Приведенные матрицы\n')
    print(f'Матрица 1:\n{A}')
    print(f'\nМатрица 2:\n{B}')

    R = solve(A, B)
    print(f'\nРезультирующая матрица:{R}')
    assert np.all((R, (A * B).align()))
