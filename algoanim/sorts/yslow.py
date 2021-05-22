from algoanim.array import Array
from algoanim.sort import Sort


def yslow(A, l, r):
    if r - l > 0:
        if A[r] < A[l]:
            A[l], A[r] = A[r], A[l]
        m = (r - l + 1) // 2

        for _ in [0, 1]:
            A = yslow(A, l, r-m)
            A = yslow(A, l + m, r)
            A = yslow(A, l + 1, r - 1)

    return A


class YSlowSort(Sort):
    name = 'YSlow Sort'

    def run(self, array: Array) -> None:
        yslow(array, 0, len(array) - 1)


SORT_CLASS = YSlowSort
