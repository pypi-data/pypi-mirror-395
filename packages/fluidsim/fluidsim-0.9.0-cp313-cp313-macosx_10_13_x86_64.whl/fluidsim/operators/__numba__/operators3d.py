
from numba import njit
import numpy as np
from random import uniform


@njit(cache=True, fastmath=True)
def dealiasing_setofvar(sov, where_dealiased):
    """Dealiasing 3d setofvar object.

    Parameters
    ----------

    sov : 4d ndarray
        A set of variables array.

    where_dealiased : 3d ndarray
        A 3d array of "booleans" (actually uint8).

    """
    nk, n0, n1, n2 = sov.shape
    for i0 in range(n0):
        for i1 in range(n1):
            for i2 in range(n2):
                if where_dealiased[i0, i1, i2]:
                    for ik in range(nk):
                        sov[ik, i0, i1, i2] = 0.0


@njit(cache=True, fastmath=True)
def dealiasing_variable(ff_fft, where_dealiased):
    """Dealiasing 3d array"""
    n0, n1, n2 = ff_fft.shape
    for i0 in range(n0):
        for i1 in range(n1):
            for i2 in range(n2):
                if where_dealiased[i0, i1, i2]:
                    ff_fft[i0, i1, i2] = 0.0


@njit(cache=True, fastmath=True)
def compute_energy_from_1field(arr):
    return 0.5 * np.abs(arr) ** 2


@njit(cache=True, fastmath=True)
def compute_energy_from_1field_with_coef(arr, coef):
    return 0.5 * coef * np.abs(arr) ** 2


@njit(cache=True, fastmath=True)
def compute_energy_from_2fields(vx, vy):
    return 0.5 * (np.abs(vx) ** 2 + np.abs(vy) ** 2)


