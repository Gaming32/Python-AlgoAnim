from threading import Thread
from algoanim.array import Array
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

    def __init__(self, wind, klass: type[Sort]):
        super().__init__(name='Sorting', daemon=True)
        self.klass = klass
        self.wind = wind

    def run(self) -> None:
        self.wind.sort_thread = self
        self.wind.length_scale.config(state='disabled')
        random.shuffle(self.wind.array)
        sort = self.klass()
        sort.run(self.wind.array)
        self.wind.array.reset(len(self.wind.array))
        self.wind.length_scale.config(state='normal')
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
