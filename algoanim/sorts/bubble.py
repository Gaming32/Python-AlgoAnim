from algoanim.array import Array
from algoanim.sort import Sort


class BubbleSort(Sort):
    name = 'Bubble Sort'

    def run(self, array: Array) -> None:
        for i in range(len(array), 0, -1):
            sorted = True
            for j in range(1, i):
                if array[j - 1] > array[j]:
                    sorted = False
                    array.swap(j - 1, j)
            if sorted:
                break


SORT_CLASS = BubbleSort
