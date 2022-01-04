import pygame
from pygame import Surface, Vector2


class Sprite(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.pos = Vector2()
        self.disabled = False


    def render(self, layer: Surface, *args, **kwargs) -> None:
        pass