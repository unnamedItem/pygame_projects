import pygame, sys
from pygame.locals import *
from pygame import Vector2
from pygame.transform import threshold

from utils import read_json

import vfx_verlet
import vfx_verlet_tool

GAME_NAME = 'VFX Verlet Tool'
MODE_DRAW = 0
MODE_TEST = 1
POINTS_THOLD = 0.3

model_data = read_json('./models/vine.json')
my_model = vfx_verlet.VfxVerlet(model_data)

pygame.init()

class Tool():
    def __init__(self, game_name: str) -> None:
        # Display Settings -------------------------------- #
        self.scale = 1
        self.screen_size = Vector2(720, 720)
        self.screen = pygame.Surface(self.screen_size)
        self.disp = self.disp = pygame.display.set_mode((self.screen_size*self.scale))
        self.main_clock = pygame.time.Clock()
        self.game_name = game_name
        pygame.display.set_caption(game_name)

        # VFX Verlet Tool Settings ------------------------ #
        self.tool = vfx_verlet_tool.VFXVerletTool()
        self.mode = MODE_DRAW
        self.space_pressed = False

        # VFX Verlet Model -------------------------------- #
        self.model = my_model
        self.reder_polygons = False 


    # Run Game ---------------------------------- #
    def run(self) -> None:
        while True:
            dt = self.main_clock.tick(60)
            self.process_events()
            self.update(dt)
            self.draw()


    # Handle events ----------------------------- #
    def process_events(self) -> None:
        over_point, px, py = self.tool.over_point(POINTS_THOLD, self.scale)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()

                if event.key == K_d:
                    self.mode = MODE_DRAW

                if event.key == K_t:
                    self.mode = MODE_TEST

            # Draw Mode -------------------------------- #
            if self.mode == MODE_DRAW:
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.space_pressed = False

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.space_pressed = True

                if event.type == MOUSEBUTTONDOWN:
                    if over_point:
                        if event.button == BUTTON_LEFT and not self.space_pressed:
                            self.tool.check_point((px, py))

                        if event.button == BUTTON_RIGHT and not self.space_pressed:
                            self.tool.uncheck_point((px, py))

                        if event.button == BUTTON_LEFT and self.space_pressed:
                            self.tool.link_points()

                        if event.button == BUTTON_RIGHT and self.space_pressed:
                            self.tool.divide_points()

            # Test Mode -------------------------------- #
            if self.mode == MODE_TEST:
                mx, my = pygame.mouse.get_pos()
                self.model.move_grounded([mx, my])

                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.reder_polygons = not self.reder_polygons


    # Update Game ------------------------------- #
    def update(self, dt) -> None:
        if self.mode == MODE_TEST:
            self.model.update()
            self.model.update_sticks()


    # Draw Game --------------------------------- #
    def draw(self):
        self.screen.fill((30,20,30))
        layer = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        if self.mode == MODE_DRAW:
            self.tool.draw_grid(self.screen, self.screen_size)

        elif self.mode == MODE_TEST:
            if not self.reder_polygons:
                self.model.render_sticks(self.screen)
            else:
                self.model.render_polygon(self.screen, (255, 255, 255))
        
        self.screen.blit(layer, Vector2())
        pygame.transform.scale(self.screen, self.disp.get_size(), self.disp)
        pygame.display.flip()


    # Exit Game --------------------------------- #
    def quit(self) -> None:
        pygame.quit()
        sys.exit()


Tool(GAME_NAME).run()
