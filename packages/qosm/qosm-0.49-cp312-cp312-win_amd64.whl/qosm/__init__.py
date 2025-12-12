"""
QOSM - Quasi-Optical System Modelling
"""
try:
    from .__version__ import __version__
except ImportError:
    __version__ = "0.0.0"

from ._core import (Vec3, Quaternion, Source, RectangularAperture, Horn, VirtualSource, Field, Vector, Medium, Dioptre,
                    Ray, Beam, Triangle, PlaneType, Grid, Domain, create_beam, Frame, field_expansion, beam_tracing,
                    surface_beam_tracing, compute_collected_power, Surface, Item, GaussianBeam, gbtc_beam_tracing,
                    gbtc_compute_coupling, gbtc_apply_abcd)

from .items.Mesh import Mesh
from .items.MshMesh import MshMesh
from .items.ObjMesh import ObjMesh
from .items.Object import Object
from .items.SlabMesh import SlabMesh
from .items.Triangle import Triangle as pyTriangle
from .items.utils import create_medium, create_pec, create_slab_mesh, load_step

from .sources.mode_matching import mm_run

from .propagation import GBTC, PW
from .propagation.PermittivityExtraction import PermittivityEstimation, moving_average, filter_s2p, add_noise

from .utils.Field import Field as pyField
from .utils.Pose import Vector as pyVector, Quaternion as pyQuaternion, Frame as pyFrame, rv2base, q2base
from .utils.toml_config import load_config_from_toml

from  .gui import gui