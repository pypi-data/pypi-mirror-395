import gmsh
from qosm._core import Frame, Vec3

from qosm.items.Mesh import Mesh


class StepMesh(Mesh):
    def __init__(self, f_obj_ref: Frame = Frame()):
        super().__init__(f_obj_ref)

    def load_step(self, filename, element_size: float, scale: float = 1e-3, create_obj=None, progress=None,
                  view=False, show_vectors=True, offset: Vec3 = Vec3(), centre_shape=False):
        gmsh.clear()
        gmsh.model.add(filename)

        # Mesh
        gmsh.option.setNumber("Geometry.Tolerance", 1e-8)
        gmsh.option.setNumber("Mesh.Algorithm", 6)
        gmsh.option.setNumber('Mesh.MeshSizeMin', element_size)
        gmsh.option.setNumber('Mesh.MeshSizeMax', element_size)

        gmsh.option.setNumber('Mesh.SmoothNormals', 0)
        gmsh.option.setNumber('Mesh.AngleSmoothNormals', 0)
        gmsh.option.setNumber("Geometry.OCCImportLabels", 0)  # import colors from STEP

        gmsh.model.occ.importShapes(filename, format="step")

        gmsh.model.occ.removeAllDuplicates()
        gmsh.model.occ.synchronize()

        gmsh.model.mesh.generate(1)
        gmsh.model.mesh.generate(2)
        gmsh.model.mesh.removeDuplicateNodes()

        self.pre_build(scale, create_obj, progress, view, show_vectors, offset, centre_shape)

        if create_obj:
            with open('%s.obj' % filename, 'w') as f:
                f.write('%s' % self._obj_txt)
                f.close()
