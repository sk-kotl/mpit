import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 925
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Эмуляция полета дрона")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DRONE_COLOR = (0, 150, 255)
POINT_COLOR = (255, 100, 100)
CIRCLE_COLOR = (0, 200, 0)

# Параметры дрона
drone_size = 20
drone_speed = 2  # Скорость движения дрона
drone_range = 200  # Радиус действия дрона (2 км)

# Радиусы действия точек
point1_range = 250  # Радиус 2.5 км
point2_range = 500  # Радиус 5 км
point_radius = 10

# Функция для вычисления расстояния
def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# Генерация случайных точек с минимальным расстоянием между ними
def generate_points(min_distance):
    while True:
        p1 = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        p2 = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        if calculate_distance(p1, p2) >= min_distance:
            return p1, p2

point1, point2 = generate_points(500)
drone_pos = point1[:]  # Дрон начинает движение от первой точки

# Шрифт для текста
font = pygame.font.Font(None, 36)

# Функция для рисования пунктирного круга
def draw_dashed_circle(surface, color, center, radius, dash_length=5):
    for angle in range(0, 360, dash_length * 2):
        start_angle = math.radians(angle)
        end_angle = math.radians(angle + dash_length)
        x1 = center[0] + radius * math.cos(start_angle)
        y1 = center[1] + radius * math.sin(start_angle)
        x2 = center[0] + radius * math.cos(end_angle)
        y2 = center[1] + radius * math.sin(end_angle)
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 1)

# Оптимальная позиция
def find_optimal_position():
    best_pos = drone_pos[:]
    min_diff = float('inf')

    # Сканируем область вокруг точек
    for x in range(0, SCREEN_WIDTH, 10):
        for y in range(0, SCREEN_HEIGHT, 10):
            dist1 = calculate_distance((x, y), point1)
            dist2 = calculate_distance((x, y), point2)
            if dist1 <= point1_range and dist2 <= point2_range:
                diff = abs(dist1 - dist2)
                if diff < min_diff:
                    min_diff = diff
                    best_pos = [x, y]
    return best_pos

# Цикл игры
clock = pygame.time.Clock()
running = True
found_second_signal = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not found_second_signal:
        # Дрон летит к точке 2 по обеим координатам
        if drone_pos[0] < point2[0]:
            drone_pos[0] += drone_speed
        elif drone_pos[0] > point2[0]:
            drone_pos[0] -= drone_speed
        
        if drone_pos[1] < point2[1]:
            drone_pos[1] += drone_speed
        elif drone_pos[1] > point2[1]:
            drone_pos[1] -= drone_speed

        # Проверка, входит ли дрон в радиус второй точки
        if calculate_distance(drone_pos, point2) <= point2_range:
            found_second_signal = True
    else:
        # Дрон перемещается к оптимальному месту
        optimal_pos = find_optimal_position()
        if calculate_distance(drone_pos, optimal_pos) > drone_speed:
            if drone_pos[0] < optimal_pos[0]:
                drone_pos[0] += drone_speed
            elif drone_pos[0] > optimal_pos[0]:
                drone_pos[0] -= drone_speed

            if drone_pos[1] < optimal_pos[1]:
                drone_pos[1] += drone_speed
            elif drone_pos[1] > optimal_pos[1]:
                drone_pos[1] -= drone_speed

    # Вычисление расстояний
    distance_to_point1 = calculate_distance(drone_pos, point1)
    distance_to_point2 = calculate_distance(drone_pos, point2)

    # Мощность от каждой точки (обратная пропорция от расстояния)
    power_from_point1 = max(0, 1 / distance_to_point1) if distance_to_point1 != 0 else 1  # Избегаем деления на 0
    power_from_point2 = max(0, 1 / distance_to_point2) if distance_to_point2 != 0 else 1

    # Отрисовка
    screen.fill(WHITE)
    
    # Отрисовка дрона
    pygame.draw.rect(screen, DRONE_COLOR, (*drone_pos, drone_size, drone_size))
    
    # Отрисовка точек
    pygame.draw.circle(screen, POINT_COLOR, point1, point_radius)
    pygame.draw.circle(screen, POINT_COLOR, point2, point_radius)

    # Отрисовка пунктирных кругов
    draw_dashed_circle(screen, CIRCLE_COLOR, drone_pos, drone_range)
    draw_dashed_circle(screen, CIRCLE_COLOR, point1, point1_range)
    draw_dashed_circle(screen, CIRCLE_COLOR, point2, point2_range)

    # Отображение расстояний и мощностей
    text1 = font.render(f"До точки 1: {distance_to_point1:.2f} м", True, BLACK)
    text2 = font.render(f"До точки 2: {distance_to_point2:.2f} м", True, BLACK)
    text_power1 = font.render(f"Мощность от точки 1: {power_from_point1:.2f}", True, BLACK)
    text_power2 = font.render(f"Мощность от точки 2: {power_from_point2:.2f}", True, BLACK)
    text_point1 = font.render(f"Точка 1: {point1}", True, BLACK)
    text_point2 = font.render(f"Точка 2: {point2}", True, BLACK)
    text_status = font.render(
        "Ищет сигнал второй точки..." if not found_second_signal else "Находится в оптимальном месте",
        True,
        BLACK,
    )
    
    # Отображение текста на экране
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 50))
    screen.blit(text_power1, (10, 90))
    screen.blit(text_power2, (10, 130))
    screen.blit(text_point1, (10, 170))
    screen.blit(text_point2, (10, 210))
    screen.blit(text_status, (10, 250))

    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

pygame.quit()
sys.exit()
