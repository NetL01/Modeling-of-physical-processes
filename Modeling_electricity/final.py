import numpy as np
import matplotlib.pyplot as plt

class Electron:
    def __init__(self, v, r1, r2, l):
        self.x = 0
        self.y = (r2 - r1) / 2 + r1
        self.r1 = r1
        self.r2 = r2
        self.vx = v
        self.vy = 0
        self.q = -1.6e-19
        self.m = 9.1e-31
        self.l_ = l
        self.t = 0

    def aay(self, U):
        return (self.q * U) / (self.y * self.m)

    def motion_for_graphic(self, U):
        dt = 1e-12
        yx = []
        vy = []
        ay = []
        yt = []
        while self.x < self.l_ and self.y > self.r1 and self.t < 10:
            yx.append((self.x, self.y))
            vy.append((self.t, self.vy))
            dvy = self.aay(U)
            ay.append((self.t, dvy))
            yt.append((self.t, self.y))
            self.vy += dvy * dt
            self.y += self.vy * dt
            self.x += self.vx * dt
            self.t += dt
        return [yx, vy, ay, yt]

Umax = 1000
Umin = 0

while Umax - Umin > 1e-7:
    Electron_ = Electron(4.5e6, 0.05, 0.11, 0.19)
    U = (Umax + Umin) / 2
    yx, vy, ay, yt = Electron_.motion_for_graphic(U)
    if Electron_.x >= Electron_.l_:
        Umin = U
    else:
        Umax = U


print("Минимальное напряжение", U)
print("Время полета", Electron_.t)
print("Скорость конечная", (Electron_.vy ** 2 + Electron_.vx ** 2) ** 0.5)


plt.title('Зависимость высоты от расстояния')
plt.xlabel('Пройденное расстояние, м')
plt.ylabel('Высота, м')
plt.plot([i[0] for i in yx], [i[1] for i in yx])
plt.grid()
plt.savefig('y(x)')
plt.show()

plt.title('Зависимость скорости от времени')
plt.xlabel('Время, c')
plt.ylabel('Скорость, м/c')
plt.grid()
plt.plot([i[0] for i in vy], [i[1] for i in vy])
plt.savefig('Vy(t)')
plt.show()

plt.title('Зависимость ускорения от времени')
plt.xlabel('Время, c')
plt.ylabel('Ускорение, м/c^2')
plt.grid()
plt.plot([i[0] for i in ay], [i[1] for i in ay])
plt.savefig('ay(t)')
plt.show()

plt.title('Зависимость высоты от времени')
plt.xlabel('Время, с')
plt.ylabel('Высота, м')
plt.grid()
plt.plot([i[0] for i in yt], [i[1] for i in yt])
plt.savefig('y(t)')
plt.show()