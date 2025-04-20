import pygame
import sys

# Константы
FRAME_W, FRAME_H = 16, 16
SCALE = 3            
STATES = ['idle', 'run', 'jump', 'fall', 'slide']
FRAMES_PER_STATE = 8
ANIM_SPEED = 7  # скорость проигрывания (кадра за кадр)
GRAVITY = 900       # гравитация
JUMP_FORCE = -400   # сила прыжка
PLAYER_SPEED = 200  # скорость передвижения
GROUND_Y = 300      # уровень земли по оси Y


class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def image_at(self, rect):
        x, y, w, h = rect
        image = pygame.Surface((w, h), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        return image

    def load_animations(self):
        animations = {}
        for row, state in enumerate(STATES):
            frames = []
            for col in range(FRAMES_PER_STATE):
                x = col * FRAME_W 
                y = row * FRAME_H * 3
                frames.append(self.image_at((x, y, FRAME_W, FRAME_H)))
            animations[state] = frames
        return animations


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, spritesheet):
        super().__init__()
        self.animations = spritesheet.load_animations()
        self.state = 'idle'
        self.frame_index = 0.0
        self.sliding = False
        self.facing_right = True

        # начальный кадр с масштабированием
        raw = self.animations[self.state][0]
        self.image = pygame.transform.scale(raw, (FRAME_W * SCALE, FRAME_H * SCALE))
        self.rect = self.image.get_rect(topleft=pos)

        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT] :
            self.velocity.x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
            self.velocity.x = PLAYER_SPEED
            self.facing_right = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False
        self.sliding = keys[pygame.K_DOWN] and self.on_ground

    def update_state(self):
        if self.sliding:
            self.state = 'slide'
        elif not self.on_ground:
            self.state = 'jump' if self.velocity.y < 0 else 'fall'
        elif self.velocity.x != 0:
            self.state = 'run'
        else:
            self.state = 'idle'

    def apply_gravity(self, dt):
        self.velocity.y += GRAVITY * dt
        self.rect.y += self.velocity.y * dt
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity.y = 0
            self.on_ground = True

    def animate(self, dt):
        frames = self.animations[self.state]
        self.frame_index += ANIM_SPEED * dt
        if self.frame_index >= len(frames):
            self.frame_index = 0.0
        raw_frame = frames[int(self.frame_index)]


        scaled_frame = pygame.transform.scale(raw_frame, (FRAME_W * SCALE, FRAME_H * SCALE))
        # зеркальное отражение
        flipped = pygame.transform.flip(scaled_frame, not self.facing_right, False)

        # сохраняем позицию и обновляем изображение
        old_topleft = self.rect.topleft
        self.image = flipped
        self.rect = self.image.get_rect(topleft=old_topleft)

    def update(self, dt):
        self.handle_input()
        self.update_state()
        self.rect.x += self.velocity.x * dt
        self.apply_gravity(dt)
        self.animate(dt)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    clock = pygame.time.Clock()

    spritesheet = SpriteSheet('spritesheet.png')
    player = Player((100, 100), spritesheet)
    all_sprites = pygame.sprite.Group(player)

    while True:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update(dt)
        screen.fill((30, 30, 30))
        pygame.draw.line(screen, (100, 100, 100), (0, GROUND_Y), (640, GROUND_Y))
        all_sprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
