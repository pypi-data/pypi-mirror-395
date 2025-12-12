# -*- coding: utf-8 -*-
import numpy as np
from numpy import linspace

from qosm.utils.Field import Field
from qosm._core import Vector as VectorNx3


def rv2base(rv):
    theta = np.reshape(Vector(rv).norm(), (-1,))
    x = Vector(N=theta.shape[0])
    y = Vector(N=theta.shape[0])
    z = Vector(N=theta.shape[0])
    u = Vector(rv).normalised()
    ux = np.reshape(u[:, 0], (-1,))
    uy = np.reshape(u[:, 1], (-1,))
    uz = np.reshape(u[:, 2], (-1,))
    c = np.cos(theta)
    s = np.sin(theta)
    t = 1 - c

    x[:, 0] = c + ux * ux * t
    x[:, 1] = uy * ux * t + uz * s
    x[:, 2] = uz * ux * t - uy * s

    y[:, 0] = ux * uy * t - uz * s
    y[:, 1] = c + uy * uy * t
    y[:, 2] = uz * uy * t + ux * s

    z[:, 0] = ux * uz * t + uy * s
    z[:, 1] = uy * uz * t - ux * s
    z[:, 2] = c + uz * uz * t

    return x, y, z


def q2base(q):
    q0 = q[:, 0]
    q1 = q[:, 1]
    q2 = q[:, 2]
    q3 = q[:, 3]
    x = Vector(
        2 * (q0 * q0 + q1 * q1) - 1,
        2 * (q1 * q2 + q0 * q3),
        2 * (q1 * q3 - q0 * q2)
    )
    y = Vector(
        2 * (q1 * q2 - q0 * q3),
        2 * (q0 * q0 + q2 * q2) - 1,
        2 * (q2 * q3 + q0 * q1)
    )
    z = Vector(
        2 * (q1 * q3 + q0 * q2),
        2 * (q2 * q3 - q0 * q1),
        2 * (q0 * q0 + q3 * q3) - 1
    )
    return x, y, z


class Vector(np.ndarray):
    def __new__(cls, *args, **kwargs):
        N = 1
        c = False
        if 'N' in kwargs:
            N = kwargs['N']
            del kwargs['N']
        if 'copy' in kwargs:
            c = kwargs['copy']
            del kwargs['copy']

        kwargs['dtype'] = np.float64

        if len(args) == 1:
            obj = np.reshape(args[0], (-1, 3)).view(cls)
            return obj
        elif len(args) == 3:
            obj = np.reshape(np.asarray(args, dtype=np.float64).view(cls), (-1, 3))
        else:
            obj = np.asarray([[0, 0, 0]], dtype=np.float64).view(cls)

        if N > 1 or c:
            obj = np.tile(obj, (N, 1))

        return obj

    def norm(self):
        return np.sqrt(self[:, 0] ** 2
                       + self[:, 1] ** 2
                       + self[:, 2] ** 2).view(np.ndarray)

    def norm2(self):
        return (self[:, 0] ** 2
                + self[:, 1] ** 2
                + self[:, 2] ** 2).view(np.ndarray)

    def normalise(self):
        n = np.sqrt(self[:, 0] ** 2
                    + self[:, 1] ** 2
                    + self[:, 2] ** 2)
        self[n > 0, 0] = self[n > 0, 0] / n[n > 0]
        self[n > 0, 1] = self[n > 0, 1] / n[n > 0]
        self[n > 0, 2] = self[n > 0, 2] / n[n > 0]

    def normalised(self):
        v = Vector(self.tolist())
        v.normalise()
        return v

    def dot(self, v):
        return (self[:, 0] * v[:, 0]
                + self[:, 1] * v[:, 1]
                + self[:, 2] * v[:, 2]).view(np.ndarray)

    def cross(self, v2):
        v1 = np.reshape(self, (-1, 3))
        v2 = np.reshape(v2, (-1, 3))
        v3 = Vector(N=self.shape[0])
        v3[:, 0] = v1[:, 1] * v2[:, 2] - v1[:, 2] * v2[:, 1]
        v3[:, 1] = v1[:, 2] * v2[:, 0] - v1[:, 0] * v2[:, 2]
        v3[:, 2] = v1[:, 0] * v2[:, 1] - v1[:, 1] * v2[:, 0]
        return v3

    def flip(self):
        return self * (-1)

    def __str__(self):
        if len(self.shape) == 1 or self.shape[0] == 1:
            return 'Vector: %s' % super().__str__()
        else:
            return 'Vector: \n%s' % super().__str__()

    @staticmethod
    def scale(v, k):
        return Vector(v * k)


