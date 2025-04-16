import pygame
import sys

# Настройки окна
WIDTH, HEIGHT = 800, 400
FPS = 10

# Размеры кадров
FRAME_WIDTH = 112
IDLE_HEIGHT = 20
RUN_HEIGHT = 20
JUMP_HEIGHT = 50

SCALE = 3

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Анимации персонажа")
clock = pygame.time.Clock()

# Загрузка спрайтов
idle_sheet = pygame.image.load("TheKeeper1.1.png").convert_alpha()
run_sheet = pygame.image.load("TheKeeper1.2.png").convert_alpha()
jump_sheet = pygame.image.load("TheKeeper1.3.png").convert_alpha()

# Функция: разрезать горизонтальный спрайт-лист
def load_animation(sheet, frame_width, frame_height, total_frames):
    frames = []
    for i in range(total_frames):
        x = i * frame_width
        y = 0
        frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (frame_width * SCALE, frame_height * SCALE))
        frames.append(frame)
    return frames

# Анимации
animations = {
    "idle": load_animation(idle_sheet, FRAME_WIDTH, IDLE_HEIGHT, 8),
    "run": load_animation(run_sheet, FRAME_WIDTH, RUN_HEIGHT, 8),
    "jump": load_animation(jump_sheet, FRAME_WIDTH, JUMP_HEIGHT, 8),
}

# Стартовая анимация
animation_name = "idle"
frame_index = 0
current_animation = animations[animation_name]

# Позиция персонажа
x = WIDTH // 2
y = HEIGHT // 2

# Цикл игры
running = True
while running:
    screen.fill((30, 30, 30))
    keys = pygame.key.get_pressed()

    # Управление
    if keys[pygame.K_RIGHT]:
        animation_name = "run"
    elif keys[pygame.K_RETURN]:
        animation_name = "jump"
    else:
        animation_name = "idle"

    # Обновить кадры
    current_animation = animations[animation_name]
    frame_index = (frame_index + 1) % len(current_animation)

    # Центрировать по разной высоте кадров
    frame = current_animation[frame_index]
    frame_rect = frame.get_rect(center=(x, y))

    # Отображение
    screen.blit(frame, frame_rect)

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
