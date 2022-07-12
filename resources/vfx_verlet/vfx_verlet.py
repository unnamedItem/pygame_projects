import pygame
from constants import *
from utils import get_dis


class VerletPoint():
    def __init__(self, point) -> None:
        self.x = point[0]
        self.y = point[1]
        self.oldx = point[0]
        self.oldy = point[1]


class VerletStick():
    def __init__(self, stick: list, points: list) -> None:
        self.p1 = stick[0]
        self.p2 = stick[1]
        self.dis = get_dis(points[stick[0]], points[stick[1]])


class VfxVerlet():
    def __init__(self, data: dict) -> None:
        self.points = self.init_points(data['points'])
        self.orig_points = self.init_points(data['points'])
        self.grounded = data['grounded']
        self.sticks = []
        for stick in data['connections']:
            self.add_stick(stick)
        self.scale = data.get('scale') or DEFAULT_SCALE
        self.gravity = data.get('gravity') or DEFAULT_GRAVITY
        self.bounce = data.get('bounce') or DEFAULT_BOUNCE
        self.friction = data.get('friction') or DEFAULT_FRICTION
        self.wind = data.get('wind') or DEFAULT_WIND


    @staticmethod
    def init_points(points: list) -> list:
        points_list = []
        for point in points:
            new_point = VerletPoint(point)
            points_list.append(new_point)
        return points_list


    def add_stick(self, stick: list) -> None:
        new_stick = VerletStick(stick, self.points)
        self.sticks.append(new_stick)


    def update(self) -> None:
        for i, point in enumerate(self.points):
            if i not in self.grounded:
                dx = (point.x - point.oldx) * self.friction + self.wind
                dy = (point.y - point.oldy) * self.friction
                point.oldx = point.x
                point.oldy = point.y
                point.x += dx
                point.y += dy
                point.y += self.gravity


    def move_grounded(self, offset: list) -> None:
        for i, point in enumerate(self.points):
            if i in self.grounded:
                point.x = self.orig_points[i].x + offset[0] / self.scale
                point.y = self.orig_points[i].y + offset[1] / self.scale
                point.oldx = point.x
                point.oldy = point.y

    
    def update_sticks(self) -> None:
        for stick in self.sticks:
            dis = get_dis(self.points[stick.p1], self.points[stick.p2])
            dis_dif = stick.dis - dis
            mv_ratio = dis_dif / dis / 2
            dx = self.points[stick.p2].x - self.points[stick.p1].x
            dy = self.points[stick.p2].y - self.points[stick.p1].y
            if stick.p1 not in self.grounded:
                self.points[stick.p1].x -= dx * mv_ratio * self.bounce
                self.points[stick.p1].y -= dy * mv_ratio * self.bounce
            if stick.p2 not in self.grounded:
                self.points[stick.p2].x += dx * mv_ratio * self.bounce
                self.points[stick.p2].y += dy * mv_ratio * self.bounce


    def render_polygon(self, target_surf: pygame.Surface, color: tuple, offset=[0, 0]) -> None:
        y_points = [p.y * self.scale for p in self.points]
        x_points = [p.x * self.scale for p in self.points]
        min_x = min(x_points)
        max_x = max(x_points)
        min_y = min(y_points)
        max_y = max(y_points)
        width = int(max_x - min_x + 2)
        height = int(max_y - min_y + 2)
        surf = pygame.Surface((width, height))
        self.render_sticks(surf, (int(min_x), int(min_y)))
        surf.set_colorkey((0, 0, 0))
        m = pygame.mask.from_surface(surf)
        outline = m.outline() # get outline of mask
        surf.fill((0, 0, 0)) # fill with color that will be colorkey
        surf.set_colorkey((0, 0, 0))
        pygame.draw.polygon(surf, color, outline)
        target_surf.blit(surf, (min_x - offset[0], min_y - offset[1]))


    def render_sticks(self, surf, offset=[0, 0]):
        render_points = [[p.x * self.scale - offset[0], p.y * self.scale - offset[1]] for p in self.points]
        for stick in self.sticks:
            pygame.draw.line(surf, (255, 255, 255), render_points[stick.p1], render_points[stick.p2], 1)
