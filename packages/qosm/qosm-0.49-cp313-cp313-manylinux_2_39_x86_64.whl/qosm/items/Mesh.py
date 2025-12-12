import gmsh

from qosm.items.Triangle import Triangle as pyTriangle
from qosm.items.Object import Sphere, Item
from qosm._core import Frame, Vector, Vec3, Triangle

import numpy as np
from matplotlib import cm, colors
from matplotlib.cm import ScalarMappable
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

gmsh.initialize()
gmsh.option.setNumber('General.Terminal', 0)


class Mesh(Item):
    def __init__(self, f_obj_ref: Frame):
        super(Mesh, self).__init__(f_obj_ref)
        self.bounces = [-1, -1]
        self.vertices = np.zeros((0, 3), dtype=float)
        self.triangles = np.zeros((0, 3), dtype=int)
        self.normals = np.zeros((0, 3), dtype=float)
        self.curvatures = np.zeros((0,), dtype=float)
        self.tri_vertices = np.zeros((0, 3), dtype=float)
        self.tri_normals = np.zeros((0, 3), dtype=float)
        self.tri_tangents = np.zeros((0, 3), dtype=float)
        self.tri_bitangents = np.zeros((0, 3), dtype=float)
        self.tri_curvatures = np.zeros((0, 3), dtype=float)

        # Obj format storage
        self._obj_txt = ''

        # map surface-faces
        self._sf_map = []
        # map faces-surface
        self._fs_map = np.zeros((0,), dtype=int)

        # map surface-vertices
        self._sv_map = []
        # map vertices-surface
        self._vs_map = np.zeros((0,), dtype=int)

        self.faces = []
        self.surf_names = []
        self.id = 0

        self.bounding = None

    def pre_build(self, scale=1e-3, create_obj=None, progress=None, view=False, show_vectors=True,
                  offset: Vec3 = Vec3(), centre_shape=False, use_parametric=True):

        tangents = np.zeros((0, 3), dtype=float)
        bitangents = np.zeros((0, 3), dtype=float)

        dims = np.array(gmsh.model.getBoundingBox(-1, -1))
        r = np.max(dims[3:]) - np.min(dims[0:3])
        self.bounding = Sphere('bounding_sphere', Vec3(), r, [-np.inf, np.inf])

        # Get each surface from the model
        surfaces = gmsh.model.getEntities(2)
        surf_tags = [s[1] for s in surfaces]
        self.surf_names = [gmsh.model.getType(2, s[1]) for s in surfaces]
        self._sf_map = [[] for _ in surfaces]
        self._sv_map = [[] for _ in surfaces]

        nv = 0
        self._obj_txt = ''
        i = 0
        nn = []
        for e in surfaces:
            surf = e[1]

            if progress is not None:
                progress.emit(int(100 * i / len(surf_tags)))

            # Get triangles tags and nodes tags
            _, tri_node_tags = gmsh.model.mesh.getElementsByType(2, surf)


            # get nodes on surface
            node_tags, node_coord_, param = gmsh.model.mesh.getNodes(2, surf, True)
            node_coord = np.reshape(node_coord_, (-1, 3))
            if len(node_coord) == 0:
                continue

            # Get tangent vectors
            if use_parametric:
                der = np.reshape(gmsh.model.getDerivative(2, surf, param), (-1, 6))
                # Set tangent and bitangents for each vectex
                # + get surface normal on all vertices
                t = Vector(der[:, 0:3].tolist()).normalised()
                b = Vector(der[:, 3:].tolist()).normalised()

                # get surface curvature
                surf_curvatures = np.reshape(gmsh.model.getCurvature(2, surf, param), (-1,))
                surf_normals = t.cross(b)

                tangents = np.vstack((tangents, t.numpy()))
                bitangents = np.vstack((bitangents, b.numpy()))
                self.curvatures = np.concatenate((self.curvatures, surf_curvatures))

            surf_normals = gmsh.model.getNormal(surf, param).reshape((-1, 3))

            surface_normal = np.mean(surf_normals, axis=0).flatten()
            surface_normal = Vec3(surface_normal[0], surface_normal[1], surface_normal[2]).normalised()

            for i in range(0, node_coord.shape[0], 1):
                n = Vec3(surf_normals[i, 0], surf_normals[i, 1], surf_normals[i, 2])
                if n.norm() == 0:
                    dim_dot = (surface_normal.dot(Vec3(1., 0., 0.)),
                               surface_normal.dot(Vec3(0., 1., 0.)),
                               surface_normal.dot(Vec3(0., 0., 1.)))
                    dim = np.argmax(np.abs(dim_dot))
                    sens = (np.array(dim_dot) > 0) * 2. - 1.
                    surf_normals[i, :] *= 0.
                    surf_normals[i, dim] = sens[dim]
                    # print('Null normal => ', surf_normals[i, :])

                nn.append(node_coord[i, 0])
                nn.append(node_coord[i, 1])
                nn.append(node_coord[i, 2])
                nn.append(surf_normals[i, 0])
                nn.append(surf_normals[i, 1])
                nn.append(surf_normals[i, 2])

            vmap = dict({j: i + nv for i, j in enumerate(node_tags)})
            vidx = [i for _, _ in enumerate(node_tags)]
            node_idx = np.array([vmap[j] for j in tri_node_tags])
            triangles_nodes_idx = node_idx.reshape((-1, 3))
            self._vs_map = np.concatenate((self._vs_map, vidx))
            self.vertices = np.concatenate((self.vertices, node_coord))
            self.normals = np.vstack((self.normals, surf_normals))
            self.triangles = np.concatenate((self.triangles, triangles_nodes_idx))

            if create_obj:
                self._obj_txt += 'o surf_%d\n' % surf
                for v in node_coord:
                    self._obj_txt += 'v %f %f %f\n' % (v[0], v[1], v[2])
                for n in surf_normals:
                    self._obj_txt += 'vn %f %f %f\n' % (n[0], n[1], n[2])
                for f in triangles_nodes_idx:
                    self._obj_txt += 'f %d//%d %d//%d %d//%d\n' % (
                        f[0] + 1, f[0] + 1, f[1] + 1, f[1] + 1, f[2] + 1, f[2] + 1)

            self._fs_map = np.concatenate(
                (self._fs_map, np.ones((triangles_nodes_idx.shape[0],), dtype=int) * (surf - 1)))
            i += 1
            nv += node_coord.shape[0]

        if centre_shape:
            barycentre = np.mean(self.vertices, axis=0)
            self.vertices -= barycentre

        self.vertices += [offset[0], offset[1], offset[2]]
        self.vertices *= scale
        self.curvatures /= scale
        self.tri_vertices = self.vertices[self.triangles]
        self.tri_normals = self.normals[self.triangles]

        if use_parametric:
            self.tri_curvatures = self.curvatures[self.triangles]
            self.tri_tangents = tangents[self.triangles]
            self.tri_bitangents = bitangents[self.triangles]

        if show_vectors:
            n = gmsh.view.add("normals")
            gmsh.view.addListData(n, "VP", len(nn) // 6, nn)
            gmsh.view.write(n, "normals.pos")

        if view:
            gmsh.fltk.run()
        gmsh.clear()

    @property
    def geometry(self, fix_with_centroid: bool = False) -> list[Triangle]:
        tri_vertices = self.frame.to_ref(self.tri_vertices.reshape((-1, 3))).reshape((-1, 3, 3))
        tri_normals = self.frame.rot_to_ref(self.tri_normals.reshape((-1, 3))).reshape((-1, 3, 3))
        tri_tangents = self.frame.rot_to_ref(self.tri_tangents.reshape((-1, 3))).reshape((-1, 3, 3))
        indexes = np.arange(0, tri_vertices.shape[0])
        return [pyTriangle(v, n, t, c, self.dioptre, None, i, self.bounces).cpp
                for v, n, t, c, i in zip(tri_vertices, tri_normals, tri_tangents, self.tri_curvatures, indexes)]

    @property
    def geometry_fix(self) -> list[Triangle]:
        tri_vertices = self.frame.to_ref(self.tri_vertices.reshape((-1, 3))).reshape((-1, 3, 3))
        tri_normals = self.frame.rot_to_ref(self.tri_normals.reshape((-1, 3))).reshape((-1, 3, 3))
        tri_tangents = self.frame.rot_to_ref(self.tri_tangents.reshape((-1, 3))).reshape((-1, 3, 3))
        indexes = np.arange(0, tri_vertices.shape[0])

        obj_centroid = np.mean(self.frame.to_ref(self.vertices), axis=0)
        return [pyTriangle(v, n, t, c, self.dioptre, obj_centroid, i, self.bounces).cpp
                for v, n, t, c, i in zip(tri_vertices, tri_normals, tri_tangents, self.tri_curvatures, indexes)]

    def dump(self, filename: str):
        N = self.tri_vertices.shape[0]
        data = np.zeros((N, 27))
        i = 0
        for v, n, t, c in zip(self.tri_vertices, self.tri_normals, self.tri_tangents, self.tri_curvatures):
            tri = pyTriangle(v, n, t, c, self.dioptre, None)
            v0, v1, v2 = tri.vertices
            n0, n1, n2 = tri.normals
            c0, c1, c2 = tri.curvatures
            e0, e1 = tri.edges
            data[i, :] = np.hstack((v0.reshape((-1,)), v1.reshape((-1,)), v2.reshape((-1,)),
                                    n0.reshape((-1,)), n1.reshape((-1,)), n2.reshape((-1,)),
                                    c0, c1, c2,
                                    e0.reshape((-1,)), e1.reshape((-1,))))
            i += 1

        np.savetxt(filename + '.tri', data)

    def get_barycentre(self, reference_frame=False):
        if reference_frame:
            return self.frame.to_ref(np.mean(self.vertices, axis=0).view(Vector))
        else:
            return Vec3(np.mean(self.vertices, axis=0))

    def plot(self, ax, fieldmap=None, vmin=None, vmax=None, alpha=0.3, scale=1.0, antialiased=False,
             linewidth=0, edgecolor=(0, 0, 0), facecolor=None, mesh_name='',
             display_normals=False,  display_vertices_normals=False, display_points=False, display_face_points=False,
             normal_length=3e-3):
        src_r_src_pts = self.frame.to_ref(self.vertices)
        x = src_r_src_pts[:, 0] * scale
        y = src_r_src_pts[:, 1] * scale
        z = src_r_src_pts[:, 2] * scale

        if fieldmap is None:
            if facecolor is None:
                h = ax.plot_trisurf(x, y, z, triangles=self.triangles, alpha=alpha, linewidth=linewidth,
                                    edgecolor=edgecolor, label='Mesh %s' % mesh_name)
            else:
                h = ax.plot_trisurf(x, y, z, triangles=self.triangles, alpha=alpha, linewidth=linewidth,
                                    edgecolor=edgecolor, facecolor=facecolor, label='Mesh %s' % mesh_name)
            if display_normals:
                for f in range(self.triangles.shape[0]):
                    n = (self.tri_normals[f, 1] + self.tri_normals[f, 2]).reshape((-1, 3)) * .5
                    b = (self.tri_vertices[f, 0] + self.tri_vertices[f, 1] + self.tri_vertices[f, 2]).reshape((-1, 3)) \
                        / 3.
                    n = self.frame.to_ref(n)[0, :] * normal_length * scale
                    b = self.frame.to_ref(b)[0, :] * scale
                    ax.quiver(b[0], b[1], b[2],
                              n[0], n[1], n[2],
                              color='red', linestyle='-', arrow_length_ratio=0.0)
            if display_vertices_normals:
                for f in range(self.triangles.shape[0]):
                    for v, n in zip(self.tri_vertices[f, :], self.tri_normals[f, :]):
                        n = self.frame.to_ref(n)[0, :] * normal_length * scale
                        b = self.frame.to_ref(v)[0, :] * scale
                        ax.quiver(b[0], b[1], b[2],
                                  n[0], n[1], n[2],
                                  color='magenta', linewidth=0.3, linestyle='-', arrow_length_ratio=0.0, zorder=3)
            if display_face_points:
                b = Vector(N=len(self.faces))
                i = 0
                for f in self.faces:
                    b[i, :] = self.frame.to_ref(f.barycentre()) * scale
                    i += 1
                ax.scatter(b[:, 0], b[:, 1], b[:, 2], '+', s=5)
            if display_points:
                ax.scatter(x, y, z, 'o', s=7)
            return h, None
        else:
            cmap = cm.get_cmap('viridis')
            if vmin is None:
                vmin = float(np.min(fieldmap))
            if vmax is None:
                vmax = float(np.max(fieldmap))
            norm = colors.Normalize(vmin=vmin, vmax=vmax)

            # Creating a triangulation object and using it to extract the actual triangles.
            # Note if it is necessary that no patch will be vertical (i.e. along the z direction)
            triangle_vertices = np.array([np.array([[x[T[0]], y[T[0]], z[T[0]]],
                                                    [x[T[1]], y[T[1]], z[T[1]]],
                                                    [x[T[2]], y[T[2]], z[T[2]]]]) for T in self.triangles])
            c = norm(fieldmap)
            c[c < 0] = 0

            sm = ScalarMappable(cmap=cmap, norm=norm)

            # Creating the patches and plotting
            collection1 = Poly3DCollection(
                triangle_vertices,
                facecolors=cmap(c),
                edgecolors=None,
                antialiased=antialiased
            )
            h = ax.add_collection(collection1)
            ax.set_xlim((np.min(x), np.max(x)))
            ax.set_ylim((np.min(y), np.max(y)))
            ax.set_zlim((np.min(z), np.max(z)))
            ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))
            return h, sm


