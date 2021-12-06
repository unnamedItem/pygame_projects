import pygame

from constants import PLAYER_POINTS, PLAYER_COLOR
from utils import angle_line

class Player():
    def __init__(self) -> None:
        self.scale = 2
        self.posx = 0
        self.posy = 0
        self.angle = 0
        self.img = pygame.Surface((22, 22))
        self.img.set_colorkey((0,0,0))
        pygame.draw.polygon(self.img, PLAYER_COLOR, PLAYER_POINTS)


    def update(self, offset: tuple, pointer: tuple) -> None:
        angle = angle_line(pygame.Vector2(offset) * self.scale, pointer)

        self.posx = offset[0]
        self.posy = offset[1]
        self.angle = angle


    def draw(self, surface: pygame.surface.Surface) -> None:
        img_copy = pygame.transform.rotate(self.img, (self.angle - 90) * -1)
        surface.blit(img_copy, (self.posx - int(img_copy.get_width() / 2), self.posy - int(img_copy.get_height() / 2)))
