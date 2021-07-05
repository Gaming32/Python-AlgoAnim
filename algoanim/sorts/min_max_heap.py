from algoanim.array import Array
from algoanim.sort import Sort
from algoanim.sorts.minmaxheap import MinMaxHeap


class MinMaxHeapSort(Sort):
    name = 'Min-Max Heap Sort'

    def run(self, array: Array) -> None:
        heap = MinMaxHeap(array)
        heap.sort()


SORT_CLASS = MinMaxHeapSort
