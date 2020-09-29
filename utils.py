from itertools import tee


def pairwise(iterable):
    it1, it2 = tee(iterable)
    next(it2)
    return zip(it1, it2)
