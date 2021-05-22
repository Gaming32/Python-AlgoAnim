import random

from algoanim.array import Array
from algoanim.sort import Sort


class BubbleSort(Sort):
    name = 'Bogo Sort'

    def is_sorted(self, array: Array):
        for i in range(1, len(array)):
            if array[i - 1] > array[i]:
                return False
        return True

    def run(self, array: Array) -> None:
        while not self.is_sorted(array):
            random.shuffle(array)


SORT_CLASS = BubbleSort
