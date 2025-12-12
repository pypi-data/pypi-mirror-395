import numpy as np
from numpy import pi


def sort_modes(n_modes: int,
               Lx: float,
               Ly: float) -> (tuple, dict):
    xy_ratio = Lx / Ly

    # TE modes
    M, N = np.meshgrid(
        np.arange(n_modes+1),
        np.arange(n_modes+1),
    )
    k_h_arr = np.concatenate(
        (np.reshape(M**2 + (xy_ratio * N)**2, (-1, 1)),
         np.reshape(M, (-1, 1)),
         np.reshape(N, (-1, 1))), axis=1
    )[1:, ]
    idxs = np.argsort(k_h_arr[:, 0])
    idx_modes_h = k_h_arr[idxs[0:n_modes], 1:3]
    k_h = idx_modes_h * pi / np.array([Lx, Ly])

    # TM modes
    M, N = np.meshgrid(
        np.arange(n_modes+1)+1,
        np.arange(n_modes+1)+1,
    )
    k_e_arr = np.concatenate(
        (np.reshape(M ** 2 + (xy_ratio * N) ** 2, (-1, 1)),
         np.reshape(M, (-1, 1)),
         np.reshape(N, (-1, 1))), axis=1
    )
    idxs = np.argsort(k_e_arr[:, 0])
    idx_modes_e = k_e_arr[idxs[0:n_modes], 1:3]
    k_e = idx_modes_e * pi / np.array([Lx, Ly])

    return (k_h, k_e), {'TE': idx_modes_h, 'TM': idx_modes_h}


def u(L, k):
    sk = np.sum(k)
    skL = np.sum(k * L)
    return 1./sk * np.sin(.5 * L[1]*sk) * np.cos(.5*skL)


def v_cos(L, kv):
    if np.sum(kv) == 0:
        return L[1]
    elif np.prod(kv) == 0:
        return 2.*u(L, kv)
    elif kv[0] == kv[1]:
        return .5 * L[1] * np.cos(.5 * kv[0] * np.diff(L)) + u(L, kv)
    else:
        return u(L, (kv[0], -kv[1])) + u(L, kv)


def v_sin(L, kv):
    if np.prod(kv) == 0:
        return 0.
    elif kv[0] == kv[1]:  # ie cos(-u) = cos(u)
        return .5 * L[1] * np.cos(.5 * L[1] * kv[0] * np.diff(L)) - u(L, kv)
    else:
        return u(L, (kv[0], -kv[1])) - u(L, kv)
    

def compute_x_single(mode, Lx, Ly, kt_w, kt_s, N_wh, N_we, N_sh, N_se):
    m = mode[0]
    n = mode[1] 

    # Usefull for readliness
    # Transverse wave numbers GUIDE W
    k_wxh = kt_w[0][:, 0]
    k_wxe = kt_w[1][:, 0]
    k_wyh = kt_w[0][:, 1]
    k_wye = kt_w[1][:, 1]
    
    # Transverse wave numbers GUIDE S
    k_sxh = kt_s[0][:, 0]
    k_sxe = kt_s[1][:, 0]
    k_syh = kt_s[0][:, 1]
    k_sye = kt_s[1][:, 1]

    # TE-TE
    N_mn = N_sh[m] * N_wh[n]
    alpha = k_wyh[n] * k_syh[m]
    beta = k_wxh[n] * k_sxh[m]

    X_hh_mn = N_mn * (
        alpha * v_cos(Lx, (k_wxh[n], k_sxh[m])) * v_sin(Ly, (k_wyh[n], k_syh[m]))
        +
        beta * v_sin(Lx, (k_wxh[n], k_sxh[m])) * v_cos(Ly, (k_wyh[n], k_syh[m]))
    )

    # TM-TM
    N_mn = N_we[n] * N_se[m]
    alpha = k_wxe[n] * k_sxe[m]
    beta = k_wye[n] * k_sye[m]

    X_ee_mn = N_mn * (
        alpha * v_cos(Lx, (k_wxe[n], k_sxe[m])) * v_sin(Ly, (k_wye[n], k_sye[m]))
        +
        beta * v_sin(Lx, (k_wxe[n], k_sxe[m])) * v_cos(Ly, (k_wye[n], k_sye[m]))
    )

    # TE-TM
    N_mn = N_we[n] * N_sh[m]
    alpha = - k_wxe[n] * k_syh[m]
    beta = k_wye[n] * k_sxh[m]

    X_eh_mn = N_mn * (
        alpha * v_cos(Lx, (k_wxe[n], k_sxh[m])) * v_sin(Ly, (k_wye[n], k_syh[m]))
        +
        beta * v_sin(Lx, (k_wxe[n], k_sxh[m])) * v_cos(Ly, (k_wye[n], k_syh[m]))
    )
    
    return X_hh_mn, X_ee_mn, X_eh_mn
    

