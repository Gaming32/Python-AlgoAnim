class Stats:
    writes: int
    reads: int
    accesses: int

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.writes = 0
        self.reads = 0
        self.accesses = 0

    def add_reads(self, count: int = 1) -> None:
        self.reads += count
        self.accesses += count

    def add_writes(self, count: int = 1) -> None:
        self.writes += count
        self.accesses += count
