import numpy as np


def step_Euler(state_spect, dt, tendencies, diss, output):
    output[:] = (state_spect + dt * tendencies) * diss
    return output


def step_Euler_inplace(state_spect, dt, tendencies, diss):
    step_Euler(state_spect, dt, tendencies, diss, state_spect)


def step_like_RK2(state_spect, dt, tendencies, diss, diss2):
    state_spect[:] = state_spect * diss + dt * diss2 * tendencies


def mean_with_phaseshift(tendencies_0, tendencies_1_shift, phaseshift, output):
    output[:] = 0.5 * (tendencies_0 + tendencies_1_shift / phaseshift)
    return output


def mean_elementwise(tendencies_0, tendencies_1, output):
    output[:] = 0.5 * (tendencies_0 + tendencies_1)
    return output


def mul(phaseshift, state_spect, output):
    output[:] = phaseshift * state_spect
    return output


def div_inplace(arr, phaseshift):
    arr /= phaseshift
    return arr


def compute_phaseshift_terms(phase_alpha, phase_beta, phaseshift_alpha, phaseshift_beta):
    phaseshift_alpha[:] = np.exp(1j * phase_alpha)
    phaseshift_beta[:] = np.exp(1j * phase_beta)
    return (phaseshift_alpha, phaseshift_beta)


def exact_lin_compute(f_lin, exact, exact2, dt):

    # transonic block (
    #     A1 f_lin, exact, exact2;
    #     float dt
    # )
    # transonic block (
    #     A2 f_lin, exact, exact2;
    #     float dt
    # )
    exact[:] = np.exp(-dt * f_lin)
    exact2[:] = np.exp(-dt / 2 * f_lin)


def rk2_tendencies_d(tendencies_d, tendencies_0, tendencies_1_shift, phaseshift):

    # transonic block (
    #     A tendencies_d, tendencies_0, tendencies_1_shift;
    #     Am1 phaseshift;
    # )
    tendencies_d[:] = 0.5 * (tendencies_0 + tendencies_1_shift / phaseshift)


def rk2_exact(tendencies_d, tendencies_d0, tendencies_1, tendencies_1_shift, phaseshift):

    # based on approximation 1
    # transonic block (
    #     A tendencies_d, tendencies_d0, tendencies_1, tendencies_1_shift;
    #     Am1 phaseshift
    # )
    tendencies_d[:] = 0.5 * (tendencies_d0 + 0.5 *
                             (tendencies_1 + tendencies_1_shift / phaseshift))


def rk4_step1(state_spect, state_spect_tmp, state_spect_12_approx2, tendencies_1, diss2, dt):

    # based on approximation 1
    # transonic block (
    #     A state_spect, state_spect_tmp,
    #       state_spect_12_approx2, tendencies_1;
    #     A1 diss2;
    #     float dt
    # )
    # transonic block (
    #     A state_spect, state_spect_tmp,
    #       state_spect_12_approx2, tendencies_1;
    #     A2 diss2;
    #     float dt
    # )
    state_spect_tmp[:] += dt / 3 * diss2 * tendencies_1
    state_spect_12_approx2[:] = state_spect * diss2 + dt / 2 * tendencies_1


def rk4_step2(state_spect, state_spect_tmp, state_spect_1_approx, tendencies_2, diss, diss2, dt):

    # based on approximation 2
    # transonic block (
    #     A state_spect, state_spect_tmp,
    #       state_spect_1_approx, tendencies_2;
    #     A1 diss, diss2;
    #     float dt
    # )
    # transonic block (
    #     A state_spect, state_spect_tmp,
    #       state_spect_1_approx, tendencies_2;
    #     A2 diss, diss2;
    #     float dt
    # )
    state_spect_tmp[:] += dt / 3 * diss2 * tendencies_2
    state_spect_1_approx[:] = state_spect * diss + dt * diss2 * tendencies_2


def rk4_step3(state_spect, state_spect_tmp, tendencies_3, dt):

    # result using the 4 approximations
    # transonic block (
    #     A state_spect, state_spect_tmp, tendencies_3;
    #     float dt
    # )
    state_spect[:] = state_spect_tmp + dt / 6 * tendencies_3


def arguments_blocks(): return {'exact_lin_compute': ['f_lin', 'exact', 'exact2', 'dt'], 'rk2_tendencies_d': ['tendencies_d', 'tendencies_0', 'tendencies_1_shift', 'phaseshift'], 'rk2_exact': ['tendencies_d', 'tendencies_d0', 'tendencies_1', 'tendencies_1_shift', 'phaseshift'], 'rk4_step1': [
    'state_spect', 'state_spect_tmp', 'state_spect_12_approx2', 'tendencies_1', 'diss2', 'dt'], 'rk4_step2': ['state_spect', 'state_spect_tmp', 'state_spect_1_approx', 'tendencies_2', 'diss', 'diss2', 'dt'], 'rk4_step3': ['state_spect', 'state_spect_tmp', 'tendencies_3', 'dt']}


def __transonic__(): return "0.8.0"
