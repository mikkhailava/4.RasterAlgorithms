import pygame
import math

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Растровые алгоритмы")
font = pygame.font.SysFont('Arial', 18)


def draw_grid():
    screen.fill(WHITE)
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)


def to_screen_coords(x, y):
    """Преобразование дискретных координат в экранные"""
    screen_x = WIDTH // 2 + x * GRID_SIZE
    screen_y = HEIGHT // 2 - y * GRID_SIZE
    return screen_x, screen_y


def to_grid_coords(screen_x, screen_y):
    """Преобразование экранных координат в дискретные"""
    x = (screen_x - WIDTH // 2) // GRID_SIZE
    y = (HEIGHT // 2 - screen_y) // GRID_SIZE
    return x, y


def step_by_step(x0, y0, x1, y1):
    points = []
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x0, y0
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    return points


def dda(x0, y0, x1, y1):
    return step_by_step(x0, y0, x1, y1)  


def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points


def bresenham_circle(x0, y0, radius):
    points = []
    x = 0
    y = radius
    d = 3 - 2 * radius
    while x <= y:
        points.extend([
            (x0 + x, y0 + y), (x0 - x, y0 + y), (x0 + x, y0 - y), (x0 - x, y0 - y),
            (x0 + y, y0 + x), (x0 - y, y0 + x), (x0 + y, y0 - x), (x0 - y, y0 - x)
        ])
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    return points


def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def main():
    running = True
    current_algorithm = "Пошаговый"
    points = []
    x0, y0, x1, y1, radius = 0, 0, 0, 0, 0

    while running:
        draw_grid()
        draw_text(f"Алгоритм: {current_algorithm}", 10, 10)
        draw_text("Управление:", 10, 40)
        draw_text("1 - Пошаговый, 2 - ЦДА, 3 - Брезенхем (линия), 4 - Брезенхем (окружность)", 10, 60)
        draw_text("ЛКМ - задать начальную/конечную точку или радиус окружности", 10, 80)
        draw_text("C - очистить экран", 10, 100)
        draw_text(f"Точки: ({x0}, {y0}) -> ({x1}, {y1}) Радиус: {radius}", 10, 120)

        for point in points:
            pygame.draw.circle(screen, RED, to_screen_coords(*point), 3)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_algorithm = "Пошаговый"
                elif event.key == pygame.K_2:
                    current_algorithm = "ЦДА"
                elif event.key == pygame.K_3:
                    current_algorithm = "Брезенхем (линия)"
                elif event.key == pygame.K_4:
                    current_algorithm = "Брезенхем (окружность)"
                elif event.key == pygame.K_c:
                   points = []
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                gx, gy = to_grid_coords(mx, my)
                if event.button == 1:  # ЛКМ
                    if current_algorithm == "Брезенхем (окружность)":
                        x0, y0 = gx, gy
                        radius = abs(x1 - x0) + abs(y1 - y0)
                        points = bresenham_circle(x0, y0, radius)
                    else:
                        if not points:
                            x0, y0 = gx, gy
                        else:
                            x1, y1 = gx, gy
                            if current_algorithm == "Пошаговый":
                                points = step_by_step(x0, y0, x1, y1)
                            elif current_algorithm == "ЦДА":
                                points = dda(x0, y0, x1, y1)
                            elif current_algorithm == "Брезенхем (линия)":
                                points = bresenham_line(x0, y0, x1, y1)

    pygame.quit()


if name == "__main__":
    main()
