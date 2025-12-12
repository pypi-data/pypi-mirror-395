from copy import deepcopy
import numpy as np

from qosm._core import Ray, Medium, Dioptre, Vec3, Frame

class Item:
    def __init__(self, f_obj_ref: Frame):
        self.dioptre = None
        self.frame = f_obj_ref

    def copy(self):
        return deepcopy(self)

    def set_dioptre(self, material1: Medium, material2: Medium) -> None:
        self.dioptre = Dioptre(material1, material2)


class Object(Item):
    def __init__(self, f_obj_glo: Frame):
        super().__init__(f_obj_glo)
        self.surfaces = []

    def copy(self):
        return deepcopy(self)

    def add_surface(self, name: str, stype: int, pos: Vec3, params: dict) -> None:
        if stype == 0:
            surface = Disk(name, pos, params['radius'])
        elif stype == 1:
            surface = Sphere(name, pos, params['radius'], params['zlim'])
        elif stype == 2:
            surface = Cylinder(name, pos, params['radius'], params['h'])
        elif stype == 3:
            surface = Plane(name, pos, params['n'], params['w'], params['h'])
        else:
            return
        self.surfaces.append(surface)

    """def intersect(self, ray_src: BeamRay, intersection: Intersection) -> None:
        # change frame GLO->LOC
        ray_loc = ray_src.change_frame(self.frame)

        for surf in self.surfaces:
            (status, n, t, t0, N) = surf.intersect(ray_loc)
            if status:
                if Intersection.acne < t0 < intersection.t0:
                    intersection.set(
                        dist=t0,
                        normal=self.frame.rot_to_ref(n),
                        tangent=self.frame.rot_to_ref(t),
                        ray=ray_src,
                        curvature=surf.C,
                        dioptre=self.dioptre
                    )
                    ray_src.z_range[1] = t0"""


class Surface:
    def __init__(self,
                 surface_name: str,
                 stype: int,
                 pos: Vec3,
                 curv_matrix=None):
        self.name = surface_name
        self.type = stype
        self.r_surf_obj = pos

        # curvature matrix
        if curv_matrix is not None:
            self.C = curv_matrix
        else:
            # flat surface
            self.C = np.zeros((2, 2))

    def intersect(self, ray: Ray) -> (bool, Vec3, Vec3, float):
        return False, Vec3(), Vec3(), np.inf

    def copy(self):
        return deepcopy(self)


class Disk(Surface):
    def __init__(self, surface_name, pos, disk_radius):
        super().__init__(surface_name, 0, pos)
        self._disk_radius = disk_radius

    def intersect(self, ray: Ray):
        # only non-tilted plane so far

        # normal vector
        # local frame: can use the z-cpnt to check normal
        t = Vec3(1, 0, 0)
        n = Vec3(0, 0, -1)

        # find t0 distance between ray origin and intersection point
        a0 = ray.di * 1e-6
        P = ray.ori + a0
        L = self.r_surf_obj - P
        t0 = (L.dot(n)) / (ray.dir.dot(n)) + 1e-6

        I = ray.ori + ray.dir * t0

        r = (I - self.r_surf_obj).norm()

        status = t0 > 0 and r <= self._disk_radius

        return status, n, t, t0[0], 1


class Plane(Surface):
    def __init__(self, surface_name, pos, n, w, h):
        super().__init__(surface_name, 0, pos)
        self._w = w
        self._h = h
        self._n = n

    def intersect(self, ray: Ray):
        # only non-tilted plane so far
        # normal vector
        # local frame: can use the z-cpnt to check normal
        # n = self._n
        t = Vec3(1, 0, 0)
        n = Vec3(0, 0, -1)

        # find t0 distance between ray origin and intersection point
        a0 = ray.dir * 1e-6
        P = ray.ori + a0
        L = self.r_surf_obj - P
        t0 = (L.dot(n)) / (ray.dir.dot(n)) + 1e-6

        status = t0 > 0

        return status, n, t, t0[0], 1


class Cylinder(Surface):
    def __init__(self, surface_name, pos, cyl_radius, h):
        super().__init__(surface_name, 2, pos, curv_matrix=np.eye(2)/cyl_radius)
        self._hd = h/2
        self._r2 = np.abs(cyl_radius)**2

    def intersect(self, ray: Ray):
        a0 = ray.dir * 1e-6
        P = ray.ori + a0
        p = np.reshape(P[0, 0:2], (2, 1))
        d = np.reshape(ray.dir[0, 0:2], (2, 1))
        a = d[0]**2 + d[1]**2
        b = p[0]*d[0] + p[1]*d[1]
        c = p[0]**2 + p[1]**2 - self._r2
        N = 0
        delta = b**2 - a*c
        status = False
        if delta < 0:
            t0 = np.nan
            n = Vec3()
        else:
            t = np.array([(-b - np.sqrt(delta))/a, (-b + np.sqrt(delta))/a]) + 1e-6
            t[t < 1e-6] = np.nan

            I = P + ray.dir * t
            t[np.abs(I[:, 2]) > self._hd] = np.nan

            if np.isnan(t[0]) and np.isnan(t[1]):
                t0 = np.nan
            else:
                N = np.nansum(t > 0)
                t0 = np.nanmin(t)
                status = True

            I = ray.ori+a0 + ray.dir * t0
            n = Vec3([I[0, 0], I[0, 1], 0])
            n.normalise()

        return status, n, Vec3(), t0, N


class Sphere(Surface):
    def __init__(self, surface_name, pos, sph_radius, zlim):
        super().__init__(surface_name, 1, pos, curv_matrix=np.eye(2)/sph_radius)
        self._zlim = zlim
        self._sph_radius = np.abs(sph_radius)

    def intersect(self, ray: Ray):
        a0 = ray.dir * 1e-6

        # find t0 distance between ray origin and intersection point
        L = ray.ori + a0 - self.r_surf_obj
        r2 = self._sph_radius ** 2
        b = 2 * ray.dir.dot(L)
        c = L.dot(L) - r2
        D = b ** 2 - 4 * c
        N = 0
        if D >= 0:
            sb = np.sign(b)
            if sb == 0:
                sb = 1
            q = -.5 * (b + sb * np.sqrt(D))
            t = np.array([q, c / q]) + 1e-6

            t[t < 1e-6] = np.nan
            pts = ray.ori + ray.dir * t

            t[pts[:, 2] < self._zlim[0]] = np.nan

            if np.isnan(t[0]) and np.isnan(t[1]):
                status = False
                t0 = np.nan
            else:
                N = np.nansum(t > 0)
                t0 = np.nanmin(t)
                status = True

            pts = ray.ori + ray.dir * t0

            # normal vector: always output
            n = (pts - self.r_surf_obj)
            n.normalise()
        else:
            t0 = np.inf
            n = Vec3()
            status = False

        return status, n, Vec3(), t0, N