class Quaternion(np.ndarray):
    def __new__(cls, *args, **kwargs):
        cls.valid = True
        data = args

        kwargs['dtype'] = np.double

        N = 1
        c = False
        if 'N' in kwargs:
            N = kwargs['N']
            del kwargs['N']
        if 'copy' in kwargs:
            c = kwargs['copy']
            del kwargs['copy']

        if len(data) == 1:
            if data[0] is None:
                obj = np.asarray([[1., 0., 0., 0.]], dtype=np.double).view(cls)
                obj.valid = False
            else:
                # CREATE QUATERNION FROM ARGS[0] = (w, q1, q2, q3)
                obj = np.reshape(np.asarray(data[0], dtype=np.double).view(cls), (-1, 4))

        elif len(data) == 2:
            # CREATE QUATERNION FROM ARGS = (v, w)
            q = np.hstack((np.array([data[1]]).reshape((-1, 1)), data[0]))
            obj = np.reshape(np.asarray(q, dtype=np.double).view(cls), (-1, 4))
        elif len(data) == 4:
            # CREATE QUATERNION FROM ARGS = (w, q1, q2, q3)
            obj = np.reshape(np.asarray(data, dtype=np.double).view(cls), (-1, 4))

        elif 'rotvec' in kwargs:
            rv = Vector(kwargs['rotvec'])
            angle = np.reshape(rv.norm(), (-1, 1))
            axis = Vector(kwargs['rotvec']).normalised()
            del kwargs['rotvec']

            kwargs['shape'] = (axis.shape[0], 4)
            obj = super().__new__(cls, *args, **kwargs)
            obj[:, 0] = np.reshape(np.cos(angle), (-1,))
            obj[:, 1:] = np.sin(angle) * axis

        elif 'axis' in kwargs and 'angle' in kwargs:
            # FROM AXIS ANGLE
            conv = 0.5
            if 'deg' in kwargs and kwargs['deg']:
                conv *= np.pi / 180.
            if 'deg' in kwargs:
                del kwargs['deg']

            angle = conv * np.reshape(kwargs['angle'], (-1, 1))
            axis = np.reshape(kwargs['axis'], (-1, 3))

            if angle.shape[0] != 1 and angle.shape[0] != axis.shape[0]:
                raise Exception(
                    '%d element(s) for angle, while %d element(s) for axis' % (angle.shape[0], axis.shape[0])
                )
            del kwargs['axis']
            del kwargs['angle']

            kwargs['shape'] = (axis.shape[0], 4)
            obj = super().__new__(cls, *args, **kwargs)
            obj[:, 0] = np.cos(angle)
            obj[:, 1:] = np.sin(angle) * axis

        elif 'vector' in kwargs:
            # CREATE PURE QUATERNION FROM VECTOR
            v = np.reshape(kwargs['vector'], (-1, 3))
            del kwargs['vector']
            kwargs['shape'] = (v.shape[0], 4)
            obj = super().__new__(cls, *args, **kwargs)
            obj[:, 0] = 0
            obj[:, 1:] = v
        else:
            obj = np.asarray([[1., 0., 0., 0.]], dtype=np.double).view(cls)

        if N > 1 or c:
            obj = np.tile(obj, (N, 1))

        return obj

    def norm(self):
        return np.sqrt(np.sum(self ** 2, axis=1))

    def normalise(self):
        n = np.sqrt(np.sum(self ** 2, axis=1))
        self[:] /= n

    def q2v(self):
        return self[:, 1:].view(Vector)

    def conj(self):
        return self * [[1, -1, -1, -1]]

    def to_rotvec(self) -> Vector:
        angle = np.arccos(self[:, 0])
        if angle != 0:
            axis = self[:, 1:3] / np.sin(angle)
        else:
            axis = self[:, 1:3]
        return Vector(angle * axis)

    def __str__(self):
        if len(self.shape) == 1 or self.shape[0] == 1:
            return 'Quaternion: %s' % super().__str__()
        else:
            return 'Quaternion: \n%s' % super().__str__()

    def rotate(self, v: Vector):
        """ Passive quaternion rotation.
        - Input: Vector to be rotated
        - Return the rotated Vector

        Active rotation is when the point is rotated with respect to the coordinate system,
        and passive rotation is when the coordinate system is rotated with respect to the point.
        The two rotations are opposite to each other.
        """
        v_ = np.reshape(v, (-1, 3))
        qv = Quaternion(N=v_.shape[0])
        qv[:, 1:] = v_
        q = self.qprod(qv.qprod(self.conj()))
        return q[:, 1:].view(Vector)

    def qprod(self, qC):
        qA = np.reshape(self, (-1, 4))
        qC = np.reshape(qC, (-1, 4))
        N = max(qA.shape[0], qC.shape[0])
        q = Quaternion(N=N)

        q[:, 0] = qA[:, 0] * qC[:, 0] - (qA[:, 1] * qC[:, 1] + qA[:, 2] * qC[:, 2] + qA[:, 3] * qC[:, 3])

        a = np.reshape(qA[:, 0], (-1, 1)) * qC[:, 1:] + + np.reshape(qC[:, 0], (-1, 1)) * qA[:, 1:]
        q[:, 1] = a[:, 0] + qA[:, 2] * qC[:, 3] - qA[:, 3] * qC[:, 2]
        q[:, 2] = a[:, 1] + qA[:, 3] * qC[:, 1] - qA[:, 1] * qC[:, 3]
        q[:, 3] = a[:, 2] + qA[:, 1] * qC[:, 2] - qA[:, 2] * qC[:, 1]
        return q

    @staticmethod
    def v2q(v):
        return Quaternion(v, 0)


