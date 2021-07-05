from algoanim.array import Array
from algoanim.sort import Sort
from algoanim.sorts.rotate_merge import sort, rotate_merge_sort


class OptimizedRotateMergeSort(Sort):
    name = 'Optimized Rotate Merge Sort'

    def run(self, array: Array) -> None:
        # rotate_merge_sort(array, 0, len(array), 128)
        sort(array)


SORT_CLASS = OptimizedRotateMergeSort
