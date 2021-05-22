from algoanim.utils import TITLE
from algoanim.array import Array
from threading import Thread

import pygame
import pygame.display
import pygame.draw
import pygame.event
import pygame.font
import pygame.time
from pygame import *
from pygame.locals import *


class GraphicsThread(Thread):
    window: Surface
    clock: pygame.time.Clock
    stats_font: pygame.font.Font
    running: bool
    array: Array
    should_show_stats: bool
    label: str

    def __init__(self, array: Array) -> None:
        super().__init__(name='Graphics', daemon=True)
        self.array = array
        self.should_show_stats = True
        self.label = ''

    def render(self, array: Array):
        winw, winh = self.window.get_size()
        scalex, scaley = winw / len(array), winh / len(array)
        j = 0
        for i in range(len(array)):
            width = int(scalex * (i + 1)) - j
            if width == 0:
                continue
            val = list.__getitem__(array, i) # Doing this to avoid highlighting indices while rendering
            y = int(winh - (val + 1) * scaley)
            self.window.fill((255, 255, 255), Rect(j, y, width, int((val + 1) * scaley)))
            j += width
        j = 0
        for i in range(len(array)):
            width = int(scalex * (i + 1)) - j
            if i in array.marks:
                val = list.__getitem__(array, i) # Doing this to avoid highlighting indices while rendering
                y = int(winh - (val + 1) * scaley)
                self.window.fill((255, 0, 0), Rect(j, y, max(width, 2), int((val + 1) * scaley)))
            j += width

    def show_stats(self):
        delay = self.array.single_delay * self.array.delay
        stats = self.array.stats
        text = self.label
        text += f' {len(self.array):7} numbers'
        text += f'   {delay:5}ms delay'
        text += f'   {stats.writes:4} writes'
        text += f'   {stats.accesses:4} accesses'
        render = self.stats_font.render(text, True, (255, 255, 255))
        rect = render.get_rect()
        self.window.blit(render.convert_alpha(), (10, 10, rect.w, rect.h))

    def run(self) -> None:
        pygame.init()
        screen_info = pygame.display.Info()
        self.window = pygame.display.set_mode((screen_info.current_w // 2, screen_info.current_h // 2), RESIZABLE)
        pygame.display.set_caption(f'{TITLE}') # Doing this weird syntax just in case I decide to add something more later
        self.stats_font = pygame.font.SysFont('lucida console', 16)
        self.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            ms = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
            self.window.fill((0, 0, 0))
            with self.array.length_lock:
                self.render(self.array)
            if self.should_show_stats:
                self.show_stats()
            pygame.display.update()