class Pose(np.ndarray):
    pass


class Frame:
    def __init__(self, *args, **kwargs):
        self.q = None
        self.rv = None
        self.ori = None
        if len(args) == 2 and isinstance(args[0], np.ndarray):
            self.R = args[0]
            self.ori = Vector(args[1])
        else:
            if 'base' in kwargs and len(kwargs['base']) == 3:
                x = np.array(kwargs['base'][0])
                y = np.array(kwargs['base'][1])
                z = np.array(kwargs['base'][2])
            elif 'matrix' in kwargs:
                x = np.array(kwargs['matrix'][:, 0:3])
                y = np.array(kwargs['matrix'][:, 3:6])
                z = np.array(kwargs['matrix'][:, 6:9])
            elif 'pose' in kwargs:
                pose = np.array(kwargs['pose'])
                self.ori = Vector(pose[:, 0:3])
                if pose.shape[1] == 6:
                    self.rv = Vector(pose[:, 3:])
                    self.q = Quaternion(rotvec=pose[:, 3:])
                    x, y, z = rv2base(self.rv)
                elif pose.shape[1] == 7:
                    self.q = Quaternion(pose[:, 3:])
                    x, y, z = q2base(self.q)
                else:
                    raise Exception('Invalid pose vector')
            elif 'quaternion' in kwargs:
                q = kwargs['quaternion']
                if type(q).__name__ != 'Quaternion':
                    q = Quaternion(q)
                x, y, z = q2base(q)
                self.q = q
            else:
                x = Vector(1, 0, 0)
                y = Vector(0, 1, 0)
                z = Vector(0, 0, 1)

            self.R = np.zeros((x.shape[0], 9), dtype=np.double)
            self.R[:, 0:3] = x
            self.R[:, 3:6] = y
            self.R[:, 6:9] = z

            if 'ori' in kwargs:
                self.ori = Vector(kwargs['ori'])
                if self.ori.shape[0] == 1:
                    self.ori = np.tile(self.ori, (self.R.shape[0], 1))
            elif self.ori is None:
                self.ori = Vector(N=self.R.shape[0])

        self.x = self.R[:, 0:3].view(Vector)
        self.y = self.R[:, 3:6].view(Vector)
        self.z = self.R[:, 6:9].view(Vector)

    @property
    def pose(self) -> np.ndarray:
        """ return the frame pose as a transformation matrix Nx4x4"""
        M = np.zeros((self.R.shape[0], 4, 4))
        M[:, 0:3, 0:3] = np.reshape(self.R, (-1, 3, 3))
        M[:, 0:3, 3] = self.ori
        M[:, 3, 3] = 1
        return M

    def get_pose(self) -> np.ndarray:
        """ return the frame pose as a transformation matrix Nx4x4"""
        M = np.zeros((self.R.shape[0], 4, 4))
        M[:, 0:3, 0:3] = np.reshape(self.R, (-1, 3, 3))
        M[:, 0:3, 3] = self.ori
        M[:, 3, 3] = 1
        return M

    def to_local(self, v: Vector):
        v_ = np.reshape(v, (-1, 3)) - self.ori
        N = max(self.R.shape[0], v_.shape[0])
        r = Vector(N=N)
        r[:, 0] = v_[:, 0] * self.R[:, 0] + v_[:, 1] * self.R[:, 1] + v_[:, 2] * self.R[:, 2]
        r[:, 1] = v_[:, 0] * self.R[:, 3] + v_[:, 1] * self.R[:, 4] + v_[:, 2] * self.R[:, 5]
        r[:, 2] = v_[:, 0] * self.R[:, 6] + v_[:, 1] * self.R[:, 7] + v_[:, 2] * self.R[:, 8]
        return r

    def to_ref(self, v: Vector):
        v_ = np.reshape(v, (-1, 3))
        N = max(self.R.shape[0], v_.shape[0])
        r = Vector(N=N)
        r[:, 0] = v_[:, 0] * self.R[:, 0] + v_[:, 1] * self.R[:, 3] + v_[:, 2] * self.R[:, 6]
        r[:, 1] = v_[:, 0] * self.R[:, 1] + v_[:, 1] * self.R[:, 4] + v_[:, 2] * self.R[:, 7]
        r[:, 2] = v_[:, 0] * self.R[:, 2] + v_[:, 1] * self.R[:, 5] + v_[:, 2] * self.R[:, 8]
        return r + self.ori

    def rot_to_local(self, f):
        f_ = np.reshape(f, (-1, 3))
        N = max(self.R.shape[0], f_.shape[0])
        # real part
        fre = np.real(f_)
        rre = Vector(N=N)
        rre[:, 0] = fre[:, 0] * self.R[:, 0] + fre[:, 1] * self.R[:, 1] + fre[:, 2] * self.R[:, 2]
        rre[:, 1] = fre[:, 0] * self.R[:, 3] + fre[:, 1] * self.R[:, 4] + fre[:, 2] * self.R[:, 5]
        rre[:, 2] = fre[:, 0] * self.R[:, 6] + fre[:, 1] * self.R[:, 7] + fre[:, 2] * self.R[:, 8]
        if type(f).__name__ != 'Field':
            return rre
        # imaginary part
        fim = np.imag(f_)
        rim = Field(N=N)
        rim[:, 0] = fim[:, 0] * self.R[:, 0] + fim[:, 1] * self.R[:, 1] + fim[:, 2] * self.R[:, 2]
        rim[:, 1] = fim[:, 0] * self.R[:, 3] + fim[:, 1] * self.R[:, 4] + fim[:, 2] * self.R[:, 5]
        rim[:, 2] = fim[:, 0] * self.R[:, 6] + fim[:, 1] * self.R[:, 7] + fim[:, 2] * self.R[:, 8]
        return rre.view(Field) + rim * 1j

    def rot_to_ref(self, f):
        N = max(self.R.shape[0], f.shape[0])
        f_ = np.reshape(f, (-1, 3))
        # real part
        fre = np.real(f_)
        rre = Vector(N=N)
        rre[:, 0] = fre[:, 0] * self.R[:, 0] + fre[:, 1] * self.R[:, 3] + fre[:, 2] * self.R[:, 6]
        rre[:, 1] = fre[:, 0] * self.R[:, 1] + fre[:, 1] * self.R[:, 4] + fre[:, 2] * self.R[:, 7]
        rre[:, 2] = fre[:, 0] * self.R[:, 2] + fre[:, 1] * self.R[:, 5] + fre[:, 2] * self.R[:, 8]
        if type(f).__name__ != 'Field':
            return rre
        # imaginary part
        fim = np.imag(f_)
        rim = Field(N=N)
        rim[:, 0] = fim[:, 0] * self.R[:, 0] + fim[:, 1] * self.R[:, 3] + fim[:, 2] * self.R[:, 6]
        rim[:, 1] = fim[:, 0] * self.R[:, 1] + fim[:, 1] * self.R[:, 4] + fim[:, 2] * self.R[:, 7]
        rim[:, 2] = fim[:, 0] * self.R[:, 2] + fim[:, 1] * self.R[:, 5] + fim[:, 2] * self.R[:, 8]
        return rre.view(Field) + rim * 1j

    def disp(self, n):
        print(np.reshape(self.R[n, 0:9], (3, 3)), np.reshape(self.R[:, 9:], (1, 3)))

    def __getitem__(self, key):
        T = np.reshape(self.R[key], (-1, 9))
        ori = np.reshape(self.ori[key], (-1, 3))
        return Frame(T, ori)

    def __str__(self):
        return 'Frame:\n    ori: %s\n    x: %s\n    y: %s\n    z: %s' % (
            self.ori, self.x, self.y, self.z
        )


