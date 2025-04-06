"""
physics_model.py

Физическая модель связанных математических маятников с пружиной.

Описание:
Два одинаковых маятника (длины L, массы m), соединены пружиной жёсткости k,
которая закреплена на расстоянии L1 от точки подвеса. Присутствует затухание
с коэффициентом β. Модель построена в линейном приближении для малых углов.

Используемые уравнения:
Уравнения движения:
    d²φ₁/dt² + 2β dφ₁/dt + (g/L) φ₁ - (k·L1²)/(m·L²)·(φ₂ - φ₁) = 0
    d²φ₂/dt² + 2β dφ₂/dt + (g/L) φ₂ - (k·L1²)/(m·L²)·(φ₁ - φ₂) = 0

Преобразовано в систему первого порядка для численного интегрирования.
"""

import numpy as np
from scipy.integrate import solve_ivp

class CoupledPendulums:
    def __init__(self, L=1.0, m=1.0, k=0.5, L1=0.5, beta=0.05, g=9.81):
        """
        Параметры маятников:
        L    — длина маятника (м)
        m    — масса (кг)
        k    — жесткость пружины (Н/м)
        L1   — расстояние от точки крепления маятника до пружины (м)
        beta — коэффициент затухания
        g    — ускорение свободного падения
        """
        self.L = L
        self.m = m
        self.k = k
        self.L1 = L1
        self.beta = beta
        self.g = g

    def derivatives(self, t, y):
        """
        Система ОДУ:
        y = [φ₁, dφ₁/dt, φ₂, dφ₂/dt]
        Возвращает dy/dt
        """
        φ1, dφ1, φ2, dφ2 = y
        L, m, k, L1, beta, g = self.L, self.m, self.k, self.L1, self.beta, self.g

        dφ1_dt = dφ1
        ddφ1_dt = -2 * beta * dφ1 - (g / L) * φ1 + (k * L1 ** 2) / (m * L ** 2) * (φ2 - φ1)

        dφ2_dt = dφ2
        ddφ2_dt = -2 * beta * dφ2 - (g / L) * φ2 + (k * L1 ** 2) / (m * L ** 2) * (φ1 - φ2)

        return [dφ1_dt, ddφ1_dt, dφ2_dt, ddφ2_dt]

    def simulate(self, y0, t_span=(0, 20), steps=2000):
        """
        Решение системы ОДУ методом solve_ivp

        Аргументы:
        y0     — начальные условия [φ1, dφ1, φ2, dφ2]
        t_span — кортеж (t_start, t_end)
        steps  — количество шагов по времени

        Возвращает:
        t — массив времени
        sol.y — массив [φ₁(t), dφ₁/dt(t), φ₂(t), dφ₂/dt(t)]
        """
        t_eval = np.linspace(*t_span, steps)
        sol = solve_ivp(self.derivatives, t_span, y0, t_eval=t_eval)
        return sol.t, sol.y
