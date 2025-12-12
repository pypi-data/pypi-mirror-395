import numpy as np
from numpy import pi, sqrt, cos, sin

from scipy import integrate

from qosm.sources.mode_matching.fn_gsm import gsm_disc, cascade_gsm_guide, cascade_guide_gsm, cascade_gsm
from qosm.sources.mode_matching.fn_mm import sort_modes, compute_x
from qosm.utils.Field import Field


def evanescent_modes(
        freq: float,
        kt: np.ndarray
):
    k0 = (2 * pi * freq / 299792458)
    kch2 = np.reshape(np.sum(kt ** 2, 1), (-1,))
    print((kch2 - k0**2) > 0)
    return (kch2 - k0**2) > 0


def rect_aperture_modes(
        freq: float,
        Nm: int,
        xa: np.array,
        ya: np.array,
):
    k0 = (2 * pi * freq / 299792458)

    Lx = 2. * xa.max()
    Ly = 2. * ya.max()

    eps0 = 8.854187817e-12
    mu0 = 4 * pi * 1e-7
    Z0 = sqrt(mu0 / eps0)

    kt, mn = sort_modes(Nm, Lx, Ly)
    kt_te = kt[0]

    m = np.reshape(mn['TE'][:, 0], (1, 1, -1))
    n = np.reshape(mn['TE'][:, 1], (1, 1, -1))

    mode_te_names = ['TE%d%d' % (mn['TE'][i, 0], mn['TE'][i, 1]) for i in range(mn['TE'].shape[0])]
    # mode_tm_names = ['TM%d%d' % (mn['TM'][i, 0], mn['TM'][i, 1]) for i in range(mn['TM'].shape[0])]
    mode_names = mode_te_names  # np.concatenate((mode_te_names, mode_tm_names))

    # kch = np.sqrt(kt_te[:, 0]**2 + kt_te[:, 1]**2)
    kch2 = np.reshape(np.sum(kt_te ** 2, 1), (1, 1, -1))

    Zk = 1j * k0 * Z0 / np.sqrt(kch2 - k0 ** 2, dtype=complex)
    Zk_sq = np.sqrt(Zk)
    Yk_sq = 1. / Zk_sq
    delta_m = 1. + (m == 0).astype(float)
    delta_n = 1. + (n == 0).astype(float)
    # only TE modes (yet at least)
    Nh = 1. / np.abs(kch2 * 0.25 * Lx * Ly * delta_m * delta_n)
    Nh_sq = np.sqrt(Nh)

    Xa, Ya = np.meshgrid(xa, ya)
    Xa = np.reshape(Xa, (Xa.shape[0], Xa.shape[1], 1))
    Ya = np.reshape(Ya, (Ya.shape[0], Ya.shape[1], 1))

    # Aperture transverse electric field modes
    Ek = np.zeros((Xa.shape[0], Xa.shape[1], Nm, 3), dtype=complex)
    Ex = -n * pi / Ly * cos(pi * m * (Xa / Lx + .5)) \
        * sin(pi * n * (Ya / Ly + .5)) * Nh_sq * Zk_sq
    Ey = m * pi / Lx * cos(pi * n * (Ya / Ly + .5)) \
        * sin(pi * m * (Xa / Lx + .5)) * Nh_sq * Zk_sq

    # Aperture transverse magnetic field modes
    Hk = np.zeros((Xa.shape[0], Xa.shape[1], Nm, 3), dtype=complex)
    Hx = -m * pi / Lx * cos(pi * n * (Ya / Ly + .5)) \
        * sin(pi * m * (Xa / Lx + .5)) * Nh_sq * Yk_sq
    Hy = -n * pi / Ly * cos(pi * m * (Xa / Lx + .5)) \
        * sin(pi * n * (Ya / Ly + .5)) * Nh_sq * Yk_sq

    # So far, only TE modes
    Ek[:, :, :, 0] = Ex
    Ek[:, :, :, 1] = Ey
    Hk[:, :, :, 0] = Hx
    Hk[:, :, :, 1] = Hy

    # extends for TM modes not used yet
    """Zk = Zk.reshape((-1,))
    Zk = np.concatenate((Zk.reshape((-1,)), np.ones(Zk.shape)))"""

    return Ek, Hk, Zk, mode_names


def rect_aperture_fields(
        coeffs_: np.array,
        freq: float,
        xa: np.array,
        ya: np.array
):

    Nm = int(.5 * coeffs_.shape[0])
    mode_coeffs = coeffs_[0:Nm]

    Ek, Hk, _, _ = rect_aperture_modes(freq, Nm, xa, ya)

    Pmz = .5 * Ek[:, :, :, 0] * Hk[:, :, :, 1].conj() - Ek[:, :, :, 1] * Hk[:, :, :, 0].conj()
    Pk = integrate.trapezoid(integrate.trapezoid(Pmz, ya, axis=1), xa, axis=0)
    print('TX:', Pk)

    Ek *= mode_coeffs.reshape((1, 1, -1, 1))
    Hk *= mode_coeffs.reshape((1, 1, -1, 1))
    Eat = np.sum(Ek, axis=2)
    Hat = np.sum(Hk, axis=2)

    Eat = Eat.reshape((-1, 3)).view(Field)
    Hat = Hat.reshape((-1, 3)).view(Field)

    return Eat, Hat


