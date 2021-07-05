from algoanim.stats import Stats
from threading import Lock
import time
from typing import Iterable, Union


class Array(list):
    marks: set[int]
    current_delay: float
    single_delay: float
    delay: float
    length_lock: Lock
    marks_lock: Lock
    stats: Stats

    def __init__(self, length: int) -> None:
        super().__init__(range(length))
        self.marks = set()
        self.current_delay = 0
        self.single_delay = 0
        self.delay = 1
        self.length_lock = Lock()
        self.marks_lock = Lock()
        self.stats = Stats()

    def sleep(self, ms: float) -> None:
        self.single_delay = ms
        if self.delay == 0:
            return
        self.current_delay += ms
        while self.current_delay > 0:
            start = time.perf_counter_ns()
            time.sleep(0.001)
            end = time.perf_counter_ns()
            if self.delay == 0:
                self.current_delay = 0
            else:
                self.current_delay -= ((end - start) // 1e6) / self.delay
        self.single_delay = 0

    def reset(self, length: int) -> None:
        with self.length_lock:
            self.clear()
            self.extend(range(length))
        with self.marks_lock:
            self.marks.clear()
        self.current_delay = 0

    def set_delay_multiplier(self, mult: float) -> None:
        if mult == 0:
            self.current_delay = 0
        self.delay = mult

    def write(self, index: int, value: int) -> None:
        self.stats.add_writes()
        super().__setitem__(index, value)
        with self.marks_lock:
            self.marks.clear()
            self.marks.add(index)
        self.sleep(0.5)

    def read(self, i: int) -> int:
        self.stats.add_reads()
        with self.marks_lock:
            self.marks.clear()
            self.marks.add(i)
        self.sleep(0.5)
        return super().__getitem__(i)

    def swap(self, a: int, b: int) -> None:
        # This swap algorithm matches Python sorting
        # algorithms not written for this program
        self[a], self[b] = self[b], self[a]

    def reverse_range(self, i: int, j: int) -> None:
        while i < j:
            self.swap(i, j)
            i += 1
            j -= 1

    def reverse(self) -> None:
        self.reverse_range(0, len(self) - 1)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __setitem__(self, i: Union[int, slice], v: Union[int, Iterable[int]]) -> None:
        if isinstance(i, slice):
            if i.step is not None and i.step != 1:
                raise NotImplementedError('Stepped slice assignments not supported')
            v = iter(v)
            for j in range(*i.indices(len(self))):
                self.write(j, next(v))
        else:
            self.write(i, v)

    def __getitem__(self, i: Union[int, slice]) -> Union[int, Iterable[int]]:
        if isinstance(i, slice):
            result = []
            for j in range(*i.indices(len(self))):
                result.append(self.read(j))
            return result
        else:
            return self.read(i)