class Vertex:
    def __init__(self, idv, v, n, t, b, c):
        self.id = idv
        self.pos = Vector(v)
        self.normal = Vector(n.tolist())
        self.tangent = Vector(t.tolist())
        self.bitangent = Vector(b.tolist())
        self.curvature = c
        self.faces = []
        self.connectivity = []


"""class Triangle:
    def __init__(self, idx: int, vertex1: Vertex, vertex2: Vertex, vertex3: Vertex, surf_id: int):
        self.name = 'Triangle_%d' % idx
        self.index = idx
        self.v1 = vertex1
        self.v2 = vertex3
        self.v3 = vertex2
        self.surf_id = surf_id
        
        c1 = self._edge1.cross(p - v0)
        c2 = self._edge2.cross(p - v2)
        c3 = self._edge3.cross(p - v1)

        self.connectivity = np.concatenate((self.v1.faces, self.v2.faces, self.v3.faces))

        pos0 = vertex1.pos
        pos1 = vertex2.pos
        pos2 = vertex3.pos

        # pre-computed variables for triangle intersection tests
        self._N = (pos1 - pos0).cross(pos2 - pos0)
        in2 = 1 / self._N.norm2()
        self._N1 = (pos2 - pos0).cross(self._N) * in2
        self._N2 = self._N.cross(pos1 - pos0) * in2

        self._d = pos0.dot(self._N)
        self._d1 = -(pos0.dot(self._N1))
        self._d2 = -(pos0.dot(self._N2))

        self._edge1 = self.v2.pos - self.v1.pos
        self._edge2 = self.v3.pos - self.v2.pos
        self._edge3 = self.v1.pos - self.v3.pos
        
        self._edge1 = v2 - v0
        self._edge2 = v1 - v2
        self._edge3 = v0 - v1

        if np.abs(self.v1.normal.dot(self._edge1.normalised().cross(self._edge3.normalised()))) < 0.2:
            self.v1.normal = self.v1.tangent.normalised()
        if np.abs(self.v2.normal.dot(self._edge1.normalised().cross(self._edge2.normalised()))) < 0.2:
            self.v2.normal = self.v2.tangent.normalised()
        if np.abs(self.v3.normal.dot(self._edge3.normalised().cross(self._edge2.normalised()))) < 0.2:
            self.v3.normal = self.v3.tangent.normalised()

        if self.v1.normal.dot(self._N.normalised()) < 0:
            self.v1.normal *= -1
        if self.v2.normal.dot(self._N.normalised()) < 0:
            self.v2.normal *= -1
        if self.v3.normal.dot(self._N.normalised()) < 0:
            self.v3.normal *= -1

        a = self._edge1.norm()
        b = self._edge2.norm()
        c = self._edge3.norm()
        s = (a + b + c) / 2
        br = (self.v1.pos + self.v2.pos + self.v3.pos) * (1 / 3)
        self.mean_length = ((br - pos0).norm() + (br - pos1).norm() + (br - pos2).norm())[0] / 3
        self.area = np.sqrt(s * (s - a) * (s - b) * (s - c))[0]

    def get_connected_faces(self):
        faces_list = []
        for face in self.v1.faces:
            if face != self:
                faces_list.append(face)
        for face in self.v2.faces:
            if face != self:
                faces_list.append(face)
        for face in self.v3.faces:
            if face != self:
                faces_list.append(face)
        return faces_list

    def intersect(self, ray: SRay):
        ori = ray.ori

        # intersection distance computation
        det = ray.dir.dot(self._N)
        if det == 0:
            # ray parallel to the plane
            return False, Vector(), Vector(), np.inf, 0

        t_prim = self._d - (ori.dot(self._N))
        t0 = (t_prim / det)[0]
        if t0 < 0:
            # plane behind the ray origin
            return False, Vector(), Vector(), np.inf, 0

        # intersection point
        p = ori + ray.dir * t0

        # inside-outside test
        c1 = self._edge1.cross(p - self.v1.pos)
        c2 = self._edge2.cross(p - self.v2.pos)
        c3 = self._edge3.cross(p - self.v3.pos)
        if self._N.dot(c1) > 1e-20 or self._N.dot(c2) > 1e-20 or self._N.dot(c3) > 1e-20:
            # P_src is not inside the triangle
            return False, Vector(), Vector(), np.inf, 0

        # UV coordinates
        p_prim = ori * det + ray.dir * t_prim
        u = float((p_prim.dot(self._N1) + det * self._d1) / det)
        v = float((p_prim.dot(self._N2) + det * self._d2) / det)

        # normal interpolation from the 3 vertex normal vectors
        n = (self.v2.normal * u + self.v3.normal * v + self.v1.normal * (1 - u - v))
        n.normalise()
        t = (self.v2.tangent * u + self.v3.tangent * v + self.v1.tangent * (1 - u - v))
        t.normalise()

        # curvature interpolation
        c = (self.v2.curvature * u + self.v3.curvature * v + self.v1.curvature * (1 - u - v))

        return True, n, t, t0, c

    def barycentre(self) -> Vector:
        return (self.v1.pos + self.v2.pos + self.v3.pos) * (1 / 3)

    def normal(self) -> Vector:
        return (self.v2.normal + self.v3.normal) * .5

    def tangents(self) -> (Vector, Vector):
        return (self.v2.tangent + self.v3.tangent) * .5, (self.v2.bitangent + self.v3.bitangent) * .5

    def curvature(self) -> float:
        return (self.v2.curvature + self.v3.curvature) * .5
"""


