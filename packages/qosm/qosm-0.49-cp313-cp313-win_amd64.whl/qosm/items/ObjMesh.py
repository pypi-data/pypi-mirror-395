import numpy as np

from qosm.items.Mesh import Mesh
from qosm.utils.Pose import Frame, Vector, Quaternion

ELEMENT_TYPES = {
    "line": 2,
    "line3": 3,
    "triangle": 3,
    "quadrangle": 4,
    "tetrahedron": 4,
    "hexahedron": 8,
    "prism": 6,
    "pyramid": 5,
}


def parse_vertices(vertices_strings):
    v = np.zeros((len(vertices_strings), 3))
    i = 0
    for vertice_strings in vertices_strings:
        v[i, :] = vertice_strings.split()
        i += 1

    return v


def parse_faces(faces_strings):
    faces_v = np.zeros((len(faces_strings), 3), dtype=int)
    faces_n = np.zeros((len(faces_strings), 3), dtype=int)
    i = 0
    for face_string in faces_strings:
        j = 0
        for e in face_string.split():
            if '//' in e:  # f v//vn
                v_idx = int(e.split('//')[0]) - 1
                n_idx = int(e.split('//')[1]) - 1
            elif '/' in e:
                if len(e.split('/')) == 2:  # f v/vt
                    v_idx = int(e.split('/')[0]) - 1
                    n_idx = int(e.split('/')[0]) - 1
                else:  # f v/vt/vn
                    v_idx = int(e.split('/')[0]) - 1
                    n_idx = int(e.split('/')[2]) - 1
            else:  # f v v v
                v_idx = int(e.split()[0]) - 1
                n_idx = int(e.split()[0]) - 1
            faces_v[i, j] = v_idx
            faces_n[i, j] = n_idx
            j += 1
        i += 1
    return faces_v, faces_n


def triangulate(faces: list):
    new_faces = []
    for face in faces:
        elements = np.array(face.split())
        if len(elements) == 3:
            new_faces.append(face)
            continue
        new_faces.append(' '.join(elements[[0, 1, 2]]))
        new_faces.append(' '.join(elements[[2, 3, 0]]))
    return new_faces


class ObjMesh(Mesh):
    def __init__(self, f_obj_glo: Frame):
        super(ObjMesh, self).__init__(f_obj_glo)
        self.frame = f_obj_glo

    def load(self, filepath: str, offset: Vector = Vector(), rot: Quaternion = Quaternion(), center: bool = False):
        num_faces_3_edges = 0
        num_faces_4_edges = 0

        with open(filepath) as f:
            lines = f.readlines()
            vStrings = [x.replace('\n', '').strip('v') for x in lines if x.startswith('v ')]
            vertices = parse_vertices(vStrings).view(Vector)

            barycentre = Vector()

            if center:
                barycentre = np.mean(vertices, axis=0).reshape((-1, 3))
            vertices -= barycentre

            self.vertices = rot.rotate(vertices)

            self.vertices += offset

            vnStrings = [x.strip('vn') for x in lines if x.startswith('vn')]
            """if not vnStrings:  # if There is no normal vectors in the obj file then compute them
                normals = fillNormalsArray(len(vStrings))
            else:"""
            self.normals = parse_vertices(vnStrings)
            self.normals = rot.rotate(self.normals.view(Vector))

            faces = [x.replace('\n', '').strip('f') for x in lines if x.startswith('f')]

            for face in faces:
                if len(face.split()) == 3:
                    num_faces_3_edges += 1
                elif len(face.split()) == 4:
                    num_faces_4_edges += 1
                else:
                    raise Exception('Faces with more than 4 edges are not supported')

            """print("File:", filepath, "\nTotal number of faces:", len(faces),
                  "\nNumber of faces with 3 vertices:", num_faces_3_edges,
                  "\nNumber of faces with 4 vertices:", num_faces_4_edges,
                  "\nTotal number of vertices:", len(self.vertices),
                  "\nTotal number of normals:", len(self.normals))"""
            if num_faces_4_edges > 0:
                faces = triangulate(faces)

            self.triangles, triangles_n = parse_faces(faces)

        self.tri_vertices = self.vertices[self.triangles]
        self.tri_normals = self.normals[triangles_n]
        self.tri_tangents = self.tri_normals*0.
        self.tri_curvatures = np.zeros((self.triangles.shape[0], 3))

    def pre_build(self, scale=1e-3, create_obj=None, progress=None, view=False, show_vectors=True,
                  offset: Vector = Vector()):
        pass