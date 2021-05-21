from algoanim.array import Array
from algoanim.sort import Sort
from algoanim.sorts.GrailSort import GrailSort as GrailSortImpl


class GrailSort(Sort):
    name = 'Grail Sort'

    def run(self, array: Array) -> None:
        GrailSortImpl.grailSortInPlace(array, 0, len(array))


SORT_CLASS = GrailSort
