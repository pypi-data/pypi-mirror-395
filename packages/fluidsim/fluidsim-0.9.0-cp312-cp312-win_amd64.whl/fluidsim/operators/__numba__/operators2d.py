
from numba import njit
from random import uniform


@njit(cache=True, fastmath=True)
def laplacian_fft(a_fft, Kn):
    """Compute the n-th order Laplacian."""
    return a_fft * Kn


@njit(cache=True, fastmath=True)
def invlaplacian_fft(a_fft, Kn_not0, rank):
    """Compute the n-th order inverse Laplacian."""
    invlap_afft = a_fft / Kn_not0
    if rank == 0:
        invlap_afft[0, 0] = 0.0
    return invlap_afft


@njit(cache=True, fastmath=True)
def compute_increments_dim1(var, irx):
    """Compute the increments of var over the dim 1."""
    n1 = var.shape[1]
    n1new = n1 - irx
    # bug for gast 0.4.0 (https://github.com/serge-sans-paille/gast/issues/48)
    inc_var = var[:, irx:n1] - var[:, 0:n1new]
    return inc_var


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar(self__has_to_dealiase, self_where_dealiased, sov):
    """Dealiasing of a setofvar arrays."""
    if self__has_to_dealiase:
        nk, n0, n1 = sov.shape
        for i0 in range(n0):
            for i1 in range(n1):
                if self_where_dealiased[i0, i1]:
                    for ik in range(nk):
                        sov[ik, i0, i1] = 0.0


def __code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar():
    return '\n\ndef new_method(self, sov):\n    return backend_func(self._has_to_dealiase, self.where_dealiased, sov)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral2D__get_phases_random(self_KX, self_KY, self_deltax, self_deltay):
    # Not supported by Pythran 0.9.5!
    # alpha_x, alpha_y = np.random.uniform(-0.5, 0.5, 2)
    alpha_x, alpha_y = tuple((uniform(-0.5, 0.5) for _ in range(2)))
    beta_x = alpha_x + 0.5 if alpha_x < 0 else alpha_x - 0.5
    beta_y = alpha_y + 0.5 if alpha_y < 0 else alpha_y - 0.5
    phase_alpha = alpha_x * self_deltax * self_KX + alpha_y * self_deltay * self_KY
    phase_beta = beta_x * self_deltax * self_KX + beta_y * self_deltay * self_KY
    return (phase_alpha, phase_beta)


def __code_new_method__OperatorsPseudoSpectral2D__get_phases_random():
    return '\n\ndef new_method(self, ):\n    return backend_func(self.KX, self.KY, self.deltax, self.deltay, )\n\n'


def __transonic__():
    return '0.8.0'
