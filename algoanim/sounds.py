from __future__ import annotations
from algoanim.array import Array
from threading import Thread
from typing import TYPE_CHECKING

import pygame
import pygame.midi
import pygame.time
from pygame import *
from pygame.locals import *

if TYPE_CHECKING:
    from algoanim.main import MainWindow


NUM_CHANNELS = 16
PITCH_MIN = 25
PITCH_MAX = 105
SOUND_MUL = 1


class SoundsThread(Thread):
    wind: MainWindow
    clock: pygame.time.Clock

    _instrument: int
    instrument: int

    def __init__(self, wind: MainWindow) -> None:
        super().__init__(name='Sounds', daemon=False)
        self.wind = wind
        self._instrument = -1
        self.instrument = -1

    def run(self) -> None:
        try:
            pygame.midi.init()
            sound = pygame.midi.Output(pygame.midi.get_default_output_id())
        except Exception:
            return
        self.clock = pygame.time.Clock()
        notes = set()
        array = self.wind.array
        marks = array.marks
        while self.wind.graphics.running:
            ms = self.clock.tick(60)
            for note in notes:
                sound.note_off(note)
            notes.clear()
            length = len(array)
            note_count = min(len(marks), NUM_CHANNELS)
            if self._instrument != self.instrument:
                self._instrument = self.instrument
                sound.set_instrument(self.instrument)
            try:
                array.marks_lock.acquire()
                for i in marks:
                    array.marks_lock.release()
                    try:
                        pitch = array[min(max(i, 0), length - 1)] / length * (PITCH_MAX - PITCH_MIN) + PITCH_MIN
                        pitch_major = int(pitch)
                        pitch_minor = int((pitch - int(pitch)) * 8192)
                        vel = int(pow(PITCH_MAX - pitch_major, 2) * pow(note_count, -0.25) * 64 * SOUND_MUL) // 2
                        if SOUND_MUL >= 1 and vel < 256:
                            vel *= vel
                        sound.note_on(pitch_major, vel)
                        sound.pitch_bend(pitch_minor)
                        notes.add(pitch_major)
                    finally:
                        array.marks_lock.acquire()
            finally:
                array.marks_lock.release()
        pygame.midi.quit()
