# Тихомиров Дмитрий
# Уравнение теплопроводности


# N - количество узлов
# t_end - окончание по времени
# L - толщина пластины
# ro - плотность материала
# c - теплоёмкость материала
# lamda - коэффициент теплопроводности
# h - расчётный шаг сетки по координате
# T0 - начальная температура
# Tl - темература слева
# Tr - температура справа
# tau - расчётный шаг сетки
# alfa, beta - прогоночные коэффициенты по времени
# ai, bi, ci, fi - коэффициенты СЛАУ с трёхдиагональной матрицей
# time - счётчик времени
# T - массив со значениями температур
# h2 - h * h
# ct = c / tau
# TT - массив температуры на прошлом шаге
# Text - конечное значение температуры явным методом
# Timp - конечное значение температуры неявным методом
# a - выбор названия для файла
# s1, sT - для создания файла
# f -сам файл

import matplotlib
from matplotlib import  pyplot as plt


N = 500
t_end = 10
L = 0.1
ro = 7800
c = 460
lamda = 46
h = L / (N - 1)
tau = t_end / 100


T0 = input('Введите начальную температуру ')
while True:
    try:
        T0 = float(T0)
    except:
        print('Введите правильно данные')
        T0 = input('Введите начальную температуру ')
    else:
        break

Tl = input('Введите температуру слева ')
while True:
    try:
        Tl = float(Tl)
    except:
        print('Введите правильно данные ')
        Tl = input('Введите температуру слева ')
    else:
        break

Tr = input('Введите температуру справа ')
while True:
    try:
        Tr = float(Tr)
    except:
        print('Введите правильно данные ')
        Tr = input('Введите температуру справа ')
    else:
        break

# Функция, которая создаёт имя для файла

def name(T, N, a):
    for i in range(N):
        s2 = '.vtk'
        sT = a + str(i) + s2
        write_to_vtk1d(T, sT, N)



# Файл с расширением *.vtk должен начинаться на эти строчки
# В этой функции мы записываем в файл "кодовые строчки" и
# знвчения температур на промежутке

def write_to_vtk1d(T, sT, N):
    f = open(sT, 'w')
    f.write("# vtk DataFile Version 3.0\n")
    f.write("Plane\n")
    f.write("ASCII\n")
    f.write("DATASET STRUCTURED_POINTS\n")
    f.write("DIMENSIONS 10 1 1\n")
    f.write("ASPECT_RATIO 1 1 1\n")
    f.write("ORIGIN 0.0 0.0 0.0\n")
    f.write("POINT_DATA 10\n")
    f.write("SCALARS volume_scalars float 1\n")
    f.write("LOOKUP_TABLE default")
    for i in range(N):
        f.write("\n" + str(T[i]))
    f.close()


# Функция, которая считает явным методом
def explicit(h, N, t_end, Tl, Tr, lamda, ro, c):
    name_file = "T"  # Имя файлов в явном методе будет начинаться на "Т"
    T = [T0] * N # Задаем начальную температуру

    # Прогоночные коэффицианты

    alfa = [0] * N
    beta = [0] * N
    time = 0

    # По шагу времени расчитываем значения температур, используя формулы (2)

    while time < t_end:
        time += tau
        alfa[0] = 0
        beta[0] = Tl
        for i in range(1, N - 1):
            h2 = h * h
            ct = c / tau
            ai = ci = lamda / h2
            bi = 2 * lamda / h2 + ro * ct
            fi = -ro * ct * T[i]
            alfa[i] = ai / (bi - ci * alfa[i - 1])
            beta[i] = (ci * beta[i - 1] - fi) / (bi - ci * alfa[i - 1])
        T[N - 1] = Tr
        T[0] = Tl

        # Вычисляем значение температур

        for i in range(N - 2, 0, -1):
            T[i] = alfa[i] * T[i + 1] + beta[i]

    # Создаем файл и записываем в него полученные данные

    name(T, N, name_file)
    return T


# Функция для неявного метода

def implicit(h, N, t_end, Tl, Tr, lamda, ro, c):
    name_file = "U" # Имя файлов в неявном методе будет начинаться на "U"
    a = lamda / ro / c
    tau = 0.25 * h * h / a
    T = [T0] * N
    T[0] = Tl
    T[N - 1] = Tr
    time = 0
    TT = [0] * N
    while time < t_end:
        time += tau
        for i in range(N):
            TT[i] = T[i] # Запоминаем предыдущее значение температуры


        # Через предыдущее и ныненшнее значени вычисляем температуру на данном участке

        for i in range(1, N - 1):
            h2 = h * h
            T[i] = TT[i] + a * tau / h2 * (TT[i + 1] - 2 * TT[i] + TT[i - 1])
    # Создаем файл и записываем в него полученные данные

    name(T, N, name_file)
    return T

# Сохраняем значение температур

Texp = explicit(h, N, t_end, Tl, Tr, lamda, ro, c)
Timp = implicit(h, N, t_end, Tl, Tr, lamda, ro, c)


# Выводим по столбикам для сравнения

print('\t{:2.15}'.format('Явный метод'), '\t\t', '{:6.16}'.format('Неявный метод'))
for i in range(N):
    print('{:2.15f}'.format(Texp[i]), '\t', end=' ')
    print('{:2.15f}'.format(Timp[i]))

