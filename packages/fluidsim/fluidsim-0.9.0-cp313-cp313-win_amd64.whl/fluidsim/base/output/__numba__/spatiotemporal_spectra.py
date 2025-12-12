
from numba import njit
import numpy as np


@njit(cache=True, fastmath=True)
def find_index_first_geq(arr, value):
    """find the first index such that `arr[index] >= value`"""
    for i, v in enumerate(arr):
        if v >= value:
            return i
    print('arr', arr)
    raise ValueError(
        f'No index such that `arr[index] >= value (={value:.8g})`')


@njit(cache=True, fastmath=True)
def find_index_first_g(arr, value):
    """find the first index such that `arr[index] > value`"""
    for i, v in enumerate(arr):
        if v > value:
            return i
    print('arr', arr)
    raise ValueError(
        f'No index such that `arr[index] >= value (={value:.8g})`')


@njit(cache=True, fastmath=True)
def find_index_first_l(arr, value):
    """find the first index such that `arr[index] < value`"""
    for i, v in enumerate(arr):
        if v < value:
            return i
    print('arr', arr)
    raise ValueError(
        f'No index such that `arr[index] >= value (={value:.8g})`')


@njit(cache=True, fastmath=True)
def get_arange_minmax(times, tmin, tmax):
    """get a range of index for which `tmin <= times[i] <= tmax`

    This assumes that `times` is sorted.

    """
    if tmin <= times[0]:
        start = 0
    else:
        start = find_index_first_geq(times, tmin)
    if tmax >= times[-1]:
        stop = len(times)
    else:
        stop = find_index_first_g(times, tmax)
    return np.arange(start, stop)


def __transonic__():
    return '0.8.0'
