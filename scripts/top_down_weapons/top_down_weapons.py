from random import randint
from math import cos, sin, pi
from typing import Counter

import pygame
from pygame import Vector2

from constants import *


vec = Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, **kwargs) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.disabled = kwargs.get('disabled') or 1

        self.pos = kwargs.get('pos') or vec(0,0)
        self.vel = kwargs.get('vel') or vec(0,0)

        self.dmg = kwargs.get('dmg') or 0


    def update(self, dt) -> None:
        if self.disabled:
            return

        self.pos += self.vel * dt
        self.rect.update((self.pos), (self.image.get_size()))

        if self.pos[0] > DISPLAY_SIZE[0]:
            self.disabled = 1
        if self.pos[0] < 0:
            self.disabled = 1
        if self.pos[1] > DISPLAY_SIZE[1]:
            self.disabled = 1
        if self.pos[1] < 0:
            self.disabled = 1


    def render(self, surface: pygame.Surface) -> None:
        if self.disabled:
            return

        surface.blit(self.image, self.pos - (vec(self.image.get_size()) / 2))



class Weapon(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, **kwargs) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.angle = 0
        self.rect = self.image.get_rect()

        self.pos = kwargs.get('pos') or vec(0,0)
        self.pos_canon = kwargs.get('pos_canon') or vec(0,0)
        self.current_pos_canon = self.pos_canon

        self.accuracy = kwargs.get('accuracy') or 1
        self.accuracy_recover_rate = kwargs.get('accuracy_recover_rate') or 0.920
        self.current_accuracy = self.accuracy
        self.recoil = kwargs.get('recoil') or 5
        self.cadency = kwargs.get('cadency') or 30
        self.last_shoot_time = 0

        self.bullet_speed = kwargs.get('bullet_speed') or 500
        self.bullet_per_shoot = kwargs.get('bullet_per_shoot') or 1
        self.bullet_dmg = kwargs.get('dmg') or 10

        self.magazine_size = kwargs.get('magazine_size') or 30
        self.magazine_ammount = kwargs.get('magazine_amount') or 30
        self.magazine_is_empty = kwargs.get('magazine_is_empty') or 0
        self.ammo_per_shoot = kwargs.get('ammo_per_shoot') or 1

        self.reload_time = kwargs.get('reload_time') or 1000
        self.reload_time_init = 0
        self.reloading = kwargs.get('reloading') or 0


    def update(self, dt: float, new_pos: Vector2, pointer: Vector2) -> None:
        self.pos = new_pos
        self.current_pos_canon = self.pos_canon + new_pos
        magnitude = vec(self.pos - self.current_pos_canon).magnitude()
        self.rect.update((new_pos), (self.image.get_size()))
        self.angle = vec(new_pos * GAME_SCALE - pointer).angle_to(vec(1,0))
        self.current_pos_canon = self.pos - vec(new_pos * GAME_SCALE - pointer).normalize() * magnitude

        if self.current_accuracy > self.accuracy:
            if self.current_accuracy > 15:
                self.current_accuracy = 15
            else:
                self.current_accuracy *= self.accuracy_recover_rate
        else:
            self.current_accuracy = self.accuracy        

        if self.reloading:
            self.check_reloading()


    def render(self, surface: pygame.Surface) -> None:
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        surface.blit(rotated_image, self.pos - (vec(rotated_image.get_size()) / 2))
        pygame.draw.circle(surface, (0,255,0), self.pos, 2)
        pygame.draw.circle(surface, (0,255,0), self.current_pos_canon, 2)


    def shoot(self, bullets: 'list[Bullet]') -> None:
        if self.reloading:
            return

        if self.magazine_is_empty:
            self.reload()

        if pygame.time.get_ticks() - self.last_shoot_time < self.cadency:
            return

        bullet_pos = vec(self.current_pos_canon)

        for x in range(self.bullet_per_shoot):
            accuracy = randint(-int(self.current_accuracy), int(self.current_accuracy))
            bullet_dir = vec(
                sin((self.angle - 90 - accuracy) * pi / 180),
                cos((self.angle - 90 - accuracy) * pi / 180),
            )

            for bullet in bullets:
                if bullet.disabled:
                    bullet.disabled = 0
                    bullet.pos = vec(bullet_pos)
                    bullet.vel = bullet_dir * self.bullet_speed
                    bullet.dmg = self.bullet_dmg
                    break
                    

        self.current_accuracy *= self.recoil
        self.last_shoot_time = pygame.time.get_ticks()
        self.magazine_ammount -= self.ammo_per_shoot

        if self.magazine_ammount == 0:
            self.magazine_is_empty = 1


    def reload(self) -> None:
        self.reloading = 1
        self.reload_time_init = pygame.time.get_ticks()


    def check_reloading(self) -> None:
        if pygame.time.get_ticks() - self.reload_time_init > self.reload_time:
            self.reloading = 0
            self.magazine_ammount = self.magazine_size
            self.magazine_is_empty = 0


    def unlock_gun(self) -> None:
        pass
