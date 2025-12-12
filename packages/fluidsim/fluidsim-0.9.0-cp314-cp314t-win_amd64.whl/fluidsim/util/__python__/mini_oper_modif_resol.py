def fill_field_fft_3d(field_fft_in, field_fft_out):
    """Fill the values from field_fft_in in field_fft_out

    This function is specialized for FFTW3DReal2Complex (no MPI).
    """
    [nk0_out, nk1_out, nk2_out] = field_fft_out.shape
    [nk0_in, nk1_in, nk2_in] = field_fft_in.shape
    nk0_min = min(nk0_out, nk0_in)
    nk1_min = min(nk1_out, nk1_in)
    nk2_min = min(nk2_out, nk2_in)
    for ik0 in range(nk0_min // 2 + 1):
        for ik1 in range(nk1_min // 2 + 1):
            for ik2 in range(nk2_min):
                # positive wavenumbers
                field_fft_out[ik0, ik1, ik2] = field_fft_in[ik0, ik1, ik2]
                # negative wavenumbers
                if ik0 > 0 and ik0 < nk0_min // 2:
                    field_fft_out[-ik0, ik1,
                                  ik2] = field_fft_in[-ik0, ik1, ik2]
                    if ik1 > 0 and ik1 < nk1_min // 2:
                        field_fft_out[-ik0, -ik1,
                                      ik2] = field_fft_in[-ik0, -ik1, ik2]
                if ik1 > 0 and ik1 < nk1_min // 2:
                    field_fft_out[ik0, -ik1,
                                  ik2] = field_fft_in[ik0, -ik1, ik2]


def __transonic__(): return "0.8.0"
