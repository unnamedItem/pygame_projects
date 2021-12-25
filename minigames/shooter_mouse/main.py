import pygame, sys, time

from pygame.locals import *
from pygame import Vector2

from sprites import Player, Bullet, Tarjet
from constants import *


class Game():
    def __init__(self, game_name: str) -> None:
        # Pygame Init ------------------------------------- #
        pygame.init()

        # Display Settings -------------------------------- #
        self.scale = 2
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
            KEYDOWN: 0,
        }

        # Player data ------------------------------------- #
        self.player = Player(self.scale, self.display_size / 2)
        self.ammo = 100
        self.ammo_tick = 0

        # Bullets pool ------------------------------------ #
        self.bullets = [ Bullet() for x in range(BULLET_POOL_SIZE) ]

        self.tarjet = Tarjet()
        self.last_hit = 0


    # Run Game ---------------------------------- #
    def run(self) -> None:
        while 1:
            dt = self.delta_time()
            self.process_events()
            self.update(dt)
            self.draw()


    # Handle events ----------------------------- #
    def process_events(self) -> None:
        mx, my = pygame.mouse.get_pos()

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
                if event.button == BUTTON_LEFT and self.ammo >= AMMO_COST:
                    bullet_data = self.player.shoot((mx, my))
                    for bullet in self.bullets:
                        if bullet.disabled:
                            bullet.pos = bullet_data['bullet_pos']
                            bullet.vel = bullet_data['bullet_vel']
                            bullet.disabled = 0
                            self.ammo -= AMMO_COST
                            break
                

    # Update Game ------------------------------- #
    def update(self, dt) -> None:
        mx, my = pygame.mouse.get_pos()             

        if self.keys[K_LCTRL] and self.keys[K_p] and not self.fps_changed:
            self.fps_show = not self.fps_show
            self.fps_changed = True

        for bullet in self.bullets:
            if not bullet.disabled:
                bullet.update(dt)
            
                collide = pygame.sprite.collide_rect(self.tarjet, bullet)
                if collide:
                    self.tarjet.image.fill(RED)
                    bullet.disabled = 1
                    self.last_hit = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.last_hit > HIT_DELAY:
                    self.tarjet.image.fill(WHITE)

        if pygame.time.get_ticks() - self.ammo_tick > AMMO_RECOVER_DELAY:
            if self.ammo < MAX_AMMO:
                self.ammo_tick = pygame.time.get_ticks()
                self.ammo += AMMO_RECOVER_RATE

        self.player.update(dt, (mx, my))
        self.fps_update()


    # Draw Game --------------------------------- #
    def draw(self):
        self.display.fill(BK_COLOR)

        # Layers ------------------------------------- #
        layer0 = pygame.Surface(self.display.get_size(), SRCALPHA)
        self.fps_render(layer0)

        for bullet in self.bullets:
            if not bullet.disabled:
                bullet.draw(layer0)

        self.player.draw(layer0, self.font)
        self.tarjet.draw(layer0)

        # Ammo bar
        pygame.draw.line(layer0, BLUE, (self.display_size[0] - 65, 20), ( self.display_size[0] - 65 + (self.ammo / 2), 20), 10)

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
