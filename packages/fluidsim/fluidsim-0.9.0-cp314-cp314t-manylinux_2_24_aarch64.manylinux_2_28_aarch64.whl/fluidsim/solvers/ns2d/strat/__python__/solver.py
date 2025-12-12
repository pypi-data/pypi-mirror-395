def tendencies_nonlin_ns2dstrat(ux, uy, px_rot, py_rot, px_b, py_b, N):
    Frot = -ux * px_rot - uy * py_rot
    Fb = -ux * px_b - uy * py_b - N ** 2 * uy
    return (Frot, Fb)


def __transonic__(): return "0.8.0"
