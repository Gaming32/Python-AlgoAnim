"""
Sort files must contain an attribute called SORT_CLASS
that is a subclass of algoanim.sort.Sort
"""

from algoanim.sort import Sort


SORT_CLASS: type[Sort]
