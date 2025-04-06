# Моделирование связанных маятников с визуализацией, графиками, GUI и экспортом
import pygame
import numpy as np
import os
from physics_model import CoupledPendulums
import tkinter as tk
from tkinter import simpledialog

# === GUI для ввода параметров ===
def get_simulation_parameters():
    root = tk.Tk()
    root.withdraw()  # Скрыть окно

    params = {
        'L': float(simpledialog.askstring("Параметр", "Длина маятника L (м)", initialvalue='1.0')),
        'm': float(simpledialog.askstring("Параметр", "Масса m (кг)", initialvalue='1.0')),
        'k': float(simpledialog.askstring("Параметр", "Жесткость пружины k (Н/м)", initialvalue='0.7')),
        'L1': float(simpledialog.askstring("Параметр", "Точка крепления пружины L1 (м)", initialvalue='0.5')),
        'beta': float(simpledialog.askstring("Параметр", "Коэффициент затухания β", initialvalue='0.05')),
        'phi1_0': float(simpledialog.askstring("Начальные условия", "Начальный угол φ1 (рад)", initialvalue='0.2')),
        'phi2_0': float(simpledialog.askstring("Начальные условия", "Начальный угол φ2 (рад)", initialvalue='-0.2')),
    }
    return params

# Получаем параметры от пользователя
params = get_simulation_parameters()

# === Физическая модель ===
model = CoupledPendulums(L=params['L'], m=params['m'], k=params['k'], L1=params['L1'], beta=params['beta'])
y0 = [params['phi1_0'], 0.0, params['phi2_0'], 0.0]
t_vals, (phi1_arr, vphi1_arr, phi2_arr, vphi2_arr) = model.simulate(y0, t_span=(0, 20), steps=2000)

# === Pygame ===
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Связанные маятники")
font = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()
FPS = 180

# === Визуальные параметры ===
L_pixels = 200
origin1 = (WIDTH // 2 - 100, 150)
origin2 = (WIDTH // 2 + 100, 150)

# === Буферы ===
phi1_history, phi2_history = [], []
vphi1_history, vphi2_history = [], []
time_history = []

# === Настройки отображения ===
show_graphs = True
show_phase = True
export_frames = True
frame_dir = "frames"
os.makedirs(frame_dir, exist_ok=True)
frame_count = 0

# === Цвета ===
RED, BLUE, GREEN, ORANGE, WHITE, BLACK, GRAY = (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 165, 0), (255, 255, 255), (0, 0, 0), (80, 80, 80)

# === Координаты графиков ===
graph_origin_angles = (50, HEIGHT - 300)
graph_origin_vel = (50, HEIGHT - 140)
graph_origin_phase1 = (600, HEIGHT - 300)
graph_origin_phase2 = (600, HEIGHT - 140)
GRAPH_WIDTH = 500
GRAPH_HEIGHT = 120

# === Основной цикл ===
running = True
i = 0
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                show_graphs = not show_graphs
            if event.key == pygame.K_f:
                show_phase = not show_phase

    if i < len(t_vals):
        phi1 = phi1_arr[i]
        phi2 = phi2_arr[i]
        vphi1 = vphi1_arr[i]
        vphi2 = vphi2_arr[i]
        t = t_vals[i]

        phi1_history.append(phi1)
        phi2_history.append(phi2)
        vphi1_history.append(vphi1)
        vphi2_history.append(vphi2)
        time_history.append(t)

        if len(phi1_history) > GRAPH_WIDTH:
            phi1_history.pop(0)
            phi2_history.pop(0)
            vphi1_history.pop(0)
            vphi2_history.pop(0)
            time_history.pop(0)

        i += 1
    else:
        i = 0
        phi1_history.clear()
        phi2_history.clear()
        vphi1_history.clear()
        vphi2_history.clear()
        time_history.clear()

    # Маятники
    x1 = origin1[0] + L_pixels * np.sin(phi1)
    y1 = origin1[1] + L_pixels * np.cos(phi1)
    x2 = origin2[0] + L_pixels * np.sin(phi2)
    y2 = origin2[1] + L_pixels * np.cos(phi2)

    pygame.draw.line(screen, WHITE, origin1, (x1, y1), 2)
    pygame.draw.line(screen, WHITE, origin2, (x2, y2), 2)
    pygame.draw.circle(screen, RED, (int(x1), int(y1)), 10)
    pygame.draw.circle(screen, BLUE, (int(x2), int(y2)), 10)
    pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 2)

    screen.blit(font.render(f"t = {t:.2f} с", True, WHITE), (WIDTH - 200, 30))

    # Графики углов и скоростей
    def draw_graph(data1, data2, origin, label, scale=100, color1=RED, color2=BLUE):
        pygame.draw.rect(screen, (30, 30, 30), (*origin, GRAPH_WIDTH, GRAPH_HEIGHT))
        for x in range(0, GRAPH_WIDTH, 50):
            pygame.draw.line(screen, GRAY, (origin[0] + x, origin[1]), (origin[0] + x, origin[1] + GRAPH_HEIGHT))
        pygame.draw.line(screen, GRAY, (origin[0], origin[1] + GRAPH_HEIGHT / 2), (origin[0] + GRAPH_WIDTH, origin[1] + GRAPH_HEIGHT / 2))
        for j in range(1, len(data1)):
            pygame.draw.line(screen, color1,
                             (origin[0] + j - 1, origin[1] + GRAPH_HEIGHT / 2 - data1[j - 1] * scale),
                             (origin[0] + j, origin[1] + GRAPH_HEIGHT / 2 - data1[j] * scale), 2)
            pygame.draw.line(screen, color2,
                             (origin[0] + j - 1, origin[1] + GRAPH_HEIGHT / 2 - data2[j - 1] * scale),
                             (origin[0] + j, origin[1] + GRAPH_HEIGHT / 2 - data2[j] * scale), 2)
        screen.blit(font.render(label, True, WHITE), (origin[0], origin[1] - 20))

    if show_graphs:
        draw_graph(phi1_history, phi2_history, graph_origin_angles, "φ₁ / φ₂", scale=100)
        draw_graph(vphi1_history, vphi2_history, graph_origin_vel, "dφ₁/dt / dφ₂/dt", scale=50, color1=ORANGE, color2=GREEN)

    if show_phase:
        draw_graph(phi1_history, vphi1_history, graph_origin_phase1, "Фаза φ₁/dφ₁", scale=80)
        draw_graph(phi2_history, vphi2_history, graph_origin_phase2, "Фаза φ₂/dφ₂", scale=80, color1=ORANGE, color2=GREEN)

    pygame.display.flip()

    # Экспорт кадров
    if export_frames:
        pygame.image.save(screen, os.path.join(frame_dir, f"frame_{frame_count:04d}.png"))
        frame_count += 1

pygame.quit()

# === Видео можно собрать отдельно через ffmpeg ===
# ffmpeg -framerate 60 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
