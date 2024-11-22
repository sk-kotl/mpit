import pygame
import sys
import random
import math

pygame.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 920
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Эмуляция полета дрона")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DRONE_COLOR = (0, 150, 255)
POINT_COLOR = (255, 100, 100)
CIRCLE_COLOR = (0, 200, 0)

drone_size = 20
drone_speed = 2 
drone_range_initial = 100  
drone_range_final = 350 

point1_range = 250 
point2_range = 500
point_radius = 10

def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def generate_points(min_distance):
    while True:
        p1 = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        p2 = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        if calculate_distance(p1, p2) >= min_distance:
            return p1, p2

point1, point2 = generate_points(500)
drone_pos = point1[:]  

font = pygame.font.Font(None, 36)

def draw_dashed_circle(surface, color, center, radius, dash_length=5):
    for angle in range(0, 360, dash_length * 2):
        start_angle = math.radians(angle)
        end_angle = math.radians(angle + dash_length)
        x1 = center[0] + radius * math.cos(start_angle)
        y1 = center[1] + radius * math.sin(start_angle)
        x2 = center[0] + radius * math.cos(end_angle)
        y2 = center[1] + radius * math.sin(end_angle)
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 1)

def find_optimal_position():
    best_pos = drone_pos[:]
    min_diff = float('inf')

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

clock = pygame.time.Clock()
running = True
found_second_signal = False
drone_range = drone_range_initial  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not found_second_signal:
        if drone_pos[0] < point2[0]:
            drone_pos[0] += drone_speed
        elif drone_pos[0] > point2[0]:
            drone_pos[0] -= drone_speed
        
        if drone_pos[1] < point2[1]:
            drone_pos[1] += drone_speed
        elif drone_pos[1] > point2[1]:
            drone_pos[1] -= drone_speed

        if calculate_distance(drone_pos, point2) <= point2_range:
            found_second_signal = True
            drone_range = drone_range_final
    else:
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

    distance_to_point1 = calculate_distance(drone_pos, point1)
    distance_to_point2 = calculate_distance(drone_pos, point2)

    screen.fill(WHITE)
    
    pygame.draw.rect(screen, DRONE_COLOR, (*drone_pos, drone_size, drone_size))
    
    pygame.draw.circle(screen, POINT_COLOR, point1, point_radius)
    pygame.draw.circle(screen, POINT_COLOR, point2, point_radius)

    draw_dashed_circle(screen, CIRCLE_COLOR, drone_pos, drone_range)
    draw_dashed_circle(screen, CIRCLE_COLOR, point1, point1_range)
    draw_dashed_circle(screen, CIRCLE_COLOR, point2, point2_range)

    text1 = font.render(f"До точки 1: {distance_to_point1:.2f} м", True, BLACK)
    text2 = font.render(f"До точки 2: {distance_to_point2:.2f} м", True, BLACK)
    text_point1 = font.render(f"Точка 1: {point1}", True, BLACK)
    text_point2 = font.render(f"Точка 2: {point2}", True, BLACK)
    text_status = font.render(
        "Ищет сигнал второй точки..." if not found_second_signal else "Находится в оптимальном месте",
        True,
        BLACK,
    )
    
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 50))
    screen.blit(text_point1, (10, 90))
    screen.blit(text_point2, (10, 130))
    screen.blit(text_status, (10, 170))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
