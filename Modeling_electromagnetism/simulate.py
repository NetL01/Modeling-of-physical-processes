# simulate.py
import matplotlib.pyplot as plt
from physics_model import CoupledPendulums

# Настройка модели
model = CoupledPendulums(L=1.0, m=1.0, k=0.7, L1=0.5, beta=0.05)

# Начальные условия [φ1, dφ1/dt, φ2, dφ2/dt]
y0 = [0.2, 0.0, -0.2, 0.0]

# Решение
t, (phi1, vphi1, phi2, vphi2) = model.simulate(y0, t_span=(0, 20), steps=2000)

# Графики углов
plt.figure(figsize=(10, 5))
plt.plot(t, phi1, label='φ₁(t)', color='red')
plt.plot(t, phi2, label='φ₂(t)', color='blue')
plt.xlabel("Время (с)")
plt.ylabel("Угол (рад)")
plt.title("Углы маятников")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("angles.png")
plt.show()

# Графики угловых скоростей
plt.figure(figsize=(10, 5))
plt.plot(t, vphi1, label='dφ₁/dt', color='orange')
plt.plot(t, vphi2, label='dφ₂/dt', color='cyan')
plt.xlabel("Время (с)")
plt.ylabel("Скорость (рад/с)")
plt.title("Угловые скорости маятников")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("angular_velocities.png")
plt.show()
