from __future__ import annotations
import time
from typing import TYPE_CHECKING
from threading import Thread
from algoanim.array import Array
if TYPE_CHECKING:
    from algoanim.main import MainWindow
import os
import importlib.machinery
import types
import random
from typing import Optional


class SortMeta(type):
    name: str = ''

    def __repr__(self) -> str:
        return f'<Sort class {self.__name__} "{self.name}">'


class Sort(metaclass=SortMeta):
    name: str = ''

    def run(self, array: Array) -> None:
        raise NotImplementedError


class SortThread(Thread):
    klass = type[Sort]
    wind: MainWindow

    def __init__(self, wind: MainWindow, klass: type[Sort]):
        super().__init__(name='Sorting', daemon=True)
        self.klass = klass
        self.wind = wind

    def run(self) -> None:
        self.wind.sort_thread = self
        self.wind.choose_sort.config(state='disabled')
        self.wind.length_scale.config(state='disabled')
        self.wind.array.reset(len(self.wind.array))
        old_delay = self.wind.delay_multiplier
        self.wind.delay_multiplier = 1024 / len(self.wind.array)
        self.wind.array.set_delay_multiplier(self.wind.delay_multiplier)
        self.wind.graphics.label = 'Shuffling...'
        self.wind.array.stats.reset()
        random.shuffle(self.wind.array)
        self.wind.graphics.label = '            '
        self.wind.delay_multiplier = old_delay
        self.wind.array.set_delay_multiplier(old_delay)
        with self.wind.array.marks_lock:
            self.wind.array.marks.clear()
        time.sleep(0.75)
        self.wind.graphics.label = self.klass.name
        self.wind.array.stats.reset()
        sort = self.klass()
        sort.run(self.wind.array)
        with self.wind.array.marks_lock:
            self.wind.array.marks.clear()
        self.wind.length_scale.config(state='normal')
        self.wind.choose_sort.config(state='readonly')
        self.wind.sort_thread = None


def load_sort_file(path: os.PathLike, package: Optional[str] = None) -> Optional[type[Sort]]:
    basename = os.path.splitext(os.path.basename(path))[0]
    if package is None:
        module_name = basename
    else:
        module_name = package + '.' + basename
    loader = importlib.machinery.SourceFileLoader(module_name, path)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    if hasattr(module, 'SORT_CLASS'):
        return module.SORT_CLASS
    return None
