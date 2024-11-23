import pygame
import sys
import math
import random

i = 0
sinr_sum = 0
sinr_viv = 0
shoom_sum = 0 
shoom_viv = 0
d = 0

pygame.init()

# Настройки экрана
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 920
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
drone_speed = 2
drone_range_initial = 100
drone_range_final = 350

# Радиусы действия точек
point1_range = 250
point2_range = 250
point_radius = 10

def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

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

point1 = None
point2 = None
drone_pos = None
selecting_points = True
found_second_signal = False
drone_range = drone_range_initial

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if selecting_points and event.type == pygame.MOUSEBUTTONDOWN:
            if not point1:
                point1 = list(event.pos)
            elif not point2:
                point2 = list(event.pos)
                drone_pos = point1[:]
                selecting_points = False

    if not selecting_points:
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

    screen.fill(WHITE)

    # Отображение точек
    if point1:
        pygame.draw.circle(screen, POINT_COLOR, point1, point_radius)
        text_point1 = font.render(f"Геолог 1", True, BLACK) # 
        screen.blit(text_point1, (point1[0] + 10, point1[1] - 10))
        text_point1 = font.render(f"({point1[0]}, {point1[1]})", True, BLACK) # 
        screen.blit(text_point1, (point1[0] + 10, point1[1] + 15))

    if point2:
        pygame.draw.circle(screen, POINT_COLOR, point2, point_radius)
        text_point2 = font.render(f"Геолог 2", True, BLACK) # 
        screen.blit(text_point2, (point2[0] + 10, point2[1] - 10))
        text_point2 = font.render(f"({point2[0]}, {point2[1]})", True, BLACK) # 
        screen.blit(text_point2, (point2[0] + 10, point2[1] + 15))

    if drone_pos:
        # Отображение дрона и текста
        pygame.draw.rect(screen, DRONE_COLOR, (*drone_pos, drone_size, drone_size))
        draw_dashed_circle(screen, CIRCLE_COLOR, drone_pos, drone_range)
        
        text_drone = font.render("Дрон", True, BLACK)
        screen.blit(text_drone, (drone_pos[0] + drone_size + 5, drone_pos[1] - 10)) 


    if point1:
        draw_dashed_circle(screen, CIRCLE_COLOR, point1, point1_range)
    if point2:
        draw_dashed_circle(screen, CIRCLE_COLOR, point2, point2_range)

    # Вычисление расстояний от дрона до точек
    if drone_pos and point1:
        distance_to_point1 = calculate_distance(drone_pos, point1)
    else:
        distance_to_point1 = None

    if drone_pos and point2:
        distance_to_point2 = calculate_distance(drone_pos, point2)
    else:
        distance_to_point2 = None

    # Отображение координат точек и расстояний в верхнем левом углу
    info_y = 50  # Начальная вертикальная позиция для информации
    # if point1:
    #     coord_text1 = font.render(f"Геолог 1: ({point1[0]}, {point1[1]})", True, BLACK)
    #     screen.blit(coord_text1, (10, info_y))
    #     info_y += 30  # Смещение для следующей строки

    # if point2:
    #     coord_text2 = font.render(f"Геолог 2: ({point2[0]}, {point2[1]})", True, BLACK)
    #     screen.blit(coord_text2, (10, info_y))
    #     info_y += 30

    if distance_to_point1 is not None:
        # distance_text1 = font.render(f"Расстояние от точки 1 до дрона: {distance_to_point1/10:.2f}", True, BLACK)
        # screen.blit(distance_text1, (10, info_y))
        # info_y += 30
        pdpd1 = (32.45 + 20 * math.log10(distance_to_point1/10) + 20 * math.log10(27))
        pspd1 = font.render(f"Потери пути свободное пространство от 1 точки: {pdpd1:.2f} дБ", True, BLACK)
        screen.blit(pspd1, (10,info_y))
        info_y += 30

    if distance_to_point2 is not None:
        # distance_text2 = font.render(f"Расстояние от дрона до точки 2: {distance_to_point2/10:.2f}", True, BLACK)
        # screen.blit(distance_text2, (10, info_y))
        # info_y += 30
        pspd2 = (32.45 + 20 * math.log10(distance_to_point2/10) + 20 * math.log10(27))
        pdpd2 = font.render(f"Потери пути свободного пространства от 2 точки: {pspd2:.2f} Дб", True, BLACK)
        screen.blit(pdpd2, (10, info_y))
        info_y += 30

        itogper1 = 37 - pdpd1 - 10
        itogper2 = 37 - pspd2 - 10

        signal = itogper1
        linear_signal = math.pow(10, signal/10) * math.pow(10, -3)
        shoom = random.randint(70, 100) * -1 #dBm

        shoom_sum += shoom
        d += 1
        if d == 50:
            shoom_viv = shoom_sum / 50
            d = 0
            shoom_sum = 0
        checkshoom1 = itogper1 - shoom_viv
        checkshoom2 = itogper2 - shoom_viv
        if checkshoom1 < 10:
            status_shoom1 = 'Нет сигнала'
        if 10 < checkshoom1 < 20:
            status_shoom1 = 'Плохой сигнал'
        if 40 > checkshoom1 > 20:
            status_shoom1 = 'Средний сигнал'
        if checkshoom1 > 40:
            status_shoom1 = 'Хороший сигнал'
        if checkshoom2 < 10:
            status_shoom2 = 'Нет сигнала'
        if 10 < checkshoom2 < 20:
            status_shoom2 = 'Плохой сигнал'
        if 20 < checkshoom2 < 30:
            status_shoom2 = 'Средний сигнал'
        if checkshoom2 > 30:
            status_shoom2 = 'Хороший сигнал'

        itogper1pr = font.render(f"Итоговое получение сигнала для первой точки равна {itogper1:.2f} дБм ({status_shoom1})", True, BLACK)
        itogper2pr = font.render(f"Итоговая получение сигнала для второй тчоки равна {itogper2:.2f} дБм ({status_shoom2})", True, BLACK)
        screen.blit(itogper1pr, (10, info_y))
        info_y += 30
        screen.blit(itogper2pr, (10, info_y))
        info_y += 30

        linear_shoom = math.pow(10, shoom/10) * math.pow(10, -3)
        linear_snr = linear_signal/linear_shoom
        snr = 10 * math.log10(linear_snr)
        pohmel = random.randint(90, 100) * -1 # dBm
        linear_pohmel = math.pow(10, pohmel/10) * math.pow(10, -3)
        sinr = 10*math.log10(linear_signal / (linear_pohmel + linear_shoom))
        sinr_sum += sinr
        i += 1
        if i == 50:
            sinr_viv = sinr_sum / 50
            i = 0
            sinr_sum = 0    
        if sinr_viv < 1:
            status = 'Нет связи'
        if 1 < sinr_viv < 10:
            status = 'Плохая связь'
        if 10 < sinr_viv < 20:
            status = 'Средняя связь'
        if 21 < sinr_viv > 21:
            status = 'Хорошая связь'
        sinr_viv_fo =  font.render(f"SINR: {sinr_viv:.2f} дБ ({status})", True, BLACK)    
        screen.blit(sinr_viv_fo, (10, info_y))
        info_y += 30

    text_status = font.render(
        "Нажмите для выбора точек" if selecting_points else (
            "Ищет сигнал второй точки..." if not found_second_signal else "Находится в оптимальном месте"
        ),
        True,
        BLACK,
    )
    screen.blit(text_status, (10, 10))

    pygame.display.flip()
    clock.tick(60)



pygame.quit()
sys.exit()
