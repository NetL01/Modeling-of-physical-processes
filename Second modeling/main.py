from math import sqrt
import numpy as np
from matplotlib import pyplot as plt

# Исходные данные
m_e = 9.1e-31  # масса электрона, кг
q_e = -1.6e-19  # заряд электрона, Кл
r = 0.05  # внутренний радиус конденсатора, м
R = 0.11  # внешний радиус конденсатора, м
V0 = 4.5e6  # начальная скорость электрона, м/с
L = 0.19  # длина конденсатора, м

# Теоретический расчетg

t = L/V0  # время полета, с
Umin = (pow((R-r), 2)/ pow(t, 2) * q_e) * m_e
V_kon = sqrt(pow(V0, 2) - (pow((R-r), 2) * pow(V0, 2))/pow(L, 2))  # конечная скорость электрона, м/с

V_values = np.linspace(0, Umin, 100)
t_values = L / V_values

# Ваши исходные данные и расчеты

# Расчет графиков зависимостей
t_values = np.linspace(0, t, 100)  # Задаем временной интервал для графиков

# График зависимости y(x)
x_values = V0 * t_values  # ускоренное движение, x = V0 * t
y_values = V0 * t_values - 0.5 * 9.8 * t_values**2  # уравнение равноускоренного движения

plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(x_values, y_values)
plt.title('y(x)')
plt.xlabel('x (м)')
plt.ylabel('y (м)')

# График зависимости Vy(t)
Vy_values = V0 - 9.8 * t_values
plt.subplot(2, 2, 2)
plt.plot(t_values, Vy_values)
plt.title('Vy(t)')
plt.xlabel('t (с)')
plt.ylabel('Vy (м/с)')

# График зависимости ay(t)
ay_values = -9.8 * np.ones_like(t_values)
plt.subplot(2, 2, 3)
plt.plot(t_values, ay_values)
plt.title('ay(t)')
plt.xlabel('t (с)')
plt.ylabel('ay (м/с^2)')

# График зависимости y(t)
y_values_t = V0 * t_values - 0.5 * 9.8 * t_values**2
plt.subplot(2, 2, 4)
plt.plot(t_values, y_values_t)
plt.title('y(t)')
plt.xlabel('t (с)')
plt.ylabel('y (м)')

plt.tight_layout()

# Вывод графиков
plt.show()

# Вывод значений теоретических данных
print(f"Минимальная разность потенциалов (U_min): {Umin:.2e} В")
print(f"Время полета при U_min (t_min): {t:.2e} с")
print(f"Конечная скорость электрона: {V_kon:.2e} м/с")