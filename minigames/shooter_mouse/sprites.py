import pygame
from pygame import Vector2


from constants import PLAYER_POINTS, PLAYER_COLOR, PLAYER_ACC, PLAYER_MAX_SPEED, FRICTION, DISPLAY_SIZE
from utils import angle_line

vec = Vector2


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

        self.image = pygame.Surface((21, 21))
        self.image.set_colorkey((0,0,0))
        pygame.draw.polygon(self.image, PLAYER_COLOR, PLAYER_POINTS)


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

        pygame.draw.circle(surface, (255, 0, 255), self.pos, 3)
        pygame.draw.line(surface, (255,0,0), self.pos, (self.pos + self.vel * 0.5), 2)
        pygame.draw.line(surface, (0,255,0), self.pos, (self.pos + self.acc * 0.5), 2)

        vel = str(round(self.vel.magnitude(), 2))
        pos = '(' + str((round(self.pos[0], 2))) + ', ' + str((round(self.pos[1], 2))) + ')'
        text_vel = font.render(vel, True, (255, 255, 255))
        text_pos = font.render(pos, True, (255, 255, 255))
        surface.blit(text_vel, (10, 5))
        surface.blit(text_pos, (10, 15))
