def compute_fb_fft(div_vb_fft, N, vz_fft):
    fb_fft = div_vb_fft
    fb_fft[:] = -div_vb_fft - N ** 2 * vz_fft
    return fb_fft


def __transonic__(): return "0.8.0"