@njit(cache=True, fastmath=True)
def compute_energy_from_3fields(vx, vy, vz):
    return 0.5 * (np.abs(vx) ** 2 + np.abs(vy) ** 2 + np.abs(vz) ** 2)


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft(self_Kx, self_Ky, vx_fft, vy_fft):
    """Compute toroidal and poloidal horizontal velocities.

        urx_fft, ury_fft contain shear modes!

        """
    inv_Kh_square_nozero = self_Kx ** 2 + self_Ky ** 2
    inv_Kh_square_nozero[inv_Kh_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1 / inv_Kh_square_nozero
    kdotu_fft = self_Kx * vx_fft + self_Ky * vy_fft
    udx_fft = kdotu_fft * self_Kx * inv_Kh_square_nozero
    udy_fft = kdotu_fft * self_Ky * inv_Kh_square_nozero
    urx_fft = vx_fft - udx_fft
    ury_fft = vy_fft - udy_fft
    return (urx_fft, ury_fft, udx_fft, udy_fft)


def __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft():
    return '\n\ndef new_method(self, vx_fft, vy_fft):\n    return backend_func(self.Kx, self.Ky, vx_fft, vy_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__project_kradial3d(self_Kx, self_Ky, self_Kz, vx_fft, vy_fft, vz_fft):
    """Project (inplace) a vector field parallel to the k-radial direction of the wavevector.

        Parameters
        ----------

        Arrays containing the velocity in Fourier space.

        Notes
        -----

        .. |kk| mathmacro:: \\mathbf{k}
        .. |ee| mathmacro:: \\mathbf{e}
        .. |vv| mathmacro:: \\mathbf{v}

        The radial unitary vector for the mode :math:`\\kk` is

        .. math::

           \\ee_\\kk = \\frac{\\kk}{|\\kk|}
           = \\sin \\theta_\\kk \\cos \\varphi_\\kk ~ \\ee_x
           + \\sin \\theta_\\kk \\sin \\varphi_\\kk ~ \\ee_y
           + \\cos \\theta_\\kk ~ \\ee_z,

        and the projection of a velocity mode :math:`\\hat{\\vv}_\\kk` along
        :math:`\\ee_\\kk` is

        .. math:: \\hat{v}_\\kk ~ \\ee_\\kk \\equiv \\hat{\\vv}_\\kk \\cdot \\ee_\\kk ~ \\ee_\\kk

        This function set :math:`\\hat{\\vv}_\\kk = \\hat{v}_\\kk ~ \\ee_\\kk` for all
        modes.

        .. note:

           For a divergent less vector field, the resulting vector is zero.

        """
    K_square_nozero = self_Kx ** 2 + self_Ky ** 2 + self_Kz ** 2
    K_square_nozero[K_square_nozero == 0] = 1e-14
    inv_K_square_nozero = 1.0 / K_square_nozero
    tmp = (self_Kx * vx_fft + self_Ky * vy_fft +
           self_Kz * vz_fft) * inv_K_square_nozero
    n0, n1, n2 = vx_fft.shape
    for i0 in range(n0):
        for i1 in range(n1):
            for i2 in range(n2):
                vx_fft[i0, i1, i2] = self_Kx[i0, i1, i2] * tmp[i0, i1, i2]
                vy_fft[i0, i1, i2] = self_Ky[i0, i1, i2] * tmp[i0, i1, i2]
                vz_fft[i0, i1, i2] = self_Kz[i0, i1, i2] * tmp[i0, i1, i2]


def __code_new_method__OperatorsPseudoSpectral3D__project_kradial3d():
    return '\n\ndef new_method(self, vx_fft, vy_fft, vz_fft):\n    return backend_func(self.Kx, self.Ky, self.Kz, vx_fft, vy_fft, vz_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__project_poloidal(self_Kx, self_Ky, self_Kz, vx_fft, vy_fft, vz_fft):
    """Project (inplace) a vector field parallel to the k-poloidal (or polar) direction.

        Parameters
        ----------

        Arrays containing the velocity in Fourier space.

        Notes
        -----

        The poloidal unitary vector for the mode :math:`\\kk` is

        .. math::

           \\ee_{\\kk\\theta}
           = \\cos \\theta_\\kk \\cos \\varphi_\\kk ~ \\ee_x
           + \\cos \\theta_\\kk \\sin \\varphi_\\kk ~ \\ee_y - \\sin \\theta_\\kk ~ \\ee_z,

        and the projection of a velocity mode :math:`\\hat{\\vv}_\\kk` along
        :math:`\\ee_{\\kk\\theta}` is

        .. math::

           \\hat{v}_{\\kk\\theta} ~ \\ee_{\\kk\\theta}
           \\equiv \\hat{\\vv}_\\kk \\cdot \\ee_{\\kk\\theta} ~ \\ee_{\\kk\\theta}

        This function set :math:`\\hat{\\vv}_\\kk = \\hat{v}_{\\kk\\theta} ~
        \\ee_{\\kk\\theta}` for all modes.
        """
    Kh_square = self_Kx ** 2 + self_Ky ** 2
    K_square_nozero = Kh_square + self_Kz ** 2
    Kh_square_nozero = Kh_square.copy()
    Kh_square_nozero[Kh_square_nozero == 0] = 1e-14
    K_square_nozero[K_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1.0 / Kh_square_nozero
    inv_K_square_nozero = 1.0 / K_square_nozero
    cos_theta_k = self_Kz * np.sqrt(inv_K_square_nozero)
    sin_theta_k = np.sqrt(Kh_square * inv_K_square_nozero)
    cos_phi_k = self_Kx * np.sqrt(inv_Kh_square_nozero)
    sin_phi_k = self_Ky * np.sqrt(inv_Kh_square_nozero)
    tmp = cos_theta_k * cos_phi_k * vx_fft + cos_theta_k * \
        sin_phi_k * vy_fft - sin_theta_k * vz_fft
    n0, n1, n2 = vx_fft.shape
    for i0 in range(n0):
        for i1 in range(n1):
            for i2 in range(n2):
                vx_fft[i0, i1, i2] = cos_theta_k[i0, i1, i2] * \
                    cos_phi_k[i0, i1, i2] * tmp[i0, i1, i2]
                vy_fft[i0, i1, i2] = cos_theta_k[i0, i1, i2] * \
                    sin_phi_k[i0, i1, i2] * tmp[i0, i1, i2]
                vz_fft[i0, i1, i2] = -sin_theta_k[i0, i1, i2] * tmp[i0, i1, i2]


def __code_new_method__OperatorsPseudoSpectral3D__project_poloidal():
    return '\n\ndef new_method(self, vx_fft, vy_fft, vz_fft):\n    return backend_func(self.Kx, self.Ky, self.Kz, vx_fft, vy_fft, vz_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__vpfft_from_vecfft(self_Kx, self_Ky, self_Kz, vx_fft, vy_fft, vz_fft):
    """Return the poloidal component of a vector field."""
    Kh_square = self_Kx ** 2 + self_Ky ** 2
    K_square_nozero = Kh_square + self_Kz ** 2
    Kh_square_nozero = Kh_square.copy()
    Kh_square_nozero[Kh_square_nozero == 0] = 1e-14
    K_square_nozero[K_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1.0 / Kh_square_nozero
    inv_K_square_nozero = 1.0 / K_square_nozero
    cos_theta_k = self_Kz * np.sqrt(inv_K_square_nozero)
    sin_theta_k = np.sqrt(Kh_square * inv_K_square_nozero)
    cos_phi_k = self_Kx * np.sqrt(inv_Kh_square_nozero)
    sin_phi_k = self_Ky * np.sqrt(inv_Kh_square_nozero)
    result = cos_theta_k * cos_phi_k * vx_fft + \
        cos_theta_k * sin_phi_k * vy_fft - sin_theta_k * vz_fft
    return result


def __code_new_method__OperatorsPseudoSpectral3D__vpfft_from_vecfft():
    return '\n\ndef new_method(self, vx_fft, vy_fft, vz_fft):\n    return backend_func(self.Kx, self.Ky, self.Kz, vx_fft, vy_fft, vz_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__vecfft_from_vpfft(self_Kx, self_Ky, self_Kz, vp_fft):
    """Return a vector field from the poloidal component."""
    Kh_square = self_Kx ** 2 + self_Ky ** 2
    K_square_nozero = Kh_square + self_Kz ** 2
    Kh_square_nozero = Kh_square.copy()
    Kh_square_nozero[Kh_square_nozero == 0] = 1e-14
    K_square_nozero[K_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1.0 / Kh_square_nozero
    inv_K_square_nozero = 1.0 / K_square_nozero
    cos_theta_k = self_Kz * np.sqrt(inv_K_square_nozero)
    sin_theta_k = np.sqrt(Kh_square * inv_K_square_nozero)
    cos_phi_k = self_Kx * np.sqrt(inv_Kh_square_nozero)
    sin_phi_k = self_Ky * np.sqrt(inv_Kh_square_nozero)
    ux_fft = cos_theta_k * cos_phi_k * vp_fft
    uy_fft = cos_theta_k * sin_phi_k * vp_fft
    uz_fft = -sin_theta_k * vp_fft
    return (ux_fft, uy_fft, uz_fft)


def __code_new_method__OperatorsPseudoSpectral3D__vecfft_from_vpfft():
    return '\n\ndef new_method(self, vp_fft):\n    return backend_func(self.Kx, self.Ky, self.Kz, vp_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__project_toroidal(self_Kx, self_Ky, vx_fft, vy_fft, vz_fft):
    """Project (inplace) a vector field parallel to the k-toroidal (or azimutal) direction.

        Parameters
        ----------

        Arrays containing the velocity in Fourier space.

        Notes
        -----

        The toroidal unitary vector for the mode :math:`\\kk` is

        .. math::

           \\ee_{\\kk\\varphi}
           = - \\sin \\varphi_\\kk ~ \\ee_x + \\cos \\varphi_\\kk ~ \\mathbb{e}_y,

        and the projection of a velocity mode :math:`\\hat{\\vv}_\\kk` along
        :math:`\\ee_{\\kk\\varphi}` is

        .. math::

           \\hat{v}_{\\kk\\varphi} ~ \\ee_{\\kk\\varphi}
           \\equiv \\hat{\\vv}_\\kk \\cdot \\ee_{\\kk\\varphi} ~ \\ee_{\\kk\\varphi}

        This function compute :math:`\\hat{\\vv}_\\kk = \\hat{v}_{\\kk\\varphi} ~
        \\ee_{\\kk\\varphi}` for all modes.
        """
    Kh_square_nozero = self_Kx ** 2 + self_Ky ** 2
    Kh_square_nozero[Kh_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1.0 / Kh_square_nozero
    del Kh_square_nozero
    tmp = np.sqrt(inv_Kh_square_nozero)
    cos_phi_k = self_Kx * tmp
    sin_phi_k = self_Ky * tmp
    tmp = -sin_phi_k * vx_fft + cos_phi_k * vy_fft
    n0, n1, n2 = vx_fft.shape
    for i0 in range(n0):
        for i1 in range(n1):
            for i2 in range(n2):
                vx_fft[i0, i1, i2] = -sin_phi_k[i0, i1, i2] * tmp[i0, i1, i2]
                vy_fft[i0, i1, i2] = cos_phi_k[i0, i1, i2] * tmp[i0, i1, i2]
                vz_fft[i0, i1, i2] = 0.0


def __code_new_method__OperatorsPseudoSpectral3D__project_toroidal():
    return '\n\ndef new_method(self, vx_fft, vy_fft, vz_fft):\n    return backend_func(self.Kx, self.Ky, vx_fft, vy_fft, vz_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__vtfft_from_vecfft(self_Kx, self_Ky, vx_fft, vy_fft, vz_fft):
    """Return the toroidal component of a vector field."""
    Kh_square_nozero = self_Kx ** 2 + self_Ky ** 2
    Kh_square_nozero[Kh_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1.0 / Kh_square_nozero
    del Kh_square_nozero
    tmp = np.sqrt(inv_Kh_square_nozero)
    cos_phi_k = self_Kx * tmp
    sin_phi_k = self_Ky * tmp
    result = -1j * sin_phi_k * vx_fft + 1j * cos_phi_k * vy_fft
    return result


def __code_new_method__OperatorsPseudoSpectral3D__vtfft_from_vecfft():
    return '\n\ndef new_method(self, vx_fft, vy_fft, vz_fft):\n    return backend_func(self.Kx, self.Ky, vx_fft, vy_fft, vz_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__vecfft_from_vtfft(self_Kx, self_Ky, vt_fft):
    """Return a 3D vector field from the toroidal component."""
    Kh_square_nozero = self_Kx ** 2 + self_Ky ** 2
    Kh_square_nozero[Kh_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1.0 / Kh_square_nozero
    tmp = np.sqrt(inv_Kh_square_nozero)
    cos_phi_k = self_Kx * tmp
    sin_phi_k = self_Ky * tmp
    ux_fft = 1j * sin_phi_k * vt_fft
    uy_fft = -1j * cos_phi_k * vt_fft
    return (ux_fft, uy_fft, np.zeros_like(vt_fft))


def __code_new_method__OperatorsPseudoSpectral3D__vecfft_from_vtfft():
    return '\n\ndef new_method(self, vt_fft):\n    return backend_func(self.Kx, self.Ky, vt_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft(self_Kx, self_Ky, vx_fft, vy_fft):
    """Compute the horizontal divergence in spectral space."""
    return 1j * (self_Kx * vx_fft + self_Ky * vy_fft)


def __code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft():
    return '\n\ndef new_method(self, vx_fft, vy_fft):\n    return backend_func(self.Kx, self.Ky, vx_fft, vy_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft(self_Kx, self_Ky, rotz_fft):
    inv_Kh_square_nozero = self_Kx ** 2 + self_Ky ** 2
    inv_Kh_square_nozero[inv_Kh_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1 / inv_Kh_square_nozero
    vx_fft = 1j * self_Ky * inv_Kh_square_nozero * rotz_fft
    vy_fft = -1j * self_Kx * inv_Kh_square_nozero * rotz_fft
    return (vx_fft, vy_fft)


def __code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft():
    return '\n\ndef new_method(self, rotz_fft):\n    return backend_func(self.Kx, self.Ky, rotz_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__vxvyfft_from_divhfft(self_Kx, self_Ky, divh_fft):
    inv_Kh_square_nozero = self_Kx ** 2 + self_Ky ** 2
    inv_Kh_square_nozero[inv_Kh_square_nozero == 0] = 1e-14
    inv_Kh_square_nozero = 1 / inv_Kh_square_nozero
    vx_fft = -1j * self_Kx * inv_Kh_square_nozero * divh_fft
    vy_fft = -1j * self_Ky * inv_Kh_square_nozero * divh_fft
    return (vx_fft, vy_fft)


def __code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_divhfft():
    return '\n\ndef new_method(self, divh_fft):\n    return backend_func(self.Kx, self.Ky, divh_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__grad_fft_from_arr_fft(self_Kx, self_Ky, self_Kz, arr_fft):
    dx_arr_fft = np.empty_like(arr_fft)
    dy_arr_fft = np.empty_like(arr_fft)
    dz_arr_fft = np.empty_like(arr_fft)
    dx_arr_fft_flat = dx_arr_fft.ravel()
    dy_arr_fft_flat = dy_arr_fft.ravel()
    dz_arr_fft_flat = dz_arr_fft.ravel()
    Kx = self_Kx.ravel()
    Ky = self_Ky.ravel()
    Kz = self_Kz.ravel()
    for i, value in enumerate(arr_fft.flat):
        dx_arr_fft_flat[i] = 1j * Kx[i] * value
        dy_arr_fft_flat[i] = 1j * Ky[i] * value
        dz_arr_fft_flat[i] = 1j * Kz[i] * value
    return (dx_arr_fft, dy_arr_fft, dz_arr_fft)


def __code_new_method__OperatorsPseudoSpectral3D__grad_fft_from_arr_fft():
    return '\n\ndef new_method(self, arr_fft):\n    return backend_func(self.Kx, self.Ky, self.Kz, arr_fft)\n\n'


@njit(cache=True, fastmath=True)
def __for_method__OperatorsPseudoSpectral3D__get_phases_random(self_Kx, self_Ky, self_Kz, self_deltax, self_deltay, self_deltaz):
    # Not supported by Pythran 0.9.5!
    # alpha_x, alpha_y, alpha_z = np.random.uniform(-0.5, 0.5, 3)
    alpha_x, alpha_y, alpha_z = tuple((uniform(-0.5, 0.5) for _ in range(3)))
    beta_x = alpha_x + 0.5 if alpha_x < 0 else alpha_x - 0.5
    beta_y = alpha_y + 0.5 if alpha_y < 0 else alpha_y - 0.5
    beta_z = alpha_z + 0.5 if alpha_z < 0 else alpha_z - 0.5
    phase_alpha = alpha_x * self_deltax * self_Kx + alpha_y * \
        self_deltay * self_Ky + alpha_z * self_deltaz * self_Kz
    phase_beta = beta_x * self_deltax * self_Kx + beta_y * \
        self_deltay * self_Ky + beta_z * self_deltaz * self_Kz
    return (phase_alpha, phase_beta)


def __code_new_method__OperatorsPseudoSpectral3D__get_phases_random():
    return '\n\ndef new_method(self, ):\n    return backend_func(self.Kx, self.Ky, self.Kz, self.deltax, self.deltay, self.deltaz, )\n\n'


def __transonic__():
    return '0.8.0'
