from os import write
import pygame
from pygame.locals import *

from utils import read_json, write_json
from constants import *


class VFXVerletTool():
    def __init__(self) -> None:
        # Tool Settings ---------------------------------------- #
        self.grid_margin = DEFAULT_GRID_MARGIN
        self.grid_scale = DEFAULT_GRID_SCALE
        self.block_size = DEFAULT_BLOCK_SIZE

        # Points data ------------------------------------------ #
        self.points = []
        self.sticks = []
        self.grounded = []


    def draw_grid(self, screen: pygame.Surface, screen_size: pygame.Vector2) -> None:
        margin = self.grid_margin
        scr_width = int(screen_size[0])
        scr_height = int(screen_size[1])

        # Draw Grid ------------------------------------------- #
        for x in range(margin, scr_width, self.block_size):
            pygame.draw.line(screen, (110, 110, 110), (x, margin), (x, scr_height - margin))
        for y in range(margin, scr_height, self.block_size):
            pygame.draw.line(screen, (110, 110, 110), (margin, y), (scr_width - margin, y))

        # Draw Points ------------------------------------------ #
        for point in self.points:
            scaled_point = (point[0] * self.block_size, point[1] * self.block_size)
            pygame.draw.circle(screen, (255, 255, 255), scaled_point, 3)

        # Draw sticks ------------------------------------------ #
        for stick in self.sticks:
            pass


    def check_point(self, point: tuple) -> None:
        if point not in self.points:
            self.points.append(point)


    def uncheck_point(self, point: tuple) -> None:
        if point in self.points:
            idx = self.points.index(point)
            self.points.pop(idx)

    
    def over_point(self, thold: float, scale: float) -> bool:
        mx, my = pygame.mouse.get_pos()
        vec = pygame.Vector2(mx, my) / (self.block_size * scale)
        px = round(vec[0])
        py = round(vec[1])
        over_point = px - thold <= vec[0] <= px + thold and py - thold <= vec[1] <= py + thold 
        return over_point, px, py


    def link_points(self) -> None:
        pass


    def divide_points(self) -> None:
        pass


    def save_model(self) -> None:
        pass


    def load_model(self) -> None:
        pass


    def get_model(self) -> dict:
        pass