class Voxel:
    def __init__(self, pt_min, pt_max):
        self.min = np.reshape(pt_min, (3,))
        self.max = np.reshape(pt_max, (3,))

    def surface_area(self):
        return (self.max[0] - self.min[0]) * (self.max[1] - self.min[1]) \
            + (self.max[0] - self.min[0]) * (self.max[2] - self.min[2]) \
            + (self.max[1] - self.min[1]) * (self.max[2] - self.min[2])

    def volume(self):
        return (self.max[0] - self.min[0]) \
            * (self.max[1] - self.min[1]) \
            * (self.max[2] - self.min[2])

    def contains(self, pt):
        return self.min[0] <= pt[0] <= self.max[0] \
            and self.min[1] <= pt[1] <= self.max[1] \
            and self.min[2] <= pt[2] <= self.max[2]

    @staticmethod
    def create_from_2pts(pt1, pt2):
        if pt1[0] < pt2[0]:
            return Voxel(pt1.copy(), pt2.copy())
        else:
            return Voxel(pt2.copy(), pt1.copy())

    @staticmethod
    def create_by_split(main_box, axis, plane_pos, side):
        box = Voxel(main_box.min.copy(), main_box.max.copy())
        if side:
            box.min[axis] = plane_pos
        else:
            box.max[axis] = plane_pos
        return box

    @staticmethod
    def create_from_triangles(triangle_list):
        if len(triangle_list) == 0:
            return
        min_ = np.reshape(triangle_list[0].v1.pos.copy(), (3,))
        max_ = min_.copy()
        for triangle in triangle_list:
            vertices = [triangle.v1, triangle.v2, triangle.v3]
            for vertex in vertices:
                p = np.reshape(vertex.pos.copy(), (3,))
                if min_[0] > p[0]:
                    min_[0] = p[0]
                if min_[1] > p[1]:
                    min_[1] = p[1]
                if min_[2] > p[2]:
                    min_[2] = p[2]
                if max_[0] < p[0]:
                    max_[0] = p[0]
                if max_[1] < p[1]:
                    max_[1] = p[1]
                if max_[2] < p[2]:
                    max_[2] = p[2]
        return Voxel(min_, max_)


