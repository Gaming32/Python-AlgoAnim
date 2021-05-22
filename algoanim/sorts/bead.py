from algoanim.array import Array
from algoanim.sort import Sort


def beadsort(input_list):
    """Bead sort."""
    # Initialize a 'transposed list' to contain as many elements as
    # the maximum value of the input -- in effect, taking the 'tallest'
    # column of input beads and laying it out flat
    transposed_list = [0] * max(input_list)
    for num in input_list:
        # For each element (each 'column of beads') of the input list,
        # 'lay the beads flat' by incrementing as many elements of the
        # transposed list as the column is tall.
        # These will accumulate atop previous additions.
        transposed_list[:num] = [n + 1 for n in transposed_list[:num]]
    # We've now dropped the beads. To de-transpose, we count the
    # 'bottommost row' of dropped beads, then mimic removing this
    # row by subtracting 1 from each 'column' of the transposed list.
    # When a column does not reach high enough for the current row,
    # its value in transposed_list will be <= 0.
    for i in range(len(input_list)):
        # Counting values > 0 is how we tell how many beads are in the
        # current 'bottommost row'. Note that Python's bools can be
        # evaluated as integers; True == 1 and False == 0.
        input_list[i] = sum(n > 0 for n in transposed_list)
        # Remove the 'bottommost row' by subtracting 1 from each element.
        transposed_list = [n - 1 for n in transposed_list]


class BeadSort(Sort):
    name = 'Bead Sort'

    def run(self, array: Array) -> None:
        beadsort(array)
        array.reverse()


SORT_CLASS = BeadSort
