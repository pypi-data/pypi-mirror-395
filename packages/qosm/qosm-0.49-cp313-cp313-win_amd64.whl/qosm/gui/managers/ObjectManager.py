import os
import uuid
from enum import Enum
from os.path import exists

import numpy as np
from numpy import mean, array
from qosm.items.StepMesh import StepMesh
from qosm.items.SlabMesh import SlabMesh
from qosm import Grid, PlaneType, Frame, Vec3, Domain

from qosm.gui.managers import SimulationManager


class ObjectType(Enum):
    DOMAIN = 'GBT Domain'
    GBE = 'GBE Grid'
    STEP_MESH = 'StepMesh'
    SHAPE_MESH = 'ShapeMesh'
    LENS_MESH = 'LensMesh'
    GBTC_PORT = 'GBTC Port',
    GBTC_SAMPLE = 'GBTC Sample',


class SourceType(Enum):
    FEKO_SOURCE = 'FekoSource'
    HORN = 'Horn'
    GAUSSIAN_BEAM = 'Gaussian Beam'


class ObjectManager:
    """Gestionnaire des sources dans l'application principale"""

    def __init__(self):
        self.objects = {}
        self.active_object_uuid = None
        self.counters = {
            'GBE': 0,
            'ShapeMesh': 0,
            'LensMesh': 0,
            'Domain': 0,
            'GBTCPort': 0
        }

    @staticmethod
    def get_object_type_name(obj):
        """Return the type name of an object"""
        if not obj:
            return 'Unknown'
        return obj.get('type', 'Unknown')

    def get_object_display_name(self, object_uuid=None):
        if not object_uuid:
            object_uuid = self.active_object_uuid

        if object_uuid in self.objects:
            return self.objects[object_uuid]['name']
        return None

    def exists(self, object_uuid = None) -> bool:
        if not object_uuid:
            object_uuid = self.active_object_uuid
        return object_uuid is not None and object_uuid in self.objects

    def get(self, object_uuid: str):
        """Return the active object"""
        if self.exists(object_uuid):
            return self.objects[object_uuid]
        return None

    def get_active_object(self):
        """Return the active object"""
        if self.exists():
            return self.objects[self.active_object_uuid]
        return None


    def add_object(self, obj_type: str, params: dict = None) -> str | None:
        """Add a new item"""
        try:
            _uuid = str(uuid.uuid4())

            if obj_type == 'StepMesh':
                _name = os.path.basename(params['filepath'])
            if obj_type == 'GBTCSample':
                _name = 'GBTC Sample'
            else:
                # For non-StepMesh objects, use type name with a counter
                # Count objects of the same type that appear before this one in the dictionary
                if obj_type in self.counters:
                    self.counters[obj_type] += 1
                    count = self.counters[obj_type]
                else:
                    self.counters[obj_type] = 1
                    count = 1
                _name = f"{obj_type}_{count}"

            self.objects[_uuid] = {
                'name': _name,
                'type': obj_type,
                'parameters': params
            }
            if self.active_object_uuid is None:
                self.active_object_uuid = _uuid
            return _uuid
        except Exception as e:
            print(f"Error adding object: {e}")
            return None

    def remove_object(self, object_uuid = None) -> bool:
        if not object_uuid:
            object_uuid = self.active_object_uuid

        """Remove an object"""
        try:
            if object_uuid in self.objects:
                # Remove from objects dictionary
                self.objects.pop(object_uuid)

                return True

        except Exception as e:
            print(f"Error removing object: {e}")

        return False

    def set_active_object(self, object_uuid) -> bool:
        """Set the active object"""
        if self.exists(object_uuid):
            self.active_object_uuid = object_uuid
            return True
        return False

    def set_object_name(self, new_name, object_uuid=None) -> bool:
        if not object_uuid:
            object_uuid = self.active_object_uuid

        if not self.exists(object_uuid):
            return False

        self.objects[object_uuid]['name'] = new_name
        return True

    def get_ordered_objects(self):
        """Return objects in consistent order for rendering"""
        return list(self.objects.items())

    def get_objects_by_type(self):
        """Return objects grouped by type"""
        objects_by_type = {
            "StepMesh": [],
            "ShapeMesh": [],
            "LensMesh": [],
            "GBE": [],
            "Domain": [],
            "GBTCPort": [],
            "GBTCSample": []
        }

        for object_uuid, obj in self.objects.items():
            type_name = self.get_object_type_name(obj)
            if type_name in objects_by_type:
                objects_by_type[type_name].append((object_uuid, obj))

        return objects_by_type

    def create_step(self, step_params) -> str | None:
        try:
            if not exists(step_params['filepath']):
                raise FileNotFoundError('File "{}" not found'.format(step_params['filepath']))
            
            m = StepMesh()
            element_size = step_params.get('element_size', 4)
            scale = step_params.get('scale', 1e-3)
            m.load_step(step_params['filepath'], element_size=element_size, scale=scale)

            params = {
                'vertices': m.vertices,
                'normals': m.normals,
                'triangles': m.triangles,
                'position': array(step_params['position']),
                'rotation': array(step_params['rotation']),
                'element_size': element_size,
                'scale': scale,
                'filepath': step_params['filepath'],
                'medium': step_params['medium']
            }

            # Generate UUID for the new mesh
            mesh_uuid = self.add_object('StepMesh', params=params)

            return mesh_uuid

        except Exception as e:
            print(e)
            return None

    def create_shape(self, shape_params, update_selected=False) -> str | None:
        try:
            m = SlabMesh(None)
            element_size = shape_params['element_size'] * 1e-3
            shape_type = shape_params['shape_type']
            if shape_type == 'sphere':
                shape_size = shape_params['shape_params']
                shape_size = (shape_size[0], shape_size[1] * np.pi / 180., shape_size[2] * np.pi / 180.,
                              shape_size[3] * np.pi / 180.)
            else:
                shape_size = tuple([el for el in shape_params['shape_params']])

            flip_normal = shape_type == 'disk' or shape_type == 'rect'
            m.load(element_size=element_size, shape=shape_type, size=shape_size)

            params = shape_params
            params['vertices'] = m.vertices
            params['normals'] = m.normals
            params['triangles'] = m.triangles

            # Generate UUID for the new mesh
            if update_selected:
                mesh_uuid = self.active_object_uuid
                self.objects[mesh_uuid]['parameters'] = params
            else:
                mesh_uuid = self.add_object('ShapeMesh', params=params)

            return mesh_uuid

        except Exception as e:
            return None

    def create_lens(self, shape_params) -> str | None:
        try:
            # Generate UUID for the new mesh
            mesh_uuid = self.add_object('LensMesh', params=shape_params)
            return mesh_uuid

        except Exception as e:
            return None

    def update_step(self, step_params, object_uuid = None):
        """Update mesh transformation and its Frame"""
        if not object_uuid:
            object_uuid = self.active_object_uuid

        if not exists(step_params['filepath']):
            raise FileNotFoundError('File "{}" not found'.format(step_params['filepath']))

        scale = step_params.get('scale', 1e-3)
        if step_params['filepath'] != self.objects[object_uuid]['parameters']['filepath'] \
                or step_params['element_size'] != self.objects[object_uuid]['parameters']['element_size']:
            # reload the whole object
            m = StepMesh()
            m.load_step(step_params['filepath'], element_size=step_params['element_size'], scale=scale)

            self.objects[object_uuid]['parameters'] = {
                'filepath': step_params['filepath'],
                'vertices': m.vertices,
                'normals': m.normals,
                'triangles': m.triangles,
                'element_size': step_params['element_size'],
                'scale': scale,
                'position': array(step_params['position']),
                'rotation': array(step_params['rotation']),
                'medium': step_params['medium']
            }

        self.objects[object_uuid]['parameters']['position'] = array(step_params['position'])
        self.objects[object_uuid]['parameters']['rotation'] = array(step_params['rotation'])
        self.objects[object_uuid]['parameters']['medium'] = step_params['medium']

        self.update_linked_grids()

    def update_object_pose(self, position, rotation_deg, object_uuid = None):
        """Update mesh transformation and its Frame"""
        if not object_uuid:
            object_uuid = self.active_object_uuid

        obj = self.get(object_uuid)
        obj['parameters']['position'] = array(position)
        obj['parameters']['rotation'] = array(rotation_deg)

        self.update_linked_grids()

    def get_object_pose(self, object_uuid = None):
        """Return position and rotation in degrees of selected object"""
        if not object_uuid:
            object_uuid = self.active_object_uuid

        obj = self.get(object_uuid)

        return obj['parameters'].get('position', None), obj['parameters'].get('rotation', None)

    def create_gbe_grid(self, grid_params) -> str | None:
        try:
            u_range = [grid_params['u_range'][0], grid_params['u_range'][1]]
            v_range = [grid_params['v_range'][0], grid_params['v_range'][1]]
            centre = (np.sum(u_range) / 2, np.sum(v_range) / 2, grid_params['n'])

            # Generate UUID for the new grid
            return self.add_object('GBE', params={
                'size_u': grid_params['u_range'][1] - grid_params['u_range'][0],
                'size_v': grid_params['v_range'][1] - grid_params['v_range'][0],
                'sampling_step': grid_params['sampling_step'],
                'sampling_unit': grid_params['sampling_unit'],
                'kappa': grid_params['kappa'],
                'position': centre,
                'reference': None,
                'plane': grid_params['plane'],
                'source': grid_params['source']
            })

        except Exception as e:
            print(e)
            return None

    def create_gbt_domain(self, domain_params) -> str | None:
        try:
            # Generate UUID for the new domain
            return self.add_object('Domain', params=domain_params)
        except Exception as e:
            return None

    def create_gbtc_port(self, gbtc_params) -> str | None:
        try:
            # Generate UUID for the new domain
            return self.add_object('GBTCPort', params=gbtc_params)
        except Exception as e:
            return None

    def create_gbtc_mlsample(self, gbtc_params) -> str | None:
        try:
            # Generate UUID for the new domain
            return self.add_object('GBTCSample', params=gbtc_params)
        except Exception as e:
            return None

    def update_gbe_grid(self, grid_params = None, object_uuid = None):
        """Update grid parameters"""
        if not object_uuid:
            object_uuid = self.active_object_uuid

        if object_uuid not in self.objects:
            return False

        obj = self.objects[object_uuid]
        try:
            if grid_params is not None:
                obj['parameters'] = grid_params
            return True

        except Exception as e:
            print(e)
            return False

    def update_gbt_domain(self, domain_params = None, object_uuid = None):
        """Update domain parameters"""
        if not object_uuid:
            object_uuid = self.active_object_uuid

        if object_uuid not in self.objects:
            return False

        obj = self.objects[object_uuid]
        try:
            if domain_params is not None:
                obj['parameters'] = domain_params
            return True

        except Exception as e:
            print(e)
            return False

    def get_gbe_points(self, object_uuid = None):
        """Get grid points"""
        if not object_uuid:
            object_uuid = self.active_object_uuid

        if not object_uuid:
            return []

        return SimulationManager.gbe_grid_from_parameters(self.get(object_uuid)).points.numpy()

    def get_domain_mesh_names(self, object_uuid = None):
        """Get grid points"""
        if not object_uuid:
            object_uuid = self.active_object_uuid

        obj = self.get(object_uuid)
        if not obj:
            return []

        names = []
        for mesh_uuid in obj['parameters'].get('meshes', []):
            names.append(self.get(mesh_uuid)['name'])
        return names

    def update_linked_grids(self):
        pass
