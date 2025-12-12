import traceback
from copy import deepcopy
from os.path import exists

import numpy as np
from numpy import zeros_like, real, min, meshgrid
from numpy import genfromtxt

from qosm.gui.dialogs.objects.LensDialog import create_lens_mesh
from qosm.gui.managers import RequestType
from scipy.interpolate import RegularGridInterpolator, interp1d

from qosm.gui.dialogs.sources.HornCreateDialog import get_all_te_modes
from qosm.items.utils import load_step, create_slab_mesh, create_pec
from qosm import Grid, PlaneType, Vec3, Domain, VirtualSource, Dioptre, Medium, field_expansion, Beam, Horn, Frame
from scipy.spatial.distance import pdist

from qosm.sources.far_field_rect import far_field_from_request


class SimulationAborted(Exception):
    def __init__(self, message="Unknown error"):
        self.message = message.replace('Simulation aborted: ', '')
        super().__init__(f'Simulation aborted: {self.message}')


class ReshapeAborted(Exception):
    def __init__(self, message="Unknown error"):
        self.message = message.replace('Reshape aborted: ', '')
        super().__init__(f'Reshape aborted: {self.message}')


class SimulationManager:
    def __init__(self, requests_data, objects_data, source_data, sweep_data):
        self.frequency_GHz = 0
        self.elements = {}
        self.src_uuid = None
        self.pipeline = None
        self.results = {}
        self.requests = requests_data
        self.objects = objects_data
        self.source_data = source_data
        self.sweep = sweep_data

    def reset(self):
        self.frequency_GHz = 0
        self.elements = {}
        self.src_uuid = None
        self.pipeline = None

    @staticmethod
    def gbe_grid_from_parameters(obj, freq_GHz: float = None, do_translation: bool = True, objects = None) -> Grid:
        if obj is None:
            return None

        u_size = obj['parameters']['size_u']
        v_size = obj['parameters']['size_v']
        sampling_step = obj['parameters']['sampling_step']
        sampling_unit = obj['parameters'].get('sampling_unit', None)
        if freq_GHz is not None:
            if sampling_unit == 'lambda':
                lambda_0 = 299792458. / (freq_GHz * 1e9)
                sampling_step *= lambda_0
            elif sampling_unit == 'mm':
                sampling_step *= 1e-3
        else:
            sampling_step = u_size / 11  # for 3D view

        center = list(obj['parameters']['position']) if do_translation else [0, 0, 0]
        if do_translation and obj['parameters'].get('reference', None) is not None and objects:

            reference_pos = objects[obj['parameters']['reference']]['parameters'].get('position', [0, 0, 0])
            for i in range(3):
                center[i] += reference_pos[i]

        plane_types = {'XY': PlaneType.XY, 'ZX': PlaneType.ZX, 'ZY': PlaneType.ZY}
        plane_type = plane_types[obj['parameters']['plane']]

        # Calculate ranges based on center and total sizes
        if plane_type == 'ZX':
            # ZX plane
            u_range = [center[0] - u_size / 2, center[0] + u_size / 2, sampling_step]
            v_range = [center[2] - v_size / 2, center[2] + v_size / 2, sampling_step]
            n = center[1]
        elif plane_type == 'ZY':
            # ZY plane
            u_range = [center[1] - u_size / 2, center[1] + u_size / 2, sampling_step]
            v_range = [center[2] - v_size / 2, center[2] + v_size / 2, sampling_step]
            n = center[0]
        else:
            # Fallback to XY
            u_range = [center[0] - u_size / 2, center[0] + u_size / 2, sampling_step]
            v_range = [center[1] - v_size / 2, center[1] + v_size / 2, sampling_step]
            n = center[2]

        if freq_GHz is None:
            return Grid(u_range, v_range, n=n, plane=plane_type)
        else:
            return Grid(u_range, v_range, n=n, plane=plane_type), sampling_step

    @staticmethod
    def nf_grid_from_parameters(obj) -> Grid:
        if obj is None:
            return None

        u_range = obj['parameters']['u_range']
        v_range = obj['parameters']['v_range']
        n = obj['parameters']['n']

        plane_types = {'XY': PlaneType.XY, 'ZX': PlaneType.ZX, 'ZY': PlaneType.ZY}
        plane_type = plane_types[obj['parameters']['plane']]

        return Grid(u_range, v_range, n=n, plane=plane_type)

    def add_gbe_grid(self, obj_uuid, obj):
        # Create new Grid object with updated parameters
        self.elements[obj_uuid] = {
            'vsrc': VirtualSource(frequency_GHz=self.frequency_GHz),
            'grid': None,
            'sampling_step': obj['parameters']['sampling_step'],
            'sampling_unit': obj['parameters']['sampling_unit'],
            'kappa': obj['parameters']['kappa'],
            'source_uuid': obj['parameters']['source'],
            'reference_uuid': obj['parameters']['reference']
        }

    def add_gbt_domain(self, obj_uuid, obj):
        # load meshes
        geometry = []
        for mesh_uuid in obj['parameters']['meshes']:
            _obj = self.objects.get(mesh_uuid, None)
            if _obj is None:
                continue
            # load mesh
            medium_value = _obj['parameters'].get('medium', {'type': int(0), 'value': 1.0 - 0j})
            if medium_value['type'] == 0:
                medium = Medium()
                medium.set_with_permittivity(epsilon_r_=medium_value['value'])
            elif medium_value['type'] == 1:
                medium = Medium(medium_value['value'])
            else:
                medium = create_pec()
            element_size_mm = _obj['parameters'].get('element_size', 4)
            if hasattr(element_size_mm, '__len__'):
                element_size_mm = element_size_mm[0]
            scale = _obj['parameters'].get('scale', 1e-3)
            pos = _obj['parameters']['position']
            att = _obj['parameters']['rotation']
            if _obj['type'] == 'StepMesh':
                if not exists(_obj['parameters']['filepath']):
                    raise SimulationAborted('Step File "{}" not found'.format(_obj['parameters']['filepath']))
                m = load_step(filepath=_obj['parameters']['filepath'], medium=medium, element_size_mm=element_size_mm,
                              x_mm=pos[0] * 1e3, y_mm=pos[1] * 1e3, z_mm=pos[2] * 1e3, rx_deg=att[0], ry_deg=att[1],
                              rz_deg=att[2], offset_mm=Vec3() * 1e3, scale=scale)
            elif _obj['type'] == 'LensMesh':
                m = create_lens_mesh(_obj['parameters'])
                _axis = Vec3(att)
                _angle = _axis.normalise()
                m.frame = Frame(ori=Vec3(pos), axis=_axis, angle=_angle, deg=True)
                m.dioptre = Dioptre(ior1=(1., 0.), ior2=(_obj['parameters']['ior'], 0), is_metallic=False)
                m.dioptre.pec = False
            else:
                shape_type = _obj['parameters']['shape_type']
                flip_normal = shape_type == 'rect' or shape_type == 'disk'
                shape_size = _obj['parameters']['shape_params']
                if shape_type == 'sphere':
                    shape_size = (shape_size[0], shape_size[1] * np.pi / 180., shape_size[2] * np.pi / 180.,
                                  shape_size[3] * np.pi / 180.)
                else:
                    shape_size = tuple([el for el in shape_size])
                m = create_slab_mesh(shape=shape_type, medium=medium, size=shape_size, element_size_mm=element_size_mm,
                                     x_mm=pos[0] * 1e3, y_mm=pos[1] * 1e3, z_mm=pos[2] * 1e3, rx_deg=att[0],
                                     ry_deg=att[1], rz_deg=att[2], offset=Vec3(), flip_normal=flip_normal)
            # retrieve mesh geometry
            geometry += m.geometry

        domain = Domain(geometry=geometry)
        domain.set_gbt_settings(
            num_bounces=[int(i) for i in obj['parameters']['num_bounces']],
            threshold_power=float(obj['parameters']['power_threshold'])
        )
        self.elements[obj_uuid] = {
            'vsrc': None,
            'domain': domain,
            'meshes': obj['parameters']['meshes']
        }


    def build_source(self, source):
        if source['type'] == 'NearFieldSource':
            self.elements[self.src_uuid]['vsrc'] = VirtualSource(frequency_GHz=self.frequency_GHz)
        elif source['type'] == 'GaussianBeam':
            polarisation = (complex(source['parameters']['polarization']['x']),
                            complex(source['parameters']['polarization']['y']))
            w0 = (source['parameters']['w0'] * 1e-3, source['parameters']['w0'] * 1e-3)
            z0 = (source['parameters']['z0'] * 1e-3, source['parameters']['z0'] * 1e-3)
            beam = Beam(freq=self.frequency_GHz * 1e9, ior=(1.0, 0.0), w0=w0, z0=z0, polarisation=polarisation)
            vsrc = VirtualSource(frequency_GHz=self.frequency_GHz)
            vsrc.init(beams=(beam,))
            self.elements[self.src_uuid]['vsrc'] = vsrc
        elif source['type'] == 'Horn':
            horn = Horn(frequency_GHz=self.frequency_GHz)
            params = source['parameters']
            modes, _ = get_all_te_modes(params['modes'], shape=params['shape'], frequency_GHz=params['frequency_GHz'],
                                        a=params['a'], b=params['b'])
            horn.init(Lx=params['a'], Ly=params['b'], modes=modes, rot_z_deg=params['rot_z_deg'], num_pts_aperture=61)
            self.elements[self.src_uuid]['horn'] = horn

    def set_source(self, src_uuid, source):
        if source['type'] == 'NearFieldSource':
            # A NearFieldSource need a GBE to be used and will generate a VirtualSource
            self.frequency_GHz = source['parameters']['frequency_GHz']
            self.elements[src_uuid] = {
                'vsrc': VirtualSource(frequency_GHz=self.frequency_GHz),
                'nf_source_data': source['parameters']
            }
        elif source['type'] == 'GaussianBeam':
            self.frequency_GHz = source['parameters']['frequency_GHz']
            polarisation = (complex(source['parameters']['polarization']['x']),
                            complex(source['parameters']['polarization']['y']))
            w0 = (source['parameters']['w0'] * 1e-3, source['parameters']['w0'] * 1e-3)
            z0 = (source['parameters']['z0'] * 1e-3, source['parameters']['z0'] * 1e-3)
            beam = Beam(freq=self.frequency_GHz * 1e9, ior=(1.0, 0.0), w0=w0, z0=z0, polarisation=polarisation)
            vsrc = VirtualSource(frequency_GHz=self.frequency_GHz)
            vsrc.init(beams=(beam,))
            self.elements[src_uuid] = {
                'vsrc': vsrc,
                'parameters': source['parameters']
            }
        elif source['type'] == 'Horn':
            self.frequency_GHz = source['parameters']['frequency_GHz']
            self.elements[src_uuid] = {
                'horn': None,
                'parameters': source['parameters']
            }
        else:
            raise SimulationAborted('Invalid main source')

        self.elements[src_uuid]['type'] = source['type']
        self.src_uuid = src_uuid

    def initialise(self, pipeline):
        for i, uuid_node in enumerate(pipeline):
            # the very first on MUST be a main source
            if i == 0:
                src = self.source_data['source']
                if self.source_data['uuid'] != uuid_node:
                    raise SimulationAborted(f'First node must be the active main source')
                if src is None:
                    raise SimulationAborted(f'Empty source found for uuid {uuid_node}')
                if src['type'] == 'NearFieldSource' and self.sweep['target'][0] == 'freq_GHz':
                    f = src['parameters']['frequency_GHz']
                    raise SimulationAborted(f'Frequency sweep is not possible (fixed frequency of {f} GHz)')
                self.set_source(uuid_node, src)
            else:
                obj = self.objects.get(uuid_node, None)
                if obj is None:
                    raise SimulationAborted(f'Empty item found for uuid {uuid_node}')
                if obj['type'] == 'GBE':
                    self.add_gbe_grid(uuid_node, obj)
                elif obj['type'] == 'Domain':
                    self.add_gbt_domain(uuid_node, obj)
                else:
                    _type = obj['type']
                    raise SimulationAborted(f'Invalid item found (type: {_type})')

        self.pipeline = pipeline

    def run(self, progress_callback = None, warning_callback = None):
        if progress_callback:
            progress_callback(0)

        # set sweep if applicable
        sweep_target = self.sweep['target']
        sweep_attribute = self.sweep['attribute']
        if sweep_target[0] != 'None':
            num_iterations = int(self.sweep['sweep'][2])
            start_val = float(self.sweep['sweep'][0])
            stop_val = float(self.sweep['sweep'][1])
            value_array = np.linspace(start_val, stop_val, num_iterations, endpoint=True)
        else:
            num_iterations = 1
            value_array = np.array([])

        # initialize requests
        self.results = {}
        for req_uuid, req in self.requests.items():
            if not req['enabled']:
                continue

            if req['type'] == RequestType.NEAR_FIELD.name and req['parameters'].get('domain', None) is not None:

                u_range = req['parameters'].get('u_range', (0, 0, 1))
                v_range = req['parameters'].get('v_range', (0, 0, 1))
                n = req['parameters'].get('n', 0)

                self.results[req_uuid] = {
                    'req_uuid': req_uuid,
                    'req_name': req['name'],
                    'req_field': req['parameters'].get('field', None),
                    'request_type': 'NearField',  # Add request type
                    'data': [None for _ in range(num_iterations)],
                    'domain_name': self.objects[req['parameters']['domain']]['name'],
                    'sweep_values': value_array,
                    'sweep_attribute': sweep_attribute,
                    'grid': {
                        'u_range': u_range,
                        'v_range': v_range,
                        'n': n,
                        'plane': req['parameters'].get('plane', 'XY')
                    }
                }
            elif req['type'] == RequestType.FAR_FIELD.name:
                req_name = req['name']
                horn_uuid = req['parameters']['horn']

                if self.source_data['source']['type'] != 'Horn':
                    warning_callback(f"Request '{req_name}': The main source is not a Horn, request ignored")
                    req['enabled'] = False
                    continue

                if horn_uuid == 'current_selected_source':
                    horn_uuid = self.source_data['uuid']
                elif self.objects.get(horn_uuid, None) is None:
                    warning_callback(f"Request '{req_name}': The main source is not the requested Horn, request ignored")
                    req['enabled'] = False
                    continue

                self.results[req_uuid] = {
                    'req_uuid': req_uuid,
                    'req_name': req_name,
                    'request_type': 'FarField',  # Add request type
                    'data': [None for _ in range(num_iterations)],
                    'horn_name': self.objects[horn_uuid]['name'],
                    'sweep_values': value_array,
                    'sweep_attribute': sweep_attribute,
                    'grid': {
                        'theta_range': req['parameters']['theta_range'],
                        'phi': req['parameters']['phi'],
                    }
                }

        num_steps = len(self.elements)
        index_update = 0

        for ii in range(num_iterations):
            if sweep_target[0] == 'freq_GHz':
                self.frequency_GHz = float(value_array[ii])
                for _, element in self.elements.items():
                    if element.get('vsrc', None) is not None:
                        element['vsrc'] = VirtualSource(frequency_GHz=self.frequency_GHz)

            elif sweep_target[0] == 'step' and sweep_target[1] in self.objects:
                step_uuid = str(sweep_target[1])
                # update object pose
                indexes = {'pose.x': 0, 'pose.y': 1, 'pose.z': 2, 'pose.rx': 0, 'pose.ry': 1, 'pose.rz': 2}
                if 'r' in self.sweep['attribute']:
                    self.objects[step_uuid]['parameters']['rotation'][indexes[self.sweep['attribute']]] = value_array[ii]
                else:
                    self.objects[step_uuid]['parameters']['position'][indexes[self.sweep['attribute']]] = value_array[ii]

            elif sweep_target[0] == 'nf_src' and sweep_target[1] in self.elements:
                src_uuid = str(sweep_target[1])
                self.elements[src_uuid]['nf_source_data'][self.sweep['attribute']] = value_array[ii]

            elif sweep_target[0] == 'horn' and sweep_target[1] in self.elements:
                src_uuid = str(sweep_target[1])
                if self.sweep['attribute'] == "a_b":
                    self.elements[src_uuid]['parameters']['a'] = value_array[ii] * 1e-3
                    self.elements[src_uuid]['parameters']['b'] = value_array[ii] * 1e-3
                else:
                    self.elements[src_uuid]['parameters'][self.sweep['attribute']] = value_array[ii] * 1e-3

            previous_src = None

            for item_uuid in self.pipeline:
                if progress_callback:
                    progress_percent = (index_update * 100) // (num_iterations*num_steps)
                    progress_callback(progress_percent)
                    index_update += 1

                item = self.elements[item_uuid]
                if previous_src is None:
                    # build main source
                    self.build_source(item)

                    # simulate the main source
                    if 'nf_source_data' in item:
                        # it is a NearFieldSource -> need to build a GBE from points
                        # warning this will work only for plane
                        lambda_0 = 299792458. / (item['nf_source_data']['frequency_GHz'] * 1e9)
                        if 'sampling_step_lambda' not in item['nf_source_data']:
                            # projects written before commit 86a5d0d6
                            r_pts = item['nf_source_data']['points']
                            sampling_step = min(pdist(r_pts))
                            e = item['nf_source_data']['e_field']
                            hc = np.conj(item['nf_source_data']['h_field'])
                        else:
                            # first: resample the grid and field
                            r_pts_init = item['nf_source_data']['points']
                            sampling_step = item['nf_source_data']['sampling_step_lambda'] * lambda_0
                            grid_info = item['nf_source_data']['grid_info']
                            e_init = item['nf_source_data']['e_field']
                            h_init = item['nf_source_data']['h_field']
                            new_width = item['nf_source_data']['max_width_lambda'] * lambda_0
                            new_height = item['nf_source_data']['max_height_lambda'] * lambda_0
                            e, r_pts, grid = resample_field(e_init, grid_info, r_pts_init, new_width, new_height,
                                                            sampling_step)
                            h, _, _ = resample_field(h_init, grid_info, r_pts_init, new_width, new_height,
                                                     sampling_step)
                            hc = np.conj(h)

                        s = zeros_like(e, dtype=float)
                        s[:, 0] = real(e[:, 1] * hc[:, 2] - e[:, 2] * hc[:, 1])
                        s[:, 1] = real(e[:, 2] * hc[:, 0] - e[:, 0] * hc[:, 2])
                        s[:, 2] = real(e[:, 0] * hc[:, 1] - e[:, 1] * hc[:, 0])

                        # perform field expansion
                        # expand field from FEKO into several Gaussian beams (assume kappa = 1)
                        beams = field_expansion(field=e, poyinting=s, points=r_pts, freq=item['vsrc'].freq,
                                                w0=sampling_step, pw_threshold=1e-8)
                        item['vsrc'].init(beams=beams)
                        previous_src = item['vsrc']
                    elif 'horn' in item:
                        previous_src = item['horn']
                    else:
                        # Source already a VirtualSource
                        previous_src = item['vsrc']

                elif 'grid' in item:
                    grid, sampling_step = self.gbe_grid_from_parameters(self.objects[item_uuid],
                                                                        freq_GHz=self.frequency_GHz,
                                                                        objects=self.objects)
                    item['grid'] = grid

                    r_pts = grid.points
                    w0 = sampling_step * item['kappa']
                    # perform field expansion
                    beams = field_expansion(source=previous_src, points=r_pts, w0=w0, pw_threshold=1e-8)
                    item['vsrc'].init(beams=beams)
                    previous_src = item['vsrc']
                elif 'domain' in item:
                    # need to update the domain it has a mesh with a sweep (actually create it again)
                    if self.sweep['target'][0] == 'step' and self.sweep['target'][1] in item['meshes']:
                        self.add_gbt_domain(item_uuid, self.objects[item_uuid])
                        item = self.elements[item_uuid]

                    domain = item['domain']
                    # perform beam tracing
                    vsrc = domain.propagates(vsrc=previous_src)
                    item['vsrc'] = vsrc
                    previous_src = vsrc

            for req_uuid, req in self.requests.items():
                if not req['enabled']:
                    continue

                if req['type'] == RequestType.NEAR_FIELD.name and req['parameters'].get('domain', None) is not None:
                    try:
                        node = self.elements[req['parameters']['domain']]

                        u_range = self.results[req_uuid]['grid']['u_range']
                        v_range = self.results[req_uuid]['grid']['v_range']
                        n = self.results[req_uuid]['grid']['n']
                        plane = self.results[req_uuid]['grid']['plane']
                        plane_types = {'XY': PlaneType.XY, 'ZX': PlaneType.ZX, 'ZY': PlaneType.ZY}
                        grid = Grid(u_range, v_range, n=n, plane=plane_types[plane])

                        req_field = req['parameters'].get('field', None)
                        if req_field is None:
                            continue
                        if req_field == 'E':
                            e_field = node['vsrc'].e_field(grid.points)
                            self.results[req_uuid]['data'][ii] = e_field.numpy()
                        elif req_field == 'H':
                            h_field = node['vsrc'].h_field(grid.points)
                            self.results[req_uuid]['data'][ii] = h_field.numpy()

                    except Exception as e:
                        traceback.print_exception(e)
                        continue
                elif req['type'] == RequestType.FAR_FIELD.name:
                    horn_data = self.source_data['source']['parameters']

                    # Calculate and plot far field
                    norm_gain_db, gain_db, theta_deg, phi_deg = far_field_from_request(req['parameters'], horn_data)
                    self.results[req_uuid]['data'][ii] = {
                        'UdB': norm_gain_db,
                        'GdB': gain_db,
                        'theta_deg': theta_deg,
                        'phi_deg': phi_deg + horn_data['rot_z_deg'],
                    }
        if progress_callback:
            progress_callback(100)


