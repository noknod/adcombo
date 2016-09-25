# -*- coding: utf-8 -*-

import itertools


__all__ = ('ArrayPermutator',)


class PermutationGenerator(object):

    def generate(length):
        for permutation in itertools.permutations(range(length), length):
            yield permutation


class ArrayPermutator(object):

    _ARRAY_ELEMENTS_CNT_IN_REPR = 3

    def __init__(self, array):
        self._array = array
        self._length = len(array)
        self._requested_cnt = 0        
        self._generator = None

    def start(self):
        self._generator = PermutationGenerator.generate(self._length)
        self._requested_cnt = 0

    def next(self):
        self._requested_cnt += 1
        permutation = None
        for permutation in self._generator:
            break
        if permutation is None:
            return None
        permutated_array = [self._array[index] for index in permutation]
        return permutated_array

    def __str__(self):
        str_array = str(
            self._array[:ArrayPermutator._ARRAY_ELEMENTS_CNT_IN_REPR]
        )
        if (self._length > ArrayPermutator._ARRAY_ELEMENTS_CNT_IN_REPR):
            str_array = str_array[:-1] + \
                ', ...] with length {0}'.format(self._length)
        return 'Requested {0} from {1}'.format(self._requested_cnt, str_array)

    def __repr__(self):
        return object.__repr__(self)[:-1] + ' (' + self.__str__() + ')>'
