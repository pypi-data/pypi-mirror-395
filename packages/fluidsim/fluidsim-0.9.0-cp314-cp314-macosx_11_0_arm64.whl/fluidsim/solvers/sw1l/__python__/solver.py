def compute_Frot(rot, ux, uy, f):
    """Compute cross-product of absolute potential vorticity with velocity."""
    if f != 0:
        rot_abs = rot + f
    else:
        rot_abs = rot
    F1x = rot_abs * uy
    F1y = -rot_abs * ux
    return (F1x, F1y)


def compute_pressure(c2, eta, ux, uy):
    return c2 * eta + 0.5 * (ux ** 2 + uy ** 2)


def __transonic__(): return "0.8.0"
