
from numba import njit


@njit(cache=True, fastmath=True)
def linear_eigenmode_from_values_1k(ux_fft, uy_fft, eta_fft, kx, ky, f, c2):
    """Compute q, d, a (fft) for a single wavenumber."""
    div_fft = 1j * (kx * ux_fft + ky * uy_fft)
    rot_fft = 1j * (kx * uy_fft - ky * ux_fft)
    q_fft = rot_fft - f * eta_fft
    k2 = kx ** 2 + ky ** 2
    ageo_fft = f * rot_fft / c2 + k2 * eta_fft
    return (q_fft, div_fft, ageo_fft)


def __transonic__():
    return '0.8.0'
