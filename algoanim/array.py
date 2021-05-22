from threading import Lock
import time


class Array(list):
    marks: set[int]
    current_delay: int
    delay: int
    length_lock: Lock

    def __init__(self, length: int) -> None:
        super().__init__(range(length))
        self.marks = set()
        self.current_delay = 0
        self.delay = 1
        self.length_lock = Lock()

    def sleep(self, ms: int) -> None:
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

    def reset(self, length: int) -> None:
        with self.length_lock:
            self.clear()
            self.extend(range(length))
        self.marks.clear()
        self.current_delay = 0

    def set_delay_multiplier(self, mult: float) -> None:
        if mult == 0:
            self.current_delay = 0
        self.delay = mult

    def write(self, index: int, value: int) -> None:
        super().__setitem__(index, value)
        self.marks.clear()
        self.marks.add(index)
        self.sleep(0.5)

    def swap(self, a: int, b: int) -> None:
        # This swap algorithm matches Python sorting
        # algorithms not written for this program
        self[a], self[b] = self[b], self[a]

    def __setitem__(self, i: int, v: int) -> None:
        self.write(i, v)

    def __getitem__(self, i: int) -> int:
        self.marks.clear()
        self.marks.add(i)
        self.sleep(0.5)
        return super().__getitem__(i)
