
from numba import njit


@njit(cache=True, fastmath=True)
def compute_Frot(ux, uy, px_rot, py_rot, beta=0):
    if beta == 0:
        return -ux * px_rot - uy * py_rot
    else:
        return -ux * px_rot - uy * (py_rot + beta)


def __transonic__():
    return '0.8.0'
