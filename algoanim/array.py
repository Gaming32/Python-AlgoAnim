from threading import Lock
import time


class Array(list):
    marks: set[int]
    current_delay: int
    delay_mult: int
    delay: int
    length_lock: Lock

    def __init__(self, length: int) -> None:
        super().__init__(range(length))
        self.marks = set()
        self.current_delay = 0
        self.delay_mult = 512
        self.delay = self.delay_mult / len(self)
        self.length_lock = Lock()

    def sleep(self, ms: int) -> None:
        self.current_delay += ms
        while self.current_delay > 0:
            start = time.perf_counter_ns()
            time.sleep(0.001)
            self.current_delay -= ((time.perf_counter_ns() - start) // 1e6) / self.delay

    def reset(self, length: int) -> None:
        with self.length_lock:
            self.clear()
            self.extend(range(length))
        self.marks.clear()
        self.current_delay = 0
        self.delay = self.delay_mult / len(self)

    def set_delay_multiplier(self, mult: float) -> None:
        self.delay_mult = mult
        self.delay = self.delay_mult / len(self)

    def write(self, index: int, value: int) -> None:
        super().__setitem__(index, value)
        self.marks.clear()
        self.marks.add(index)
        self.sleep(1)

    def swap(self, a: int, b: int) -> None:
        temp = super().__getitem__(a)
        super().__setitem__(a, super().__getitem__(b))
        super().__setitem__(b, temp)
        self.marks.clear()
        self.marks.update({a, b})
        self.sleep(1)

    def __setitem__(self, i: int, v: int) -> None:
        self.write(i, v)

    def __getitem__(self, i: int) -> int:
        self.marks.clear()
        self.marks.add(i)
        self.sleep(1)
        return super().__getitem__(i)
