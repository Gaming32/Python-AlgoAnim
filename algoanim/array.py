class Array(list):
    marks: set[int]

    def __init__(self, length: int) -> None:
        super().__init__(range(length))
        self.marks = set()

    def write(self, index: int, value: int) -> None:
        super().__setitem__(index, value)
        self.marks.clear()
        self.marks.add(index)

    def swap(self, a: int, b: int) -> None:
        temp = super().__getitem__(a)
        super().__setitem__(a, super().__getitem__(b))
        super().__setitem__(b, temp)
        self.marks.clear()
        self.marks.update({a, b})

    def __setitem__(self, i: int, v: int) -> None:
        self.write(i, v)

    def __getitem__(self, i: int) -> int:
        self.marks.clear()
        self.marks.add(i)
        return super().__getitem__(i)