def rect_mm(
        freq: float,  # [Hz] frequencies vector
        n_modes,  # Number of modes taken into account
        n_disc,  # Number of discontinuities
        Lx, Ly, dz,  # [m] Dimension of the first section (waveguide)
        tau_x,  # [m] Lx step between each section
        tau_y,  # [m] Ly step between each section
        pbar=None
):
    Mr1 = 1  # iif(tau_x>0, {1, ceil((Lx+tau_x)/Lx)})
    Mr2 = 1  # iif(tau_x>0, {ceil((Lx+tau_x)/Lx), 1})
    """if tau_x > 0:
        Mr2 = int(np.ceil((Lx+tau_x)/Lx))"""

    eps0 = 8.854187817e-12
    mu0 = 4 * pi * 1e-7
    Z0 = sqrt(mu0 / eps0)
    k0 = (2 * pi * freq / 299792458)
    kt1, _ = sort_modes(Mr1 * n_modes, Lx, Ly)

    if pbar is not None:
        pbar.emit(0, n_disc)

    for i in range(n_disc):

        # frequency-independent values computation
        kt2, _ = sort_modes(Mr2 * n_modes, Lx + tau_x, Ly + tau_y)

        X_bar, kt_w, kt_s = compute_x(kt1, kt2, (Lx, Ly), (Lx + tau_x, Ly + tau_y), (tau_x < 0))

        # frequency-dependent values computation
        Kc_wh, K0wh = np.meshgrid(np.sum(kt_w[0] ** 2, 1), k0 ** 2)
        Kc_we, K0we = np.meshgrid(np.sum(kt_w[1] ** 2, 1), k0 ** 2)
        Kc_sh, K0sh = np.meshgrid(np.sum(kt_s[0] ** 2, 1), k0 ** 2)
        Kc_se, K0se = np.meshgrid(np.sum(kt_s[1] ** 2, 1), k0 ** 2)

        # Propagation constants
        gamma_W = np.hstack(
            (sqrt(Kc_wh - K0wh, dtype=complex), sqrt(Kc_we - K0we, dtype=complex)))[0, :]
        gamma_S = np.hstack(
            (sqrt(Kc_sh - K0sh, dtype=complex), sqrt(Kc_se - K0se, dtype=complex)))[0, :]

        # Wave's Impedances - GUIDE S
        Z_sh = 1j * k0 * Z0 / sqrt(Kc_sh - K0sh, dtype=complex)
        Z_se = sqrt(Kc_se - K0sh, dtype=complex) * Z0 / (1j * k0)
        Zs = sqrt(np.hstack((Z_sh, Z_se)), dtype=complex)[0, :]

        # Wave's Admittances - GUIDE W
        Z_wh = 1j * k0 * Z0 / sqrt(Kc_wh - K0wh, dtype=complex)
        Z_we = sqrt(Kc_we - K0wh, dtype=complex) * Z0 / (1j * k0)
        Yw = sqrt(np.hstack((1. / Z_wh, 1. / Z_we)), dtype=complex)[0, :]

        Sww, Sws, Ssw, Sss = gsm_disc(
            Zs,  # Wave's Impedance  - GUIDE S
            Yw,  # Wave's Admittance - GUIDE W
            X_bar  # Normalised inner products
        )

        # Cascade
        if tau_x > 0:
            gamma = gamma_S
        else:
            gamma = gamma_W
        if i == 0:
            # First step: Guide-Discontinuity with no previous GSM
            S11, S12, S21, S22 = cascade_guide_gsm(
                dz,  # waveguide's length
                gamma,  # propagation constants
                tau_x > 0,  # true: S->W, else W->S
                Sww, Sws, Ssw, Sss  # Previous GSM
            )

        if i == (n_disc - 1):
            # Previous GSM - last waveguide's GSM
            if tau_x > 0:
                gamma = gamma_W
            else:
                gamma = gamma_S
            S11, S12, S21, S22 = cascade_gsm_guide(
                dz,  # waveguide's length
                gamma,  # propagation constants
                S11, S12, S21, S22  # Previous GSM
            )
        else:
            # Previous GSM - Discontinuity's GSM
            S11, S12, S21, S22 = cascade_gsm(
                dz,  # waveguide's length
                gamma,  # propagation constants guide S&W,
                tau_x > 0,  # true: S->W, else W->S
                S11, S12, S21, S22,  # Previous GSM to be cascaded
                Sww, Sws, Ssw, Sss,  # W-S discontinuity's GSM
            )

        kt1 = kt2
        Lx += tau_x
        Ly += tau_y

        if pbar is not None:
            pbar.emit((i + 1), 0)

    if tau_x > 0:
        kt_ap = kt_w
    else:
        kt_ap = kt_s

    return S11, S12, S21, S22, kt_ap
