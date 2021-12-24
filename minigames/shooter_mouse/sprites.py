import pygame
from pygame import Vector2

from constants import *
from utils import angle_line

vec = Vector2

class Tarjet(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.update((50,50), (40,40))


    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, (50,50))


class Bullet(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(BULLET_SIZE)
        self.image.set_colorkey(COLOR_KEY_0)
        pygame.draw.circle(self.image, BLUE, vec(BULLET_SIZE) / 2, 2)
        pygame.draw.circle(self.image, WHITE, vec(BULLET_SIZE) / 2, 1)
        self.rect = self.image.get_rect()

        self.pos = vec(0,0)
        self.vel = vec(0,0)

        self.disabled = 1
        

    def update(self, dt: float) -> bool:
        self.pos += self.vel * dt

        if self.pos[0] > DISPLAY_SIZE[0]:
            self.disabled = 1
        if self.pos[0] < 0:
            self.disabled = 1
        if self.pos[1] > DISPLAY_SIZE[1]:
            self.disabled = 1
        if self.pos[1] < 0:
            self.disabled = 1

        self.rect.update(self.pos, self.image.get_size())

        
    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.pos)



class Player(pygame.sprite.Sprite):
    def __init__(self, scale: int, init_pos: Vector2) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale

        self.pos = init_pos
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.var_acc = PLAYER_ACC
        self.max_vel = PLAYER_MAX_SPEED
        self.angle = 0

        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.set_colorkey(COLOR_KEY_0)
        pygame.draw.polygon(self.image, PLAYER_COLOR, PLAYER_POINTS)
        self.rect = self.image.get_rect()


    def update(self, dt: float, pointer: tuple) -> None:
        self.acc = vec(0,0)

        if self.vel.length_squared() < 0.1 * dt:
            self.vel = vec(0,0)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w]:
            self.acc = (self.acc - (vec(0, 1) * self.var_acc))
        if keys_pressed[pygame.K_d]:
            self.acc = (self.acc + vec(1, 0) * self.var_acc)
        if keys_pressed[pygame.K_s]:
            self.acc = (self.acc + vec(0, 1) * self.var_acc)
        if keys_pressed[pygame.K_a]:
            self.acc = (self.acc - vec(1, 0) * self.var_acc)

        if self.vel.length_squared() > self.max_vel ** 2:
            self.vel = self.vel.normalize() * self.max_vel

        if self.pos[0] > DISPLAY_SIZE[0]:
            self.pos[0] = DISPLAY_SIZE[0]
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] > DISPLAY_SIZE[1]:
            self.pos[1] = DISPLAY_SIZE[1]
        if self.pos[1] < 0:
            self.pos[1] = 0

        self.acc += self.vel * FRICTION

        self.vel += self.acc * dt
        self.pos += (self.vel + 0.5 * (self.acc * dt)) * dt
        self.angle = angle_line(self.pos * self.scale, pointer)


    def draw(self, surface: pygame.surface.Surface, font: pygame.font.Font) -> None:        
        img_copy = pygame.transform.rotate(self.image, (self.angle - 90) * -1)
        surface.blit(img_copy, self.pos - (vec(img_copy.get_size()) / 2))

        # pygame.draw.circle(surface, BLUE, self.pos, 3)
        # pygame.draw.line(surface, RED, self.pos, (self.pos + self.vel * 0.5), 2)
        # pygame.draw.line(surface, GREEN, self.pos, (self.pos + self.acc * 0.25), 2)

        vel = str(round(self.vel.magnitude(), 2))
        pos = '(' + str((round(self.pos[0], 2))) + ', ' + str((round(self.pos[1], 2))) + ')'
        text_vel = font.render(vel, True, WHITE)
        text_pos = font.render(pos, True, WHITE)
        surface.blit(text_vel, (10, 5))
        surface.blit(text_pos, (10, 15))

        
    def shoot(self, pointer: tuple) -> dict:
        bullet_pos = self.pos
        bullet_dir = (self.pos * self.scale) - vec(pointer)
        bullet_vel = bullet_dir.normalize() * BULLET_SPEED * -1
        bullet_data = {
            'bullet_pos': vec(bullet_pos),
            'bullet_vel': vec(bullet_vel)
        }
        return bullet_data
