import random

n1, m1, n2, m2, k, l = 0, 0, 0, 0, 0, 2
print('Вас приветствует программа\n'
      'быстрого перемножения матриц методом Штрассена\n')

while n1 <= 0 or m1 <= 0:
    n1, m1 = map(int, input('Введите размеры первой матрицы\n').split())

while n2 <= 0 or m2 <= 0:
    n2, m2 = map(int, input('Введите размеры второй матрицы\n').split())

M1 = list()
for i in range(n1):
    M1.append([None] * m1)

M2 = list()
for i in range(n2):
    M2.append([None] * m2)

"""
    Выбор способа заполнения и заполнение матриц
"""

while k < 1 or k > 2:
    k = int(input('Выберите способ заполнения матриц\n'
                  '1 - Вручную \n'
                  '2 - Случайным образом\n'))

match k:
    case 1:
        for i in range(n1):
            for j in range(m1):
                M1[i][j] = int(input())

        for i in range(n2):
            for j in range(m2):
                M2[i][j] = int(input())

        print('\nМатрица 1\n')
        for i in range(n1):
            for j in range(m1):
                print(M1[i][j], end=' ')
            print()

        print('\nМатрица 2\n')
        for i in range(n2):
            for j in range(m2):
                print(M2[i][j], end=' ')
            print()

    case 2:
        for i in range(n1):
            for j in range(m1):
                M1[i][j] = random.randint(0, 10)
        for i in range(n2):
            for j in range(m2):
                M2[i][j] = random.randint(0, 10)

        print('\nМатрица 1\n')
        for i in range(n1):
            for j in range(m1):
                print(M1[i][j], end=' ')
            print()

        print('\nМатрица 2\n')
        for i in range(n2):
            for j in range(m2):
                print(M2[i][j], end=' ')
            print()

"""
    Приведение матриц к требуемому размеру
"""

while l < n1 or l < n2 or l < m1 or l < m2:
    l *= 2

M3 = list()
for i in range(l):
    M3.append([0] * l)

M4 = list()
for i in range(l):
    M4.append([0] * l)

for i in range(n1):
    for j in range(m1):
        M3[i][j] = M1[i][j]

for i in range(n2):
    for j in range(m2):
        M4[i][j] = M2[i][j]

print('Приведенные матрицы\n')

print('Матрица 1\n')
for i in range(l):
    for j in range(l):
        print(M3[i][j], end=' ')
    print()

print('Матрица 2\n')
for i in range(l):
    for j in range(l):
        print(M4[i][j], end=' ')
    print()

""" 
    Разбиение матриц на подматрицы и их заполнение
"""

mat1 = list()
for i in range(l // 2):
    mat1.append(M3[i][:l // 2])

mat2 = list()
for i in range(l // 2):
    mat2.append(M3[i][l // 2:])

mat3 = list()
for i in range(l // 2):
    mat3.append(list())
    for j in range(l // 2):
        mat3[i].append(M3[l // 2 + i][j])

mat4 = list()
for i in range(l // 2):
    mat4.append(list())
    for j in range(l // 2):
        mat4[i].append(M3[l // 2 + i][l // 2 + j])

mat5 = list()
for i in range(l // 2):
    mat5.append(M4[i][:l // 2])

mat6 = list()
for i in range(l // 2):
    mat6.append(M4[i][l // 2:])

mat7 = list()
for i in range(l // 2):
    mat7.append(list())
    for j in range(l // 2):
        mat7[i].append(M4[l // 2 + i][j])

mat8 = list()
for i in range(l // 2):
    mat8.append(list())
    for j in range(l // 2):
        mat8[i].append(M4[l // 2 + i][l // 2 + j])

"""
    Создание промежуточных матриц
"""

p1 = list()
for i in range(l // 2):
    p1.append([None] * (l // 2))

p2 = list()
for i in range(l // 2):
    p2.append([None] * (l // 2))

p3 = list()
for i in range(l // 2):
    p3.append([None] * (l // 2))

p4 = list()
for i in range(l // 2):
    p4.append([None] * (l // 2))

p5 = list()
for i in range(l // 2):
    p5.append([None] * (l // 2))

p6 = list()
for i in range(l // 2):
    p6.append([None] * (l // 2))

p7 = list()
for i in range(l // 2):
    p7.append([None] * (l // 2))

"""
    Вычисление значений промежуточных матриц
"""

for i in range(l // 2):
    for j in range(l // 2):
        p1[i][j] = 0
        for z in range(l // 2):
            p1[i][j] += (mat1[i][z] + mat4[i][z]) * (mat5[z][j] + mat8[z][j])

        p2[i][j] = 0
        for z in range(l // 2):
            p1[i][j] += (mat3[i][z] + mat4[i][z]) * mat5[z][j]

        p3[i][j] = 0
        for z in range(l // 2):
            p3[i][j] += mat1[i][z] * (mat4[i][z] -  mat8[z][j])

        p4[i][j] = 0
        for z in range(l // 2):
            p4[i][j] += mat4[i][z] * (mat7[z][j] - mat5[z][j])

        p5[i][j] = 0
        for z in range(l // 2):
            p5[i][j] += (mat1[i][z] + mat2[i][z]) * mat8[z][j]

        p6[i][j] = 0
        for z in range(l // 2):
            p6[i][j] += (mat3[i][z] - mat1[i][z]) * (mat5[z][j] + mat6[z][j])

        p7[i][j] = 0
        for z in range(l // 2):
            p7[i][j] += (mat2[i][z] - mat4[i][z]) * (mat7[z][j] + mat8[z][j])

"""
    Создание вспомогательных матриц
"""

mat9 = list()
for i in range(l // 2):
    mat9.append([None] * (l // 2))

mat10 = list()
for i in range(l // 2):
    mat10.append([None] * (l // 2))

mat11 = list()
for i in range(l // 2):
    mat11.append([None] * (l // 2))

mat12 = list()
for i in range(l // 2):
    mat12.append([None] * (l // 2))

"""
    Подсчет значений вспомогательных матриц из промежуточных
"""

for i in range(l // 2):
    for j in range(l // 2):
        mat9[i][j] = p1[i][j] + p4[i][j] - p5[i][j] + p7[i][j]
        mat10[i][j] = p3[i][j] + p5[i][j]
        mat11[i][j] = p2[i][j] + p4[i][j]
        mat12[i][j] = p1[i][j] - p2[i][j] + p3[i][j] + p6[i][j]

"""
    Создание результирующей матрицы
"""

M5 = list()
for i in range(l):
    M5.append([None] * l)

"""
    Занесение информации из вспомогательных матриц в результирующую
"""

for i in range(l // 2):
    for j in range(l // 2):
        M5[i][j] = mat9[i][j]
        M5[i][j + l // 2] = mat10[i][j]
        M5[i + l // 2][j] = mat11[i][j]
        M5[i + l // 2][j + l // 2] = mat12[i][j]

"""
    Выравнивание границ результирующей матрицы
"""

x, f, s = 0, 100, 100
for i in range(l):
    x = 0
    for j in range(l):
        if M5[i][j] != 0:
            x += 1
            f = 100
    if x == 0 and i < f:
        f = i

for i in range(l):
    x = 0
    for j in range(l):
        if M5[i][j] != 0:
            x += 1
            s = 100
    if x == 0 and i < s:
        s = i

M6 = list()
for i in range(f):
    M6.append(
        M5[i][:s]
    )

"""
    Вывод результирующей матрицы
"""

print('\nРезультирующая матрица\n')
for i in range(f):
    for j in range(s):
        print(M6[i][j], end=' ')
    print()

input('\n')
