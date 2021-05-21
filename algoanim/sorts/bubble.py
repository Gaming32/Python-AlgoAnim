from algoanim.array import Array
from algoanim.sort import Sort


class BubbleSort(Sort):
    name = 'Bubble Sort'

    def run(self, array: Array) -> None:
        for i in range(len(array) - 1, -1, -1):
            for j in range(1, i):
                if array[j - 1] > array[j]:
                    array.swap(j - 1, j)


SORT_CLASS = BubbleSort