def compute_x(
        kt1: tuple,
        kt2: tuple,
        L1: tuple[float, float],
        L2: tuple[float, float],
        is_closing: bool
) -> (np.ndarray, dict):

    if is_closing:
        Ls = L2
        Lw = L1
        kt_s = kt2
        kt_w = kt1
        n_mode_s = kt2[0].shape[0]
        n_mode_w = kt1[0].shape[0]
    else:
        Ls = L1
        Lw = L2
        kt_s = kt1
        kt_w = kt2
        n_mode_s = kt1[0].shape[0]
        n_mode_w = kt2[0].shape[0]

    X_hh = np.zeros((n_mode_s, n_mode_w))
    X_ee = np.zeros((n_mode_s, n_mode_w))
    X_eh = np.zeros((n_mode_s, n_mode_w))
    O = np.zeros((n_mode_s, n_mode_w))

    # Guides' cross section surfaces
    ab_w = np.prod(Lw)
    ab_s = np.prod(Ls)

    # Eigenfunction (T) normalisations GUIDE W
    adw = (np.prod(kt_w[0], 1) == 0).astype(float)
    N_wh = 2. / np.sqrt(np.abs(np.sum(kt_w[0] ** 2, 1) * ab_w * (1 + adw)))
    N_we = 2. / np.sqrt(np.abs(np.sum(kt_w[1] ** 2, 1) * ab_w))

    # Eigenfunction (T) normalisations GUIDE S
    ads = (np.prod(kt_s[0], 1) == 0).astype(float)
    N_sh = 2. / np.sqrt(np.abs(np.sum(kt_s[0] ** 2, 1) * ab_s * (1 + ads)))
    N_se = 2. / np.sqrt(np.abs(np.sum(kt_s[1] ** 2, 1) * ab_s))

    # Usefull for readliness
    # Transverse wave numbers GUIDE W
    k_wxh = kt_w[0][:, 0]
    k_wxe = kt_w[1][:, 0]
    k_wyh = kt_w[0][:, 1]
    k_wye = kt_w[1][:, 1]

    # Transverse wave numbers GUIDE S
    k_sxh = kt_s[0][:, 0]
    k_sxe = kt_s[1][:, 0]
    k_syh = kt_s[0][:, 1]
    k_sye = kt_s[1][:, 1]

    Lx = np.array((Lw[0], Ls[0]))
    Ly = np.array((Lw[1], Ls[1]))

    # Matrix elements computation Xsw
    # Xsw -> Xmn
    
    M, N = np.meshgrid(range(n_mode_s), range(n_mode_w))
    M = M.reshape((-1, 1))
    N = N.reshape((-1, 1))
    modes = np.hstack((M, N))
    
    for row in range(modes.shape[0]):
        m = modes[row, 0]
        n = modes[row, 1] 

        # TE-TE
        N_mn = N_wh[n] + N_sh[m]
        alpha = k_wyh[n] * k_syh[m]
        beta = k_wxh[n] * k_sxh[m]

        X_hh[m, n] = N_mn * (
            alpha * v_cos(Lx, (k_wxh[n], k_sxh[m])) * v_sin(Ly, (k_wyh[n], k_syh[m]))
            +
            beta * v_sin(Lx, (k_wxh[n], k_sxh[m])) * v_cos(Ly, (k_wyh[n], k_syh[m]))
        )

        # TM-TM
        N_mn = N_we[n] * N_se[m]
        alpha = k_wxe[n] * k_sxe[m]
        beta = k_wye[n] * k_sye[m]

        X_ee[m, n] = N_mn * (
            alpha * v_cos(Lx, (k_wxe[n], k_sxe[m])) * v_sin(Ly, (k_wye[n], k_sye[m]))
            +
            beta * v_sin(Lx, (k_wxe[n], k_sxe[m])) * v_cos(Ly, (k_wye[n], k_sye[m]))
        )

        # TE-TM
        N_mn = N_we[n] * N_sh[m]
        alpha = - k_wxe[n] * k_syh[m]
        beta = k_wye[n] * k_sxh[m]

        X_eh[m, n] = N_mn * (
            alpha * v_cos(Lx, (k_wxe[n], k_sxh[m])) * v_sin(Ly, (k_wye[n], k_syh[m]))
            +
            beta * v_sin(Lx, (k_wxe[n], k_sxh[m])) * v_cos(Ly, (k_wye[n], k_syh[m]))
        )

    X = np.vstack((
            np.hstack((X_hh, X_eh)),
            np.hstack((O, X_ee))
    ))

    return X, kt_w, kt_s
