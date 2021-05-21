from algoanim.array import Array
from algoanim.sort import Sort


class InsertionSort(Sort):
    name = 'Insertion Sort'

    def run(self, array: Array) -> None:
        for i in range(1, len(array)):
            v = array[i]
            j = i - 1
            while j > -1 and array[j] > v:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = v


SORT_CLASS = InsertionSort
