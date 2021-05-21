from algoanim.array import Array
from threading import Thread

import pygame
import pygame.display
import pygame.draw
import pygame.event
import pygame.time
from pygame import *
from pygame.locals import *


class GraphicsThread(Thread):
    window: Surface
    clock: pygame.time.Clock
    running: bool
    array: Array

    def __init__(self, array: Array) -> None:
        super().__init__(name='Graphics', daemon=True)
        self.array = array

    def render(self, array):
        winw, winh = self.window.get_size()
        scalex, scaley = (winw - 40) / len(array), winh / len(array)
        j = 0
        for i in range(len(array)):
            width = int(scalex * (i + 10)) - j
            if width == 0:
                continue
            val = list.__getitem__(array, i) # Doing this to avoid highlighting indices while rendering
            y = int((winh - 20) - (val + 1) * scaley)
            self.window.fill((255, 255, 255), Rect(j + 20, y, width, int((val + 1) * scaley)))
            j += width

    def run(self) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((640, 480), RESIZABLE)
        # self.scale = (WINDOW_SIZE[0] - 40)
        self.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            fps = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
            self.window.fill((0, 0, 0))
            self.render(self.array)
            pygame.display.update()
