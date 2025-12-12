
from numba import njit


@njit(cache=True, fastmath=True)
def tendencies_nonlin_ns2dbouss(ux, uy, px_rot, py_rot, px_b, py_b):
    Frot = -ux * px_rot - uy * py_rot + px_b
    Fb = -ux * px_b - uy * py_b
    return (Frot, Fb)


def __transonic__():
    return '0.8.0'
