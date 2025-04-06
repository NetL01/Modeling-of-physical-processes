import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Физические параметры
g = 9.81      # ускорение свободного падения
L = 1.0       # длина маятников (м)
m = 1.0       # масса маятников (кг)
k = 0.5       # жесткость пружины (Н/м)
L1 = 0.5      # расстояние от подвеса до пружины (м)
beta = 0.05   # коэффициент затухания

# Начальные условия
phi1_0 = 0.2     # начальный угол маятника 1
vphi1_0 = 0.0    # начальная скорость маятника 1
phi2_0 = -0.2    # начальный угол маятника 2
vphi2_0 = 0.0    # начальная скорость маятника 2

# Начальный вектор состояния
y0 = [phi1_0, vphi1_0, phi2_0, vphi2_0]

# Система уравнений
def derivatives(t, y):
    phi1, vphi1, phi2, vphi2 = y
    dphi1 = vphi1
    dvphi1 = -2*beta*vphi1 - (g/L)*phi1 + (k*L1**2)/(m*L**2)*(phi2 - phi1)
    dphi2 = vphi2
    dvphi2 = -2*beta*vphi2 - (g/L)*phi2 + (k*L1**2)/(m*L**2)*(phi1 - phi2)
    return [dphi1, dvphi1, dphi2, dvphi2]

# Время симуляции
t_span = (0, 20)
t_eval = np.linspace(*t_span, 2000)

# Решение
sol = solve_ivp(derivatives, t_span, y0, t_eval=t_eval)

# Разделим результат
t = sol.t
phi1, vphi1, phi2, vphi2 = sol.y
