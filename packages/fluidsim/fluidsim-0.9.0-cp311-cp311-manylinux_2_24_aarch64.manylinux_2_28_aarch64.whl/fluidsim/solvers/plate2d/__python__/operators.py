def monge_ampere_step0(a_fft, b_fft, KX2, KY2, KXKZ):
    pxx_a_fft = -a_fft * KX2
    pyy_a_fft = -a_fft * KY2
    pxy_a_fft = -a_fft * KXKZ
    pxx_b_fft = -b_fft * KX2
    pyy_b_fft = -b_fft * KY2
    pxy_b_fft = -b_fft * KXKZ
    return (pxx_a_fft, pyy_a_fft, pxy_a_fft, pxx_b_fft, pyy_b_fft, pxy_b_fft)


def monge_ampere_step1(pxx_a, pyy_a, pxy_a, pxx_b, pyy_b, pxy_b):
    return pxx_a * pyy_b + pyy_a * pxx_b - 2 * pxy_a * pxy_b


def __transonic__(): return "0.8.0"
