
from numba import njit
import numpy as np


@njit(cache=True, fastmath=True)
def compute_spectrum_kzkhomega(field_k0k1omega, khs, kzs, KX, KZ, KH):
    """Compute the kz-kh-omega spectrum."""
    deltakh = khs[1]
    deltakz = kzs[1]
    nkh = len(khs)
    nkz = len(kzs)
    nk0, nk1, nomega = field_k0k1omega.shape
    spectrum_kzkhomega = np.zeros(
        (nkz, nkh, nomega), dtype=field_k0k1omega.dtype)
    for ik0 in range(nk0):
        for ik1 in range(nk1):
            values = field_k0k1omega[ik0, ik1, :]
            kx = KX[ik0, ik1]
            if kx != 0.0:
                # warning: we should also consider another condition
                # (kx != kx_max) but it is not necessary here mainly
                # because of dealiasing
                values = 2 * values
            kappa = KH[ik0, ik1]
            ikh = int(kappa / deltakh)
            kz = abs(KZ[ik0, ik1])
            ikz = int(round(kz / deltakz))
            if ikz >= nkz - 1:
                ikz = nkz - 1
            if ikh >= nkh - 1:
                ikh = nkh - 1
                for i, value in enumerate(values):
                    spectrum_kzkhomega[ikz, ikh, i] += value
            else:
                coef_share = (kappa - khs[ikh]) / deltakh
                for i, value in enumerate(values):
                    spectrum_kzkhomega[ikz, ikh, i] += (1 - coef_share) * value
                    spectrum_kzkhomega[ikz, ikh + 1, i] += coef_share * value
    # get one-sided spectrum in the omega dimension
    nomega = (nomega + 1) // 2
    spectrum_onesided = np.zeros((nkz, nkh, nomega))
    spectrum_onesided[:, :, 0] = spectrum_kzkhomega[:, :, 0]
    spectrum_onesided[:, :, 1:] = spectrum_kzkhomega[:, :,
                                                     1:nomega] + spectrum_kzkhomega[:, :, -1:-nomega:-1]
    return spectrum_onesided / (deltakz * deltakh)


def __transonic__():
    return '0.8.0'