def frame_change_q(
        pose_ref_a: tuple[Vector, Quaternion],
        pose_ref_b: tuple[Vector, Quaternion]
) -> tuple[Vector, Quaternion]:
    ref_r_ref_a, q_ref_a = pose_ref_a
    ref_r_ref_b, q_ref_b = pose_ref_b

    q_a_ref = q_ref_a.conj()
    q_a_b = Quaternion.qprod(q_a_ref, q_ref_b)

    ref_r_a_b = ref_r_ref_b - ref_r_ref_a
    a_r_a_b = q_a_b.rotate(ref_r_a_b)

    pose_a_b = (a_r_a_b, q_a_b)
    return pose_a_b


def frame_change(
        frame_ref_a: Frame,
        frame_ref_b: Frame
) -> Frame:
    ref_r_ref_a = frame_ref_a.ori
    ref_r_ref_b = frame_ref_b.ori

    R_ref_a = frame_ref_a.R.reshape((3, 3))
    R_ref_b = frame_ref_b.R.reshape((3, 3))
    R_b_ref = np.transpose(R_ref_b)
    R_b_a = (R_b_ref @ R_ref_a).reshape((1, -1))

    ref_r_b_a = ref_r_ref_a - ref_r_ref_b
    b_r_b_a = R_b_a @ ref_r_b_a

    return Frame(R_b_a, b_r_b_a)


