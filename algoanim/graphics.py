from threading import Thread

import pygame
import pygame.display
import pygame.event
import pygame.time
from pygame import *
from pygame.locals import *


class GraphicsThread(Thread):
    window: Surface
    clock: pygame.time.Clock
    running: bool

    def __init__(self) -> None:
        super().__init__(name='Graphics', daemon=True)

    def run(self) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((640, 480), RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            fps = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
            pygame.display.update()
