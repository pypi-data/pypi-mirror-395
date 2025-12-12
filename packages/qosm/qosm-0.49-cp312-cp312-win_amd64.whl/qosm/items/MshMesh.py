import gmsh

from qosm.items.Mesh import Mesh
from qosm._core import  Frame, Vec3


class MshMesh(Mesh):
    def __init__(self, f_obj_ref: Frame = Frame()):
        super().__init__(f_obj_ref)

    def load_mesh(self, element_size: float, scale: float = 1., view=False, show_vectors=False):
        gmsh.option.setNumber("Geometry.Tolerance", 1e-8)
        gmsh.option.setNumber("Mesh.Algorithm", 6)
        gmsh.option.setNumber('Mesh.MeshSizeMin', element_size)
        gmsh.option.setNumber('Mesh.MeshSizeMax', element_size)

        gmsh.option.setNumber('Mesh.SmoothNormals', 0)
        gmsh.option.setNumber('Mesh.AngleSmoothNormals', 0)
        gmsh.option.setNumber("Geometry.OCCImportLabels", 0)

        gmsh.model.occ.removeAllDuplicates()
        gmsh.model.occ.synchronize()

        gmsh.model.mesh.generate(1)
        gmsh.model.mesh.generate(2)
        gmsh.model.mesh.removeDuplicateNodes()

        self.pre_build(scale, False, None, view, show_vectors, Vec3(), False)