class MeshGrid:
    def __init__(self, u: np.ndarray, v: np.ndarray):
        self.nu = u.shape[0]
        self.nv = v.shape[0]
        self.axis = (u, v)
        if u.shape[0] > 1:
            step_u = u[1] - u[0]
        else:
            step_u = 0
        if v.shape[0] > 1:
            step_v = v[1] - v[0]
        else:
            step_v = 0
        self.step = (step_u, step_v)
        self.U, self.V = np.meshgrid(u, v)

    @staticmethod
    def create_grid(dim_u: [float, float], dim_v: [float, float],
                    offset: [float, float] = (0, 0)):
        ru = dim_u[0] / 2
        rv = dim_v[0] / 2
        num_u = 1 + int(2 * ru / dim_u[1])
        num_v = 1 + int(2 * rv / dim_v[1])
        u = np.linspace(-ru, ru, num_u, endpoint=True) + offset[0]
        v = np.linspace(-rv, rv, num_v, endpoint=True) + offset[1]
        return MeshGrid(u=u, v=v)

    @staticmethod
    def draw_box(points, ax, scale=1.0):
        x1 = np.min(points[:, 0]) * scale
        x2 = np.max(points[:, 0]) * scale
        y1 = np.min(points[:, 1]) * scale
        y2 = np.max(points[:, 1]) * scale
        z1 = np.min(points[:, 2]) * scale
        z2 = np.max(points[:, 2]) * scale

        col = 'b'

        ax.plot([y1, y1], [z1, z1], [x1, x2], linewidth=1.0)  # | (up)
        ax.plot([y1, y2], [z1, z1], [x2, x2], linewidth=1.0)  # -->
        ax.plot([y2, y2], [z1, z1], [x2, x1], linewidth=1.0)  # | (down)
        ax.plot([y2, y1], [z1, z1], [x1, x1], linewidth=1.0)  # <--

        ax.plot([y1, y1], [z2, z2], [x1, x2], linewidth=1.0)  # | (up)
        ax.plot([y1, y2], [z2, z2], [x2, x2], linewidth=1.0)  # -->
        ax.plot([y2, y2], [z2, z2], [x2, x1], linewidth=1.0)  # | (down)
        ax.plot([y2, y1], [z2, z2], [x1, x1], linewidth=1.0)  # <--

        ax.plot([y1, y1], [z1, z2], [x1, x1], linewidth=1.0)  # | (up)
        ax.plot([y2, y2], [z1, z2], [x2, x2], linewidth=1.0)  # -->
        ax.plot([y2, y2], [z1, z2], [x1, x1], linewidth=1.0)  # | (down)
        ax.plot([y1, y1], [z1, z2], [x2, x2], linewidth=1.0)  # <--

    def ax(self, idx: int, scale: float = 1.) -> np.ndarray:
        return self.axis[idx] * scale

    def size(self) -> None:
        return self.nu * self.nv

    def flatten_u(self) -> None:
        return self.U.reshape(-1, )

    def flatten_v(self) -> None:
        return self.V.reshape(-1, )

    def xy_plane(self, z: float = 0) -> Vector:
        r_pts = Vector(N=self.nu * self.nv)
        r_pts[:, 0] = self.U.reshape(-1, )
        r_pts[:, 1] = self.V.reshape(-1, )
        r_pts[:, 2] = z
        return r_pts

    def yz_plane(self, x: float = 0) -> Vector:
        r_pts = Vector(N=self.nu * self.nv)
        r_pts[:, 0] = x
        r_pts[:, 1] = self.U.reshape(-1, )
        r_pts[:, 2] = self.V.reshape(-1, )
        return r_pts

    def xz_plane(self, y: float = 0) -> Vector:
        r_pts = Vector(N=self.nu * self.nv)
        r_pts[:, 0] = self.U.reshape(-1, )
        r_pts[:, 1] = y
        r_pts[:, 2] = self.V.reshape(-1, )
        return r_pts

    def yx_plane(self, z: float = 0) -> Vector:
        r_pts = Vector(N=self.nu * self.nv)
        r_pts[:, 0] = self.V.reshape(-1, )
        r_pts[:, 1] = self.U.reshape(-1, )
        r_pts[:, 2] = z
        return r_pts

    def zy_plane(self, x: float = 0) -> Vector:
        r_pts = Vector(N=self.nu * self.nv)
        r_pts[:, 0] = x
        r_pts[:, 1] = self.V.reshape(-1, )
        r_pts[:, 2] = self.U.reshape(-1, )
        return r_pts

    def zx_plane(self, y: float = 0) -> Vector:
        r_pts = Vector(N=self.nu * self.nv)
        r_pts[:, 0] = self.V.reshape(-1, )
        r_pts[:, 1] = y
        r_pts[:, 2] = self.U.reshape(-1, )
        return r_pts


