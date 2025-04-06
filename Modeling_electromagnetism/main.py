import pygame
import numpy as np
from physics_model import CoupledPendulums

# --- Настройки физики ---
model = CoupledPendulums(L=1.0, m=1.0, k=0.7, L1=0.5, beta=0.05)
y0 = [0.2, 0.0, -0.2, 0.0]
t_vals, (phi1_arr, vphi1_arr, phi2_arr, vphi2_arr) = model.simulate(y0, t_span=(0, 20), steps=2000)

# --- Настройки Pygame ---
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Связанные маятники с графиками")
font = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()
FPS = 60

# --- Координаты маятников ---
L_pixels = 200
origin1 = (WIDTH // 2 - 100, 100)
origin2 = (WIDTH // 2 + 100, 100)

# --- Память для графиков ---
phi1_history = []
phi2_history = []
vphi1_history = []
vphi2_history = []
time_history = []

# --- Цвета ---
RED, BLUE, GREEN, ORANGE, WHITE, BLACK = (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 165, 0), (255, 255, 255), (0, 0, 0)

# --- Оси графиков ---
GRAPH_WIDTH = 400
GRAPH_HEIGHT = 150
graph_origin_angles = (50, HEIGHT - 320)
graph_origin_vel = (50, HEIGHT - 150)

# --- Основной цикл ---
running = True
i = 0

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # --- Рисуем маятники ---
    x1 = origin1[0] + L_pixels * np.sin(phi1)
    y1 = origin1[1] + L_pixels * np.cos(phi1)
    x2 = origin2[0] + L_pixels * np.sin(phi2)
    y2 = origin2[1] + L_pixels * np.cos(phi2)

    pygame.draw.line(screen, WHITE, origin1, (x1, y1), 2)
    pygame.draw.line(screen, WHITE, origin2, (x2, y2), 2)
    pygame.draw.circle(screen, RED, (int(x1), int(y1)), 10)
    pygame.draw.circle(screen, BLUE, (int(x2), int(y2)), 10)
    pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 2)

    # --- Тексты ---
    screen.blit(font.render(f"φ₁ = {phi1:.2f} рад", True, WHITE), (WIDTH - 250, 50))
    screen.blit(font.render(f"φ₂ = {phi2:.2f} рад", True, WHITE), (WIDTH - 250, 80))
    screen.blit(font.render(f"t = {t:.2f} с", True, WHITE), (WIDTH - 250, 110))

    # --- График углов ---
    pygame.draw.rect(screen, (40, 40, 40), (*graph_origin_angles, GRAPH_WIDTH, GRAPH_HEIGHT), border_radius=8)
    for idx in range(1, len(phi1_history)):
        x_prev = graph_origin_angles[0] + idx - 1
        x_curr = graph_origin_angles[0] + idx
        y_phi1_prev = graph_origin_angles[1] + GRAPH_HEIGHT / 2 - phi1_history[idx - 1] * 100
        y_phi1_curr = graph_origin_angles[1] + GRAPH_HEIGHT / 2 - phi1_history[idx] * 100
        y_phi2_prev = graph_origin_angles[1] + GRAPH_HEIGHT / 2 - phi2_history[idx - 1] * 100
        y_phi2_curr = graph_origin_angles[1] + GRAPH_HEIGHT / 2 - phi2_history[idx] * 100

        pygame.draw.line(screen, RED, (x_prev, y_phi1_prev), (x_curr, y_phi1_curr), 2)
        pygame.draw.line(screen, BLUE, (x_prev, y_phi2_prev), (x_curr, y_phi2_curr), 2)
    screen.blit(font.render("φ₁ / φ₂", True, WHITE), (graph_origin_angles[0], graph_origin_angles[1] - 20))

    # --- График скоростей ---
    pygame.draw.rect(screen, (40, 40, 40), (*graph_origin_vel, GRAPH_WIDTH, GRAPH_HEIGHT), border_radius=8)
    for idx in range(1, len(vphi1_history)):
        x_prev = graph_origin_vel[0] + idx - 1
        x_curr = graph_origin_vel[0] + idx
        y_vphi1_prev = graph_origin_vel[1] + GRAPH_HEIGHT / 2 - vphi1_history[idx - 1] * 50
        y_vphi1_curr = graph_origin_vel[1] + GRAPH_HEIGHT / 2 - vphi1_history[idx] * 50
        y_vphi2_prev = graph_origin_vel[1] + GRAPH_HEIGHT / 2 - vphi2_history[idx - 1] * 50
        y_vphi2_curr = graph_origin_vel[1] + GRAPH_HEIGHT / 2 - vphi2_history[idx] * 50

        pygame.draw.line(screen, ORANGE, (x_prev, y_vphi1_prev), (x_curr, y_vphi1_curr), 2)
        pygame.draw.line(screen, GREEN, (x_prev, y_vphi2_prev), (x_curr, y_vphi2_curr), 2)
    screen.blit(font.render("dφ₁/dt / dφ₂/dt", True, WHITE), (graph_origin_vel[0], graph_origin_vel[1] - 20))

    # --- Обновление экрана ---
    pygame.display.flip()

pygame.quit()
