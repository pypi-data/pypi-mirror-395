import gmsh
from numpy import pi
from qosm._core import Frame, Vec3

from qosm.items.Mesh import Mesh

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


class SlabMesh(Mesh):
    def __init__(self, f_obj_glo: Frame):
        super(SlabMesh, self).__init__(f_obj_glo)
        self.frame = f_obj_glo

    def load(self, element_size: float, shape: str, size: tuple, flip_normal: bool = False, obj_file=None,
             offset: Vec3 = Vec3(), progress=None, view=False):
        gmsh.clear()
        gmsh.model.add("OBJECT")

        if shape == 'sphere':
            if len(size) == 4:
                radius, angle1, angle2, angle3 = size
            else:
                radius = size[0]
                angle1, angle2, angle3 = (-pi/2, pi/2, 2*pi)
            gmsh.model.occ.addSphere(xc=0, yc=0, zc=0, radius=radius, angle1=angle1, angle2=angle2, angle3=angle3)
        if shape == 'cylinder':
            radius, length = size
            gmsh.model.occ.addCylinder(x=0, y=0, z=-length/2, dx=0, dy=0, dz=length, r=radius)
        if shape == 'disk':
            if len(size) == 2:
                L = 0.
                ru, rv = size
            else:
                ru, rv, L = size
            if ru > rv:
                rx = ru
                ry = rv
                x_axis = (1, 0, 0)
            else:
                rx = rv
                ry = ru
                x_axis = (0, 1, 0)
            L *= 1 - 2*float(flip_normal)
            gmsh.model.occ.addDisk(xc=0, yc=0, zc=0, rx=rx, ry=ry,
                                   zAxis=(0, 0, 1 - 2*float(flip_normal)), xAxis=x_axis)
        elif shape == 'box':
            width, height, length = size
            gmsh.model.occ.addBox(x=-width/2, y=-height/2, z=-length/2, dx=width, dy=height, dz=length)

        elif shape == 'rect':
            width, height = size
            tag = gmsh.model.occ.addRectangle(x=-width/2, y=-height/2, z=0, dx=width, dy=height)
            if flip_normal:
                gmsh.model.occ.rotate([(tag, 2)], 0, 0, 0, 1, 0, 0, pi)

        # Mesh
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.Algorithm", 6)
        gmsh.option.setNumber('Mesh.MeshSizeMin', element_size)
        gmsh.option.setNumber('Mesh.MeshSizeMax', element_size)

        gmsh.model.mesh.generate(2)

        create_obj = obj_file is not None
        self.pre_build(1.0, create_obj, progress, view, offset=offset, show_vectors=False)

        if create_obj:
            with open('%s.obj' % obj_file, 'w') as f:
                f.write('%s' % self._obj_txt)
                f.close()