class KdTreeNode:
    def __init__(self, triangle_list, max_depth, axis=0, node_depth=0):
        self.left = None
        self.right = None
        self.voxel = Voxel.create_from_triangles(triangle_list)
        self.triangles = triangle_list
        self.depth = node_depth
        self.split_axis = axis
        self.split_pos = 0
        self._max_depth = max_depth

    def is_leaf(self):
        return len(self.triangles) == 0 or self.right is None or self.left is None

    def subdivise(self):
        if len(self.triangles) == 0 or self.depth >= self._max_depth:
            return

        # Determine best split plane position
        # Yet: simple method = median
        self.split_pos = (self.voxel.min[self.split_axis] + self.voxel.max[self.split_axis]) / 2

        left_box = Voxel.create_by_split(
            main_box=self.voxel,
            axis=self.split_axis,
            plane_pos=self.split_pos,
            side=False
        )
        right_box = Voxel.create_by_split(
            main_box=self.voxel,
            axis=self.split_axis,
            plane_pos=self.split_pos,
            side=True
        )

        left_triangles = []
        right_triangles = []
        for triangle in self.triangles:
            v1 = triangle.v1.pos[0, :]
            v2 = triangle.v2.pos[0, :]
            v3 = triangle.v3.pos[0, :]
            if left_box.contains(v1) or left_box.contains(v2) or left_box.contains(v3):
                left_triangles.append(triangle)
            if right_box.contains(v1) or right_box.contains(v2) or right_box.contains(v3):
                right_triangles.append(triangle)

        # Create child nodes
        next_split_axis = self.split_axis + 1
        if next_split_axis == 3:
            next_split_axis = 0
        self.left = KdTreeNode(
            triangle_list=left_triangles,
            node_depth=self.depth + 1,
            max_depth=self._max_depth,
            axis=next_split_axis
        )
        self.right = KdTreeNode(
            triangle_list=right_triangles,
            node_depth=self.depth + 1,
            max_depth=self._max_depth,
            axis=next_split_axis
        )

        self.left.subdivise()
        self.right.subdivise()


class KdTree:
    def __init__(self, max_depth):
        self.root = None
        self._max_depth = max_depth

    def build(self, triangles):
        # Create root node
        self.root = KdTreeNode(
            triangle_list=triangles,
            max_depth=self._max_depth
        )
        self.root.subdivise()


class StackNode:
    def __init__(self, knode, t1=0, t2=1e30):
        self.node = knode
        self.tmin = t1
        self.tmax = t2
