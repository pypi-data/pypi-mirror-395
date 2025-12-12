from qosm.items.SlabMesh import SlabMesh
from qosm.items.StepMesh import StepMesh
from qosm._core import Medium, Vec3, Frame
from numpy import pi


def create_medium(epsr: float, loss_tan: float = 0.) -> Medium:
    medium = Medium()
    epsr_sec = epsr * loss_tan
    medium.set_with_permittivity(epsr, epsr_sec)
    return medium


def create_pec() -> Medium:
    medium = Medium(is_pec=True)
    return medium


def create_slab_mesh(
        shape: str,
        medium: Medium,
        size: tuple,
        element_size_mm: float = 4.,
        x_mm: float = 0., y_mm: float = 0., z_mm: float = 0.,
        rx_deg: float = 0., ry_deg: float = 0., rz_deg: float = 0.,
        offset: Vec3 = Vec3(),
        flip_normal: bool = False,
        view: bool = False,
        ext_medium: Medium = Medium(),
        bounces=None
        ) -> SlabMesh:

    if bounces is None:
        bounces = [-1, -1]

    mesh = SlabMesh(Frame())
    mesh.bounces = bounces
    mesh.load(element_size=element_size_mm * 1e-3, shape=shape, size=size, view=view, flip_normal=flip_normal,
              offset=offset)
    mesh.set_dioptre(ext_medium, medium)
    ori = Vec3(x_mm*1e-3, y_mm*1e-3, z_mm*1e-3)
    axis = Vec3(rx_deg * pi / 180., ry_deg * pi / 180., rz_deg * pi / 180.)
    mesh.frame = Frame(ori=ori, axis=axis.normalised(), angle=axis.norm(), deg=False)
    return mesh


def load_step(filepath: str,
              medium: Medium,
              element_size_mm: float = 4.,
              x_mm: float = 0., y_mm: float = 0., z_mm: float = 0.,
              rx_deg: float = 0., ry_deg: float = 0., rz_deg: float = 0.,
              offset_mm: Vec3 = Vec3(),
              scale=1e-3
              ) -> StepMesh:
    free_space = Medium()

    ori = Vec3(x_mm*1e-3, y_mm*1e-3, z_mm*1e-3)
    axis = Vec3(rx_deg * pi / 180., ry_deg * pi / 180., rz_deg * pi / 180.)

    msh1_frame = Frame(ori=ori, axis=axis.normalised(), angle=axis.norm(), deg=False)
    mesh = StepMesh(msh1_frame)
    mesh.load_step(filename=filepath, element_size=element_size_mm, scale=scale, create_obj=False, view=False,
                   offset=offset_mm, show_vectors=False)
    mesh.set_dioptre(free_space, medium)
    mesh.frame = msh1_frame
    return mesh