def create_meshgrid(u_min_mm: float = -40.,
                    u_max_mm: float = 40.,
                    u_step_mm: float = 1.,
                    u_offset_mm: float = 0.,
                    v_min_mm: float = -40.,
                    v_max_mm: float = 40.,
                    v_step_mm: float = 1.,
                    v_offset_mm: float = 0.,
                    n_mm: float = 0.,
                    plane: str = 'xy'
                    ) -> (VectorNx3, MeshGrid):
    ru = (u_max_mm - u_min_mm) / 2
    rv = (v_max_mm - v_min_mm) / 2
    num_u = 1 + int(2 * ru / u_step_mm)
    num_v = 1 + int(2 * rv / v_step_mm)
    u = linspace(u_min_mm, u_max_mm, num_u, endpoint=True) + u_offset_mm
    v = linspace(v_min_mm, v_max_mm, num_v, endpoint=True) + v_offset_mm

    grid = MeshGrid(u=u, v=v)

    r_pts = Vector()
    plane = plane.lower()
    if plane == 'xy':
        r_pts = grid.xy_plane(z=n_mm)
    elif plane == 'xz':
        r_pts = grid.xz_plane(y=n_mm)
    elif plane == 'yz':
        r_pts = grid.yz_plane(x=n_mm)
    elif plane == 'yx':
        r_pts = grid.yx_plane(z=n_mm)
    elif plane == 'zx':
        r_pts = grid.zx_plane(y=n_mm)
    elif plane == 'zy':
        r_pts = grid.zy_plane(x=n_mm)
    else:
        raise Exception('Invalid plane requested for GBE: %s' % plane)

    return VectorNx3(r_pts * 1e-3), grid