def resample_field(field_data, init_grid, r_pts, new_width, new_height, new_step):
    """
    Resample with RegularGridInterpolator (2D equivalent of interp1d).

    field_data : array (N, 3) - original complex field
    nu0, nv0 : int - original grid size
    step0 : float - original step
    nu_new, nv_new : int - new grid size
    step_new : float - new step

    Returns: array (N_new, 3) - resampled field
    """
    x_min, x_max, nx = init_grid['x_range']
    y_min, y_max, ny = init_grid['y_range']
    z_min, z_max, nz = init_grid['z_range']
    centre = ((x_min + x_max) / 2, (y_min + y_max) / 2, (z_min + z_max) / 2)

    # New coordinates
    u_max_new = centre[0] + new_width/2
    v_max_new = centre[1] + new_height/2

    new_u_ = np.arange(0, u_max_new + new_step, new_step)
    new_u = np.hstack((-new_u_[::-1], new_u_[1:]))

    new_v_ = np.arange(0, v_max_new + new_step, new_step)
    new_v = np.hstack((-new_v_[::-1], new_v_[1:]))

    U, V = meshgrid(new_u, new_v)
    points_new_2d = np.column_stack([V.ravel(), U.ravel()])
    points_new = np.zeros((points_new_2d.shape[0], 3))
    new_shape = (new_v.shape[0], new_u.shape[0])

    if init_grid['z_range'][2] == 1 and r_pts[1, 1] - r_pts[0, 1] == 0:
        # XY or YX, suppose XY
        points_new[:, 0] = points_new_2d[:, 0]
        points_new[:, 1] = points_new_2d[:, 1]
        points_new[:, 2] = r_pts[0, 2]

        field_grid = field_data.reshape(ny, nx, 3)
        u0 = np.linspace(x_min, x_max, nx)
        v0 = np.linspace(y_min, y_max, ny)
    else:
        raise ReshapeAborted('Only XY grid is supported so far')

    points_new = points_new[:, [1, 0, 2]]  # for RegularGridInterpolator

    # Interpolation
    field_new = np.zeros((np.prod(new_shape), 3), dtype=complex)

    for i in range(3):  # Ex, Ey, Ez
        # Real part
        interp_real = RegularGridInterpolator((v0, u0), np.real(field_grid[:, :, i]), method='nearest',
                                              bounds_error=False, fill_value=None)
        # Imaginary part
        interp_imag = RegularGridInterpolator((v0, u0), np.imag(field_grid[:, :, i]), method='nearest',
                                              bounds_error=False, fill_value=None)

        field_new[:, i] = interp_real(points_new_2d) + 1j * interp_imag(points_new_2d)

    return field_new, points_new, (new_u, new_v, new_shape)
