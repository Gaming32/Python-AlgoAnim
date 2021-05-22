from algoanim.array import Array
from algoanim.sort import Sort


# From https://stackabuse.com/sorting-algorithms-in-python#selectionsort
def selection_sort(nums):
    # This value of i corresponds to how many values were sorted
    for i in range(len(nums)):
        # We assume that the first item of the unsorted segment is the smallest
        lowest_value_index = i
        # This loop iterates over the unsorted items
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[lowest_value_index]:
                lowest_value_index = j
        # Swap values of the lowest unsorted element with the first unsorted
        # element
        nums[i], nums[lowest_value_index] = nums[lowest_value_index], nums[i]


class SelectionSort(Sort):
    name = 'Selection Sort'

    def run(self, array: Array) -> None:
        selection_sort(array)


SORT_CLASS = SelectionSort