def create_meshgrid_linspace(u_min_mm: float = -40.,
                             u_max_mm: float = 40.,
                             num_u: int = 41,
                             u_offset_mm: float = 0.,
                             v_min_mm: float = -40.,
                             v_max_mm: float = 40.,
                             num_v: int = 41,
                             v_offset_mm: float = 0.,
                             n_mm: float = 0.,
                             plane: str = 'xy'
                             ) -> (VectorNx3, MeshGrid):
    u = linspace(u_min_mm, u_max_mm, num_u, endpoint=True) + u_offset_mm
    v = linspace(v_min_mm, v_max_mm, num_v, endpoint=True) + v_offset_mm

    grid = MeshGrid(u=u, v=v)

    r_pts = Vector()
    plane = plane.lower()
    if plane == 'xy':
        r_pts = grid.xy_plane(z=n_mm)
    elif plane == 'xz':
        r_pts = grid.xz_plane(y=n_mm)
    elif plane == 'yz':
        r_pts = grid.yz_plane(x=n_mm)
    elif plane == 'yx':
        r_pts = grid.yx_plane(z=n_mm)
    elif plane == 'zx':
        r_pts = grid.zx_plane(y=n_mm)
    elif plane == 'zy':
        r_pts = grid.zy_plane(x=n_mm)
    else:
        raise Exception('Invalid plane requested for GBE: %s' % plane)

    return VectorNx3(r_pts * 1e-3), grid
