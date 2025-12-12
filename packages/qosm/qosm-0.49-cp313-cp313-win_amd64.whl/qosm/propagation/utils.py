from qosm._core import Beam as _Beam
from qosm._core import Vec3 as _Vec3
from qosm._core import Frame as _Frame

from qosm.utils.Pose import Vector

import numpy as np
from numpy import pi

import pandas as pd


def plane(d: float, z: float, dims: tuple[float, float]):
    """Define a plane surface"""
    dx = dims[0] / 2
    dy = dims[1] / 2
    numx = 1 + int(2 * dx / d)
    numy = 1 + int(2 * dy / d)
    xa_ = np.linspace(-dx, dx, numx, endpoint=True)
    ya_ = np.linspace(-dy, dy, numy, endpoint=True)
    r_pts = Vector(N=xa_.shape[0] * ya_.shape[0])
    (Xa_, Ya_) = np.meshgrid(xa_, ya_)
    r_pts[:, 0] = np.reshape(Xa_, (-1,))
    r_pts[:, 1] = np.reshape(Ya_, (-1,))
    r_pts[:, 2] = z
    nb_pts = r_pts.shape[0]
    return r_pts, nb_pts


def icosphere(d: float, r: float, theta_r_rad: float = 0.0, cut_half: int = 1):
    """ Generate Node xyz positions
    Used 2004 paper by Markus Deserno, Max-Planck-Institut:
    "How to generate equidistributed points on the surface of a sphere"
    Enforces constant intervales d_theta ~ d_phi
    Assumes unit radius
    Does not replace MATLAB "sphere" function
    Create Sphere 3D Geometry Centered at (x,y,z) = (0,0,0)
    
    N: target number of nodes
    N_new: final number of nodes
    X,Y,Z: column vectors of length N_new containing _node coordinates
    """
    dist = d / r
    area = 2 * dist ** 2
    M_theta = round((pi - theta_r_rad) / dist)
    d_theta = (pi - theta_r_rad) / M_theta
    d_phi = area / d_theta

    Theta_ = np.linspace(0, M_theta - 1, M_theta)
    # Theta_ = pi * (Theta_ + 0.5) / M_theta
    Theta_ = pi * Theta_ / M_theta
    if cut_half > 0:
        Theta_ = Theta_[Theta_ <= pi / 2 - theta_r_rad + 0.01]
    elif cut_half < 0:
        Theta_ = Theta_[Theta_ >= pi / 2 + theta_r_rad - 0.01]

    M_phi = np.round(4 * pi * np.sin(Theta_) / d_phi)  # not exact

    N_new = int(np.sum(M_phi))

    iT = 0
    if cut_half == 0:
        ii = 0
    else:
        N_new += 1
        ii = 1

    r_pts = np.zeros((N_new, 3))

    for Theta in Theta_:
        idx = int(M_phi[iT])
        phi_ = np.linspace(0, idx - 1, idx)
        Phi_ = 2 * pi * (phi_ - 1) / M_phi[iT]

        r_pts[ii:(ii + idx), 0] = np.sin(Theta) * np.cos(Phi_)
        r_pts[ii:(ii + idx), 1] = np.sin(Theta) * np.sin(Phi_)
        r_pts[ii:(ii + idx), 2] = np.cos(Theta)

        ii += idx
        iT += 1
    if cut_half >= 0:
        r_pts[0, :] = [0, 0, 1]
    elif cut_half < 0:
        r_pts[0, :] = [0, 0, -1]

    return Vector(r_pts * r), N_new


def avg_distance(points):
    n = points.shape[0]
    d = np.zeros((n, 2))
    for i in range(n):
        dist = (points - points[i, :]).norm()
        dist = np.sort(dist[dist > 0])[0:3]
        d[i, :] = [np.median(dist), np.median(dist)]
    return d


def filter_beam_for_surface(src, mesh) -> (Vector, float, Vector, list):
    """
    Select vertices, normals and curvatures to use for beam tracing on a surface
    WARNING: the function uses the initial normal list, in which no normal correction is applied
    """
    vertices = mesh.frame.to_ref(mesh.vertices.view(Vector))

    # compute with incoming field
    E, _, P = src.fields(vertices)
    intensity = E.intensity(normalise=True)

    normals = mesh.frame.rot_to_ref(mesh.normals.view(Vector))
    curvatures = mesh.curvatures

    # filter with only visible point from the field
    idx = (P.normalised().dot(normals) <= 0).reshape((-1,))
    intensity *= idx.astype('float')

    vertices = vertices[idx, :]
    normals = normals[idx, :]
    curvatures = curvatures[idx]
    d = np.mean(avg_distance(vertices)[:, 0])

    return vertices, normals, curvatures, d


def beams_to_panda(beams: list[_Beam], types: list[int] = None) -> pd.DataFrame:
    output_beams = []

    if types is not None:
        for beam in beams:
            if beam.beam_type in types:
                output_beams.append(beam)
    else:
        output_beams = beams

    df = pd.DataFrame(data={
        'ori': [beam.frame.ori.tuple() for beam in output_beams],
        'fx': [beam.frame.x.tuple() for beam in output_beams],
        'fy': [beam.frame.y.tuple() for beam in output_beams],
        'fz': [beam.frame.z.tuple() for beam in output_beams],
        'alpha': [beam.alpha for beam in output_beams],
        'k0': [beam.k0 for beam in output_beams],
        'n': [beam.n for beam in output_beams],
        'kappa': [beam.kappa for beam in output_beams],
        'a0': [beam.a0 for beam in output_beams],
        'phi0': [beam.phi0 for beam in output_beams],
        'init_power': [beam.init_power for beam in output_beams],
        'theta': [beam.theta for beam in output_beams],
        'q1': [beam.q1 for beam in output_beams],
        'q2': [beam.q2 for beam in output_beams],
        'z_range': [beam.z_range for beam in output_beams],
        'type': [beam.beam_type for beam in output_beams]
    })
    return df


def panda_to_beams(df: pd.DataFrame | object, types: list[int] = None) -> list[_Beam]:
    beams = []
    i = 0
    for index, row in df.iterrows():
        if types is not None and int(row['type']) not in types:
            continue

        beam = _Beam()
        beam.k0 = row['k0']
        beam.n = row['n']
        beam.kappa = row['kappa']
        beam.alpha = row['alpha']
        beam.beam_type = int(row['type'])
        beam.q1 = row['q1']
        beam.q2 = row['q2']
        beam.theta = row['theta']
        beam.init_power = row['init_power']
        beam.a0 = row['a0']
        beam.phi0 = row['phi0']
        beam.frame = _Frame(
            _Vec3(row['fx'].astype(float)),
            _Vec3(row['fy'].astype(float)),
            _Vec3(row['fz'].astype(float)),
            _Vec3(row['ori'].astype(float)),
        )
        beam.init_power = row['init_power']
        beam.z_range = row['z_range']

        beams.append(beam)
        i += 1

    return beams
