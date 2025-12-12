import numpy as np

from qosm.utils.Pose import Vector
from qosm._core import Triangle as _Triangle
from qosm._core import Vec3 as _Vec3


def is_outward_normal(vertex_normal, vertex_position, centroid):
    # Compute vector from the vertex to the centroid
    vector_to_centroid = centroid - vertex_position
    vector_to_centroid /= np.sqrt(np.sum(vector_to_centroid**2))

    # Compute dot product of the vertex normal and the vector
    dot_product = np.dot(vertex_normal, vector_to_centroid)

    # If dot product is negative, normal is outward (opposite direction)
    return dot_product < 0


class Triangle:
    def __init__(self,
                 vertices,
                 normals,
                 tangents,
                 curvatures,
                 dioptre,
                 obj_centroid=None,
                 id_tri: int = -1,
                 bounces=None):
        if bounces is None:
            bounces = [-1, 1]
        self.dioptre = dioptre
        self.id_tri = id_tri
        self.bounces = bounces
        v0, v1, v2 = vertices

        _edge1, _edge2, _edge3 = (v1 - v0, v2 - v0, v2 - v1)
        n0, n1, n2 = normals
        t0, t1, t2 = tangents

        # print(_edge1.reshape((-1, 3)).norm(), _edge2.reshape((-1, 3)).norm(), _edge3.reshape((-1, 3)).norm())

        n = np.cross(_edge1/np.sqrt(np.sum(_edge1**2)), _edge2/np.sqrt(np.sum(_edge2**2)))
        n /= np.sqrt(np.sum(n**2))
        b = (v0 + v1 + v2) / 3.

        if np.sum(n0**2) == 0 or np.sum(n1**2) == 0 or np.sum(n2**2) == 0:
            raise Exception('Null normal detected (n0, n1, n2): %d %d %d' %
                            (np.sum(n0**2) == 0, np.sum(n1**2) == 0, np.sum(n2**2) == 0))

        # print(id_tri, n0.tolist(), n1.tolist(), n2.tolist())

        if obj_centroid is not None:
            n_outward = is_outward_normal(n, b, obj_centroid)
            if not n_outward:
                v0, v2, v1 = vertices
                n0, n2, n1 = normals
                _edge1, _edge2 = (v1 - v0, v2 - v0)

        # Some vertices can lie on a degenerate or singular point where the normal vector cannot be uniquely defined.
        # This might occur, for example, at sharp edges, corners, or vertices where multiple surfaces meet.
        if np.sqrt(np.sum(n0 ** 2)) < 1e-6:
            tests = Vector([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            test_norm = tests.dot(t0.reshape((-1, 3)))
            tests = tests[test_norm < .5]
            candidates = tests.cross(t0.reshape((-1, 3))).normalised()
            test_dot_n = candidates.dot(n.reshape((-1, 3)))
            idx_candidate = np.abs(test_dot_n).argmax()
            n0 = candidates[idx_candidate, :]
        if np.sqrt(np.sum(n1 ** 2)) < 1e-6:
            tests = Vector([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            test_norm = tests.dot(t1.reshape((-1, 3)))
            tests = tests[test_norm < .5]
            candidates = tests.cross(t1.reshape((-1, 3))).normalised()
            test_dot_n = candidates.dot(n.reshape((-1, 3)))
            idx_candidate = np.abs(test_dot_n).argmax()
            n1 = candidates[idx_candidate, :]
        if np.sqrt(np.sum(n2 ** 2)) < 1e-6:
            tests = Vector([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            test_norm = tests.dot(t2.reshape((-1, 3)))
            tests = tests[test_norm < .5]
            candidates = tests.cross(t2.reshape((-1, 3))).normalised()
            test_dot_n = candidates.dot(n.reshape((-1, 3)))
            idx_candidate = np.abs(test_dot_n).argmax()
            n2 = candidates[idx_candidate, :]

        if np.dot(n0, n) < 0:
            n0 = n0 * -1
        if np.dot(n1, n) < 0:
            n1 = n1 * -1
        if np.dot(n2, n) < 0:
            n2 = n2 * -1

        self.normals = (n0, n1, n2)
        self.curvatures = curvatures
        self.vertices = (v0, v1, v2)

        # store precomputed values
        self.edges = (_edge1, _edge2)

    @property
    def cpp(self):
        v0, v1, v2 = self.vertices
        n0, n1, n2 = self.normals
        c0, c1, c2 = self.curvatures
        e0, e1 = self.edges
        dioptre = self.dioptre
        tri = _Triangle(
            vertices=(
                _Vec3(v0[0], v0[1], v0[2]),
                _Vec3(v1[0], v1[1], v1[2]),
                _Vec3(v2[0], v2[1], v2[2])),
            normals=(
                _Vec3(n0[0], n0[1], n0[2]),
                _Vec3(n1[0], n1[1], n1[2]),
                _Vec3(n2[0], n2[1], n2[2])),
            edges=(_Vec3(e0[0], e0[1], e0[2]),
                   _Vec3(e1[0], e1[1], e1[2])),
            curvatures=(c0, c1, c2),
            dioptre=dioptre,
            id_triangle=self.id_tri
        )
        tri.bounces = self.bounces
        return tri
