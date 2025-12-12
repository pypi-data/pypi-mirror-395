import numpy as np
from numpy.linalg import inv


def gsm_disc(
        Zs,     # Wave's Impedances - GUIDE S
        Yw,     # Wave's Admittances - GUIDE W
        Xbar    # normalised inner products
):
    # GSM_DISC Compute the W->S discontinuity's GSM

    Iw = np.eye(Xbar.shape[1])
    Is = np.eye(Xbar.shape[0])

    Zs = np.diagflat(Zs.reshape(-1,))
    Yw = np.diagflat(Yw.reshape(-1,))

    # GSM computation
    # Arbitrary constants usually chosen to be unitary
    X = Zs @ Xbar @ Yw
    F = 2. * inv(Is + X @ X.T)
    G = X.T @ F

    Sww = G @ X - Iw
    Sws = G
    Ssw = F @ X
    Sss = F - Is
    return Sww, Sws, Ssw, Sss


def cascade_guide_gsm(
        L,      # waveguide's longitudinal length
        gamma,  # propagation constants
        do_reverse,
        S11b, S12b, S21b, S22b
):
    if do_reverse:
        # Real config: [S guide -> (S->W)]
        # Computed   : [(W->S)]
        # Need to compute:
        #   - [(W->S) -> GuideS]
        #   - 'transposes' the S parameters to have: [GuideS -> (S->W)]
        S22c, S21c, S12c, S11c = cascade_gsm_guide(L, gamma,
                                                   S11b, S12b, S21b, S22b)
    else:
        # Real config: [W guide -> (W->S)]
        # Computed   : [(W->S)]
        # Need to compute:
        #   - [GuideW -> (W->S)]

        # Guide:a
        Ya = np.diagflat(np.exp(-gamma * L))

        # Guide:a - Discontinuity:b -> c
        S11c = Ya @ S11b @ Ya
        S12c = Ya @ S12b
        S21c = S21b @ Ya
        S22c = S22b

    return S11c, S12c, S21c, S22c


def cascade_gsm_guide(
        L,      # waveguide's longitudinal length
        gamma,  # propagation constants
        S11a, S12a, S21a, S22a
):

    # Guide:b
    Yb = np.diagflat(np.exp(-gamma * L))

    # (Previous GSM):a - Guide:b
    S_11 = S11a
    S_12 = S12a @ Yb
    S_21 = Yb @ S21a
    S_22 = Yb @ S22a @ Yb

    return S_11, S_12, S_21, S_22


def cascade_gsm(
        L,                       # waveguide's longitudinal length
        gamma,                   # propagation constants
        do_reverse,
        S11a, S12a, S21a, S22a,  # GSM 1
        Sww, Sws, Ssw, Sss       # GSM 2
):
    # Add a waveguide junction between GSM1 and GSM2
    Y = np.diagflat(np.exp(-gamma * L))
    if do_reverse:
        S11b = Sss
        S12b = Ssw
        S21b = Sws
        S22b = Sww
    else:
        S11b = Sww
        S12b = Sws
        S21b = Ssw
        S22b = Sss

    # Compute the new GSM
    I = np.eye(Y.shape[0])
    H = inv(I - S11b @ Y @ S22a @ Y)
    S11 = S11a + S12a @ Y @ H @ S11b @ Y @ S21a
    S12 = S12a @ Y @ H @ S12b
    S21 = S21b @ Y @ (I + S22a @ Y @ H @ S11b @ Y) @ S21a
    S22 = S22b + S21b @ Y @ S22a @ Y @ H @ S12b

    return S11, S12, S21, S22

