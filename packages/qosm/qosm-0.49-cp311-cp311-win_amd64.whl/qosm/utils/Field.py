# -*- coding: utf-8 -*-

import numpy as np


def lin2db(mag, db_min=-50, do20=False):
    m = 10 * np.log10(mag)
    if do20:
        m *= 2
    m[m < db_min] = db_min
    return m


class Field(np.ndarray):
    eps0 = 8.854187817e-12
    mu0 = 4 * np.pi * 1e-7
    Z0 = 2 * np.sqrt(np.pi * 1e-7 / 8.854187817e-12)

    def __new__(cls, *args, **kwargs):
        N = 1
        data = args
        if 'N' in kwargs:
            N = kwargs['N']
            del kwargs['N']
        elif len(data) == 1 and data[0] is not None:
            N = data[0].shape[0]

        if len(data) == 3:
            obj = np.asarray(data, dtype=np.complex128).view(cls)
            if N > 1:
                obj = np.tile(obj, (N, 1))
        else:
            kwargs['shape'] = (N, 3)
            kwargs['dtype'] = np.complex128
            args = []
            obj = super().__new__(cls, *args, **kwargs)
            obj[:, 0] = 0 + 0j
            obj[:, 1] = 0 + 0j
            obj[:, 2] = 0 + 0j

        return obj

    """def rotate(self, qrot):
        # rotate real part
        E_real = QFrame.rotate(np.real(self), qrot)
        E_imag = QFrame.rotate(np.imag(self), qrot)

        return E_real + E_imag * 1j"""

    def numpy(self):
        return self.view(np.ndarray)

    def norm(self):
        m = np.sqrt(np.real(self.dotc(self)))
        return m.view(np.ndarray)

    def normalise(self, norm_value=None):
        if norm_value is not None:
            self[:] /= norm_value
        elif np.nanmax(self) > 0:
            m = np.sqrt(np.real(self.dotc(self)))
            m[m == 0] = 1e-30
            self[:] /= np.nanmax(m)
            return np.nanmax(np.nanmax(m))
        return None

    def normalised(self, norm_value=None):
        if norm_value is not None:
            return self / norm_value
        elif np.nanmax(self) > 0:
            m = np.sqrt(np.real(self.dotc(self)))
            return self / np.nanmax(m), np.nanmax(m)
        else:
            return self

    def intensity(self, db=False, db_min=-50, normalise=False, norm_value=None, reshape=None):
        # sqrt ** 2 => use norm2 formula
        m = np.real(self.dotc(self))
        if normalise:
            if norm_value is not None:
                m /= norm_value
            elif np.nanmax(m) > 0:
                m /= np.nanmax(m)
        if db:
            m[m == 0] = 1e-70
            m = lin2db(m, db_min)
        if reshape is not None:
            m = np.reshape(m, reshape)

        return m

    def Phase(self, cmp: str, deg = False, unwrap = False, abs = False, reshape=None):
        cmp_idx = {'x': 0, 'y': 1, 'zp': 2}
        p = np.angle(self[:, cmp_idx[cmp]], deg=deg)

        if reshape is not None:
            p = np.reshape(p, reshape)
        if abs:
            p = np.abs(p)
        if unwrap:
            p = np.unwrap(p)
        return p

    def Real(self, cmp: str, normalise=False, norm_value=None, reshape=None):
        cmp_idx = {'x': 0, 'y': 1, 'z': 2}
        m = np.real(self[:, cmp_idx[cmp]])

        if normalise:
            if norm_value is not None:
                m /= norm_value
            elif np.nanmax(m) > 0:
                m /= np.nanmax(m)

        if reshape is not None:
            m = np.reshape(m, reshape)

        return m

    def magnitude(self, db=False, db_min=-50, normalise=False, norm_value=None, reshape=None):
        m = np.sqrt(np.real(self.dotc(self)))

        if normalise:
            if norm_value is not None:
                m /= norm_value
            elif np.nanmax(m) > 0:
                m /= np.nanmax(m)
        if db:
            m[m == 0] = 1e-70
            m = lin2db(m, db_min)
        if reshape is not None:
            m = np.reshape(m, reshape)

        return m

    def phase(self, deg=False, dim=None, reshape=None, unwrap=False):
        if dim is None:
            phase = np.angle(self, deg=deg)
        else:
            phase = np.angle(self[:, dim], deg=deg)
        if reshape is not None:
            phase = np.reshape(phase, reshape)
        if unwrap:
            phase = np.unwrap(phase)
        return phase

    def dot(self, v):
        # v must be real
        return np.sum(self * np.reshape(v, (-1, 3)), axis=1)

    def dotc(self, f):
        return np.sum(self * np.conj(np.reshape(f, (-1, 3))), axis=1)

    def cross(self, v2):
        v3 = Field(N=max(self.shape[0], v2.shape[0]))
        v3[:, 0] = self[:, 1] * v2[:, 2] - self[:, 2] * v2[:, 1]
        v3[:, 1] = self[:, 2] * v2[:, 0] - self[:, 0] * v2[:, 2]
        v3[:, 2] = self[:, 0] * v2[:, 1] - self[:, 1] * v2[:, 0]
        return v3
        # return self.cross(v2)
