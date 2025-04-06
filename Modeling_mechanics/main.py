import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
wall_collision_count = 0
collision_count = 0
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BROWN = (150, 75, 0)
# Массы и начальные скорости
n = 1.5
m1 = 3
m2 = m1*pow(10, n)
v1 = 0
v2 = -1
x1, y1 = WIDTH // 4, HEIGHT // 2
x2, y2 = 3 * WIDTH // 4, HEIGHT // 2
e = 1.0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Абсолютно упругое взаимодействие")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    rect0 = pygame.draw.rect(screen, RED, (x1, y1, 35, 35))
    rect1 = pygame.draw.rect(screen, RED, (x2, y2 - 15, 50, 50))
    wall = pygame.draw.rect(screen, BROWN, (50, 50, 20, HEIGHT))
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - 265, WIDTH, 10))

    if rect0.colliderect(rect1):
        v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

        v1 = v1_final * e
        v2 = v2_final * e

        collision_count += 1
        print('detact')
    if wall.colliderect(rect0):
        v1 = -v1 * e
        wall_collision_count += 1

    if wall.colliderect(rect1):
        v2 = -v2 * e

    x1 += v1
    x2 += v2
    if v2 >= 0:
        print('Тело массой m2 прекратило своё движение в отрицательном направлении.')
        print('--------------------------------------------------------------------')
        print(f'm1 = {m1}, m2 = {m2}, n = {n}')
        print(f'Столкновений со стеной: {wall_collision_count}  ////// Столкновений между двумя телами: {collision_count-2}')
        break
    pygame.display.flip()
    clock.tick(50)