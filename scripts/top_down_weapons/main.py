import pygame, sys, time

from pygame.locals import *
from pygame import Vector2

from constants import *
from top_down_weapons import Bullet, Weapon


class Game():
    def __init__(self, game_name: str) -> None:
        # Pygame Init ------------------------------------- #
        pygame.init()

        # Display Settings -------------------------------- #
        self.scale = GAME_SCALE
        self.display_size = Vector2(DISPLAY_SIZE)
        self.screen_size = Vector2(DISPLAY_SIZE) * self.scale
        self.display = pygame.Surface(self.display_size)
        self.screen = pygame.display.set_mode((self.screen_size), DOUBLEBUF, DEFAULT_BPP)
        self.game_name = game_name
        pygame.display.set_caption(game_name)

        # Font -------------------------------------------- #
        self.font = pygame.font.SysFont('verdana', 10)

        # Clock ------------------------------------------- #
        self.main_clock = pygame.time.Clock()
        self.last_time = time.time()
        self.fps = self.main_clock.get_fps()
        self.fps_display = ''
        self.fps_show = True
        self.fps_changed = False

        # Keys pressed ------------------------------------ #
        self.keys = {
            K_LCTRL: 0,
            K_p: 0,
            KEYUP: 0,
            KEYDOWN: 0
        }

        self.weapon_image = pygame.surface.Surface((40, 10))
        self.weapon_image.set_colorkey((0,0,0))
        self.weapon_image.fill((120,120,120))
        self.weapon = Weapon(self.weapon_image, pos_canon=Vector2(18, 0))

        self.bullet_image = pygame.Surface((4,4))
        self.bullet_image.set_colorkey(COLOR_KEY_0)
        pygame.draw.circle(self.bullet_image, BLUE, Vector2(4,4) / 2, 2)
        pygame.draw.circle(self.bullet_image, WHITE, Vector2(4,4) / 2, 1)
        self.bullets = [Bullet(self.bullet_image) for x in range(50)]


    # Run Game ---------------------------------- #
    def run(self) -> None:
        while 1:
            dt = self.delta_time()
            self.process_events()
            self.update(dt)
            self.draw()


    # Handle events ----------------------------- #
    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:
                self.keys[KEYDOWN] = 1
                self.keys[KEYUP] = 0
                
                if event.key == K_ESCAPE:
                    self.quit()

                if event.key == K_LCTRL:
                    self.keys[K_LCTRL] = 1

                if event.key == K_p:
                    self.keys[K_p] = 1

            if event.type == KEYUP:
                self.keys[KEYDOWN] = 0
                self.keys[KEYUP] = 1

                if event.key == K_LCTRL:
                    self.keys[K_LCTRL] = 0

                if event.key == K_p:
                    self.keys[K_p] = 0

            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    self.weapon.shoot(self.bullets)

            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                self.weapon.shoot(self.bullets)


    # Update Game ------------------------------- #
    def update(self, dt) -> None:
        pointer = Vector2(pygame.mouse.get_pos())

        self.fps_update()

        if self.keys[K_LCTRL] and self.keys[K_p] and not self.fps_changed:
            self.fps_show = not self.fps_show
            self.fps_changed = True

        if self.keys[KEYUP]:
            self.fps_changed = False

        self.weapon.update(dt, self.display_size / 2, pointer)

        for bullet in self.bullets:
            bullet.update(dt)


    # Draw Game --------------------------------- #
    def draw(self):
        self.display.fill(BK_COLOR)

        # Layers ------------------------------------- #
        layer0 = pygame.Surface(self.display.get_size(), SRCALPHA)
        self.fps_render(layer0)
        self.weapon.render(layer0)

        for bullet in self.bullets:
            bullet.render(layer0)

        # Blit Layers -------------------------------- #
        self.display.blit(layer0, Vector2())

        pygame.transform.scale(self.display, self.screen.get_size(), self.screen)
        pygame.display.flip()


    # Exit Game --------------------------------- #
    def quit(self) -> None:
        pygame.quit()
        sys.exit()


    # Delta Time -------------------------------- #
    def delta_time(self) -> float:
        self.main_clock.tick(FPS_LIMIT)
        self.fps = self.main_clock.get_fps()
        dt = time.time() - self.last_time
        self.last_time = time.time()
        return dt


    # Fps Update -------------------------------- #
    def fps_update(self) -> None:
        fps_str = 'FPS: ' + str(round(self.fps, 2))
        text = self.font.render(fps_str, True, WHITE)
        self.fps_display = text


    # Fps Render -------------------------------- #
    def fps_render(self, layer: pygame.surface.Surface) -> None:
        if self.fps_show:
            layer.blit(self.fps_display, (self.display_size[0] - 65, 5))


Game(GAME_NAME).run()
