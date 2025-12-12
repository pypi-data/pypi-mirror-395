import math
from copy import deepcopy

import numpy as np
from PySide6.QtGui import QPalette
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtWidgets import QApplication
from numpy import array

from scipy.spatial.transform import Rotation as R
from qosm.gui.managers.RequestManager import RequestType
from qosm.gui.view.opengl_viewer.gbtc import render_gbtc_port, render_gbtc_sample
from qosm.gui.view.opengl_viewer.objects import render_mesh, render_lens, render_grid
from qosm.gui.view.opengl_viewer.requests import render_far_field
from qosm.gui.view.opengl_viewer.sources import render_feko_grid, render_horn, render_gaussian_beam


class GLViewer(QOpenGLWidget):
    def __init__(self, parent=None, src_manager=None, obj_manager=None, req_manager=None):
        super().__init__(parent)
        # Managers
        self.source_manager = src_manager
        self.object_manager = obj_manager
        self.request_manager = req_manager

        self.angle_x = 30
        self.angle_y = -45
        self.zoom = -0.7
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.last_pos = None

        # Flag to display normal vectors
        self.show_normals = False

        # Projection mode
        self.is_perspective = True
        self.ortho_size = 2.0  # Taille de la vue orthogonale

        # Changed from list to dictionary with UUID keys
        self.objects = {}  # {uuid: object}
        self.filenames = {}  # {uuid: filename} for StepMesh objects
        self.selected_uuid = None
        self.setFocusPolicy(Qt.StrongFocus)

        # Object movement mode
        self.object_move_mode = False
        self.move_axis = None

        # Callbacks - now pass UUIDs instead of indices
        self.selection_callback = None
        self.log_callback = None

    def toggle_projection(self):
        """Switch between perspective and orthogonal projection"""
        self.is_perspective = not self.is_perspective
        self.update_projection()

        mode = "perspective" if self.is_perspective else "orthogonal"
        self.log_callback(f"Projection switched to {mode} mode")

        self.update()

    def update_projection(self):
        """Update projection matrix"""
        self.makeCurrent()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Calculer le ratio d'aspect
        aspect = self.width() / self.height() if self.height() != 0 else 1.0

        # Paramètres de clipping
        near_plane = 0.0001
        far_plane = 1000.0

        if self.is_perspective:
            # Projection perspective
            gluPerspective(45.0, aspect, near_plane, far_plane)
        else:
            # Projection orthogonale
            # Ajuster la taille orthogonale basée sur le zoom pour une transition fluide
            ortho_size = abs(self.zoom) * 0.5 if abs(self.zoom) > 0.1 else self.ortho_size
            glOrtho(-ortho_size * aspect, ortho_size * aspect,
                    -ortho_size, ortho_size,
                    near_plane, far_plane)

        glMatrixMode(GL_MODELVIEW)

    def fit_all_objects(self):
        """Adjust view to see all objects"""
        #todo à refaire !
        if not self.object_manager.objects:
            return

        return
        # Calculate bounding box of all objects
        min_bounds = np.array([float('inf'), float('inf'), float('inf')])
        max_bounds = np.array([float('-inf'), float('-inf'), float('-inf')])

        for _obj in self.object_manager.objects.values():
            pass

        # Calculate center and size
        center = (min_bounds + max_bounds) / 2
        size = np.max(max_bounds - min_bounds)

        if size == 0:  # Handle case with no objects or single point
            size = 1.0

        # Adjust view to center and zoom to fit
        self.pan_x = -center[0]
        self.pan_y = -center[1]
        # Improved zoom calculation based on object size
        self.zoom = -size * 1.5  # Better fit factor

        # Ensure zoom stays within reasonable bounds
        self.zoom = max(-500.0, min(-0.01, self.zoom))

        if self.log_callback:
            self.log_callback(f"View adjusted to fit all objects (size: {size:.2f})")

        self.update()

    def set_source_view(self):
        if self.log_callback:
            self.log_callback("View updated with active source")
        self.update()

    def set_view_xy(self):
        """Set view to XY plane (front view) - looking at xOy plane"""
        self.angle_x = 0
        self.angle_y = 0
        if self.log_callback:
            self.log_callback("View set to XY plane (front view)")
        self.update()

    def set_view_xz(self):
        """Set view to XZ plane (side view) - looking at xOz plane"""
        self.angle_x = 90
        self.angle_y = 90
        if self.log_callback:
            self.log_callback("View set to XZ plane (side view)")
        self.update()

    def set_view_yz(self):
        """Set view to YZ plane (top view) - looking at yOz plane"""
        self.angle_x = 0
        self.angle_y = 90
        if self.log_callback:
            self.log_callback("View set to YZ plane (top view)")
        self.update()

    def reset_view(self):
        """Reset view to default (XZ plane)"""
        self.angle_x = 90
        self.angle_y = 90
        self.zoom = -2.5
        self.pan_x = 0.0
        self.pan_y = 0.0
        if self.log_callback:
            self.log_callback("View reset to default (XZ plane)")
        self.update()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glClearColor(0.8, 0.8, 0.8, 1.0)

        light_pos = [0.0, 1.0, 1.0, 0.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

        distance = 100.0
        height = distance * 0.7071  # sin(45°) ≈ 0.7071

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        """glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Adjust near and far clipping planes for better zoom behavior
        # Near plane: very close to avoid clipping when zooming in
        # Far plane: very far to avoid clipping large scenes
        near_plane = 0.0001
        far_plane = 1000.0
        gluPerspective(45.0, w / h if h != 0 else 1.0, near_plane, far_plane)
        glMatrixMode(GL_MODELVIEW)"""
        self.update_projection()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setup_lighting()

        glLoadIdentity()

        # Apply view transformations
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

        self.draw_axes(length=0.1)

        # display the source if possible
        source = self.source_manager.get_active_source()
        if source:
            glPushMatrix()
            self.render_transform(source)
            if source['type'] == 'NearFieldSource':
                render_feko_grid(source['parameters']['grid_info'], picking_mode=False, selected_mode=False)
            elif source['type'] == 'Horn':
                render_horn(self, source['parameters'], picking_mode=False, selected_mode=False)
            elif source['type'] == 'GaussianBeam':
                render_gaussian_beam(self, source['parameters'], picking_mode=False, selected_mode=False)
            glPopMatrix()

        # get the selected domain (if any)
        selected_obj = self.object_manager.get_active_object()
        if selected_obj is not None and selected_obj['type'] == 'Domain':
            pre_selected = selected_obj['parameters']['meshes']
        else:
            pre_selected = []
        items = self.object_manager.get_ordered_objects() + self.request_manager.get_ordered_requests()
        for object_uuid, obj in items:
            if not obj:
                continue
            glPushMatrix()
            self.render_transform(obj)

            # Render object
            self.render_object(obj,
                               picking_mode=False,
                               selected_mode=(object_uuid == self.object_manager.active_object_uuid
                                              or object_uuid == self.request_manager.active_request_uuid
                                              or object_uuid in pre_selected),
                               domain_mode=object_uuid in pre_selected)

            glPopMatrix()

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Propriétés de la lumière
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  # Blanc
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Blanc
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])  # Ambiance faible

    @staticmethod
    def set_to_selected_color(alpha=0.8):
        palette = QApplication.palette()
        selection_bg = palette.color(QPalette.Highlight)
        r = selection_bg.red() / 255.0
        g = selection_bg.green() / 255.0
        b = selection_bg.blue() / 255.0
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [r, g, b, 1.0])
        glColor4f(r, g, b, alpha)

    def render_transform(self, obj):
        if obj is None:
            return

        """ Apply individual mesh position and rotation (Frame rotation matrix) """
        if 'position' in obj['parameters']:
            position = list(obj['parameters']['position'])
            rotation_deg = - array(obj['parameters'].get('rotation', [0, 0, 0]))

            reference_uuid = obj['parameters'].get('reference', None)
            if reference_uuid is not None:
                reference_pos = self.object_manager.get_object_pose(reference_uuid)[0]
                for i in range(3):
                    position[i] += reference_pos[i]

            glTranslatef(position[0], position[1], position[2])
            gl_matrix = np.eye(4)
            gl_matrix[:3, :3] = R.from_rotvec(rotation_deg, degrees=True).as_matrix()
            glMultMatrixf(gl_matrix.flatten())
        elif 'rot_z_deg' in obj['parameters']:
            rotation_deg = (0, 0, -obj['parameters'].get('rot_z_deg', 0))
            gl_matrix = np.eye(4)
            gl_matrix[:3, :3] = R.from_rotvec(rotation_deg, degrees=True).as_matrix()
            glMultMatrixf(gl_matrix.flatten())

    def render_object(self, obj, picking_mode=False, selected_mode=False, domain_mode=False):
        """Unified object rendering method"""
        if obj['type'] == 'StepMesh' or obj['type'] == 'ShapeMesh':
            render_mesh(self, obj, picking_mode, selected_mode, domain_mode)
        if obj['type'] == 'LensMesh':
            render_lens(self, obj['parameters'], picking_mode, selected_mode)
        elif obj['type'] in ['GBE', RequestType.NEAR_FIELD.name]:
            render_grid(self, obj, picking_mode, selected_mode)
        elif obj['type'] == RequestType.FAR_FIELD.name:
            render_far_field(self, obj, picking_mode, selected_mode)
        elif obj['type'] == 'GBTCPort':
            render_gbtc_port(self, obj, picking_mode, selected_mode)
        elif obj['type'] == 'GBTCSample':
            render_gbtc_sample(self, obj, picking_mode, selected_mode)

    def render_for_picking(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

        glDisable(GL_LIGHTING)
        glDisable(GL_DITHER)

        # Create mapping from color to UUID for picking
        self.picking_color_map = {}

        items = self.object_manager.get_ordered_objects() + self.request_manager.get_ordered_requests()
        for idx, (object_uuid, obj) in enumerate(items):
            glPushMatrix()
            self.render_transform(obj)

            # Set picking color using index (but map back to UUID)
            color_id = idx + 1
            r = ((color_id >> 16) & 0xFF) / 255.0
            g = ((color_id >> 8) & 0xFF) / 255.0
            b = (color_id & 0xFF) / 255.0
            glColor3f(r, g, b)

            # Store mapping for later retrieval
            self.picking_color_map[color_id] = object_uuid

            # Render object in picking mode
            self.render_object(obj, picking_mode=True)

            glPopMatrix()

        glEnable(GL_LIGHTING)
        glEnable(GL_DITHER)

    def pick_mesh_at(self, x, y):
        self.makeCurrent()
        self.render_for_picking()
        glFlush()

        pixel = glReadPixels(x, self.height() - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        rgb = np.frombuffer(pixel, dtype=np.uint8)
        if rgb.size < 3:
            return None

        r, g, b = rgb
        color_id = (r << 16) | (g << 8) | b

        # Map color back to UUID
        if color_id in self.picking_color_map:
            object_uuid = self.picking_color_map[color_id]
            if self.object_manager.exists(object_uuid):
                self.object_manager.set_active_object(object_uuid)
                display_name = self.object_manager.get_object_display_name(object_uuid)
            else:
                self.request_manager.set_active_request(object_uuid)
                display_name = self.request_manager.get_request_display_name(object_uuid)

            self.object_move_mode = False
            self.move_axis = None

            if self.log_callback:
                self.log_callback(f"Object selected: {display_name}")

            if self.selection_callback:
                self.selection_callback(object_uuid)
        else:
            if self.log_callback and (self.object_manager.get_active_object() is not None or
                    self.request_manager.get_active_request() is not None):
                self.log_callback("No object selected")

            self.object_manager.set_active_object(None)
            self.request_manager.set_active_request(None)
            self.object_move_mode = False
            self.move_axis = None

            if self.selection_callback:
                self.selection_callback(None)

        self.update()
        return object_uuid if color_id in self.picking_color_map else None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.position().toPoint()
            self.pick_mesh_at(pos.x(), pos.y())
        else:
            self.last_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.RightButton and self.last_pos:
            dx = event.position().x() - self.last_pos.x()
            dy = event.position().y() - self.last_pos.y()
            self.angle_x += dy * 0.5
            self.angle_y += dx * 0.5
            self.last_pos = event.position().toPoint()
            self.update()

    def wheelEvent(self, event):

        delta = event.angleDelta().y() / 120
        # Adjust zoom step based on current zoom level for smoother zooming
        zoom_step = abs(self.zoom) * 0.1 if abs(self.zoom) > 0.1 else 0.05
        self.zoom += delta * zoom_step

        # Limit zoom to prevent extreme values that could cause clipping issues
        self.zoom = max(-500.0, min(-0.01, self.zoom))

        # En mode orthogonale, mettre à jour la projection
        if not self.is_perspective:
            self.update_projection()

        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        angle_step = 5.0
        move_step = 0.001

        # Delete key to remove selected object
        if key == Qt.Key_Delete:
            if self.object_manager.active_object_uuid is not None:
                # Delegate to main window for deletion with confirmation
                if hasattr(self.parent(), 'delete_object'):
                    self.parent().delete_object()
            return

        # Movement mode management with G
        if key == Qt.Key_G:
            if self.object_move_mode:
                self.object_move_mode = False
                self.move_axis = None
                if self.log_callback:
                    self.log_callback("Movement mode: DISABLED")
            else:
                if (self.object_manager.active_object_uuid is not None
                        and self.object_manager.get_active_object()['type'] == 'StepMesh'):
                    self.object_move_mode = True
                    self.move_axis = None
                    if self.log_callback:
                        self.log_callback("Movement mode: ENABLED - Select an axis (X/Y/Z)")
            self.update()
            return

        # Axis selection in movement mode
        if self.object_move_mode and self.object_manager.active_object_uuid is not None:
            if key == Qt.Key_X:
                self.move_axis = 'x'
                if self.log_callback:
                    self.log_callback("Movement axis: X")
                self.update()
                return
            elif key == Qt.Key_Y:
                self.move_axis = 'y'
                if self.log_callback:
                    self.log_callback("Movement axis: Y")
                self.update()
                return
            elif key == Qt.Key_Z:
                self.move_axis = 'z'
                if self.log_callback:
                    self.log_callback("Movement axis: Z")
                self.update()
                return

        # CTRL + arrows for lateral view movement
        if modifiers & Qt.ControlModifier:
            if key == Qt.Key_Left:
                self.pan_x -= move_step
            elif key == Qt.Key_Right:
                self.pan_x += move_step
            elif key == Qt.Key_Up:
                self.pan_y += move_step
            elif key == Qt.Key_Down:
                self.pan_y -= move_step
            else:
                super().keyPressEvent(event)
                return

        # Object movement mode activated with axis selected
        elif self.object_move_mode and self.object_manager.active_object_uuid is not None and self.move_axis:
            position, rotation_deg = self.object_manager.get_object_pose()
            if key == Qt.Key_Left or key == Qt.Key_Down:
                if self.move_axis == 'x':
                    position[0] -= move_step
                elif self.move_axis == 'y':
                    position[1] -= move_step
                elif self.move_axis == 'z':
                    position[2] -= move_step
            elif key == Qt.Key_Right or key == Qt.Key_Up:
                if self.move_axis == 'x':
                    position[0] += move_step
                elif self.move_axis == 'y':
                    position[1] += move_step
                elif self.move_axis == 'z':
                    position[2] += move_step
            else:
                super().keyPressEvent(event)
                return

            # Update Frame with new position
            self.object_manager.update_object_pose(position, rotation_deg)
            self.selection_callback(self.object_manager.active_object_uuid)
            self.update()

        # View rotation mode (default behavior)
        else:
            if key == Qt.Key_Left:
                self.angle_y -= angle_step
            elif key == Qt.Key_Right:
                self.angle_y += angle_step
            elif key == Qt.Key_Up:
                self.angle_x -= angle_step
            elif key == Qt.Key_Down:
                self.angle_x += angle_step
            else:
                super().keyPressEvent(event)
                return

        self.update()

    @staticmethod
    def draw_axes(length=0.1):
        glDisable(GL_LIGHTING)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)
        glColor3f(0, .8, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        glEnd()
        glEnable(GL_LIGHTING)
