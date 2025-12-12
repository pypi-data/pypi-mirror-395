from copy import deepcopy

from OpenGL.GL import *
from qosm import Vec3
import math

from qosm.gui.view.opengl_viewer.objects import render_lens
from qosm.propagation.GBTC import get_port_pointing_direction


def render_gbtc_port(viewer, gbtc_port, picking_mode=False, selected_mode=False):
    """
    Render a GBTC Port object with lens, beam waist disk, and bounding box

    Args:
        viewer (QGLViewer): the QGLViewer object
        gbtc_port: Dictionary containing GBTC port parameters
        picking_mode: Boolean, if True render for object picking
        selected_mode: Boolean, if True render with selected colors
    """
    if gbtc_port is None:
        return

    params = gbtc_port['parameters']

    # Extract beam parameters
    beam = params['beam']
    w0 = beam['w0']
    z0 = beam['z0']

    # Extract lenses - use first lens for main rendering
    lenses = params['lenses']
    if not lenses:
        return  # No lenses to render

    lens = lenses[0]  # Use first lens for main rendering
    distance_from_previous = lens['distance_from_previous']
    distance_sample_output_lens = params['distance_sample_output_lens']

    samples = viewer.object_manager.get_objects_by_type()['GBTCSample']
    if len(samples) > 0:
        sample = samples[0][1]
        sample_attitude = tuple(sample['parameters']['rotation'])
    else:
        sample_attitude = (0, 0, 0)

    _port = {
        'distance_lens_sample': distance_sample_output_lens,
        'lenses': lenses,
    }
    if not params['follow_sample']:
        _port['attitude_deg'] = params['attitude']
    if 'offset' in params:
        _port['offset'] = params['offset']

    # Calculate position and attitude
    _, pos_port, att_port = get_port_pointing_direction(_port, sample_attitude)

    # Bounding box includes waist disk and lenses
    margin = 0.002  # 5mm margin
    max_radius = 0
    box_max_z = margin
    for lens in _port['lenses']:
        box_max_z += lens['thickness'] + lens['distance_from_previous']
        max_radius = max(max_radius, lens['radius'])
    box_min_x = -max(w0, max_radius/2) - margin
    box_max_x = max(w0, max_radius/2) + margin
    box_min_y = -max(w0, max_radius/2) - margin
    box_max_y = max(w0, max_radius/2) + margin
    box_min_z = 0

    empty_obj = {
        'parameters': {
            'position': pos_port.numpy(),
            'rotation': att_port.numpy()
        }
    }
    glPushMatrix()
    viewer.render_transform(empty_obj)

    if not picking_mode:

        # Render lens at the correct position
        z_pos = 0
        for lens in lenses:
            z_pos += lens['distance_from_previous']
            glPushMatrix()
            glTranslatef(0, 0, z_pos)
            render_lens(viewer, lens, picking_mode, selected_mode, show_lines=False)
            glPopMatrix()
            z_pos += lens['thickness']

        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)

        # Add beam waist disk
        glColor4f(0.2, 0.8, 0.2, 0.7)

        segments = 32
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, z0)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            x = w0 * math.cos(angle)
            y = w0 * math.sin(angle)
            glVertex3f(x, y, z0)
        glEnd()

        # Render circle outline for better visibility
        glColor3f(0.1, 0.1, 0.1)  # Dark outline
        glLineWidth(2.0)

        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            x = w0 * math.cos(angle)
            y = w0 * math.sin(angle)
            glVertex3f(x, y, z0)
        glEnd()

        # show link to port origin
        if selected_mode:
            viewer.set_to_selected_color(alpha=0.9)
        else:
            glColor4f(0.4, 0.2, 0.4, 0.5)

        glLineWidth(2.0)
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0x00FF)  # Pattern: 0x00FF
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, distance_from_previous)
        glEnd()
        glDisable(GL_LINE_STIPPLE)

        # Render wireframe box in normal mode, solid faces in picking mode
        if selected_mode:
            viewer.set_to_selected_color(alpha=0.9)
        else:
            glColor4f(1.0, 0.0, 1.0, 0.1)  # Magenta with transparency

        glLineWidth(1.2)
        glBegin(GL_LINES)

        # Front face edges (Z = max)
        glVertex3f(box_min_x, box_min_y, box_max_z)
        glVertex3f(box_max_x, box_min_y, box_max_z)

        glVertex3f(box_max_x, box_min_y, box_max_z)
        glVertex3f(box_max_x, box_max_y, box_max_z)

        glVertex3f(box_max_x, box_max_y, box_max_z)
        glVertex3f(box_min_x, box_max_y, box_max_z)

        glVertex3f(box_min_x, box_max_y, box_max_z)
        glVertex3f(box_min_x, box_min_y, box_max_z)

        # Back face edges (Z = min)
        glVertex3f(box_min_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_min_y, box_min_z)

        glVertex3f(box_max_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_max_y, box_min_z)

        glVertex3f(box_max_x, box_max_y, box_min_z)
        glVertex3f(box_min_x, box_max_y, box_min_z)

        glVertex3f(box_min_x, box_max_y, box_min_z)
        glVertex3f(box_min_x, box_min_y, box_min_z)

        # Connecting edges between front and back faces
        glVertex3f(box_min_x, box_min_y, box_min_z)
        glVertex3f(box_min_x, box_min_y, box_max_z)

        glVertex3f(box_max_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_min_y, box_max_z)

        glVertex3f(box_max_x, box_max_y, box_min_z)
        glVertex3f(box_max_x, box_max_y, box_max_z)

        glVertex3f(box_min_x, box_max_y, box_min_z)
        glVertex3f(box_min_x, box_max_y, box_max_z)

        glEnd()

        glEnable(GL_LIGHTING)
        glDisable(GL_BLEND)
    else:
        # Picking mode: render solid triangular faces for collision detection
        glBegin(GL_TRIANGLES)

        # Front face (Z = max) - 2 triangles
        glVertex3f(box_min_x, box_min_y, box_max_z)
        glVertex3f(box_max_x, box_min_y, box_max_z)
        glVertex3f(box_max_x, box_max_y, box_max_z)

        glVertex3f(box_min_x, box_min_y, box_max_z)
        glVertex3f(box_max_x, box_max_y, box_max_z)
        glVertex3f(box_min_x, box_max_y, box_max_z)

        # Back face (Z = min) - 2 triangles
        glVertex3f(box_min_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_max_y, box_min_z)
        glVertex3f(box_max_x, box_min_y, box_min_z)

        glVertex3f(box_min_x, box_min_y, box_min_z)
        glVertex3f(box_min_x, box_max_y, box_min_z)
        glVertex3f(box_max_x, box_max_y, box_min_z)

        # Right face (X = max) - 2 triangles
        glVertex3f(box_max_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_max_y, box_min_z)
        glVertex3f(box_max_x, box_max_y, box_max_z)

        glVertex3f(box_max_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_max_y, box_max_z)
        glVertex3f(box_max_x, box_min_y, box_max_z)

        # Left face (X = min) - 2 triangles
        glVertex3f(box_min_x, box_min_y, box_min_z)
        glVertex3f(box_min_x, box_max_y, box_max_z)
        glVertex3f(box_min_x, box_max_y, box_min_z)

        glVertex3f(box_min_x, box_min_y, box_min_z)
        glVertex3f(box_min_x, box_min_y, box_max_z)
        glVertex3f(box_min_x, box_max_y, box_max_z)

        # Top face (Y = max) - 2 triangles
        glVertex3f(box_min_x, box_max_y, box_min_z)
        glVertex3f(box_min_x, box_max_y, box_max_z)
        glVertex3f(box_max_x, box_max_y, box_max_z)

        glVertex3f(box_min_x, box_max_y, box_min_z)
        glVertex3f(box_max_x, box_max_y, box_max_z)
        glVertex3f(box_max_x, box_max_y, box_min_z)

        # Bottom face (Y = min) - 2 triangles
        glVertex3f(box_min_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_min_y, box_max_z)
        glVertex3f(box_min_x, box_min_y, box_max_z)

        glVertex3f(box_min_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_min_y, box_min_z)
        glVertex3f(box_max_x, box_min_y, box_max_z)

        glEnd()

    glPopMatrix()


def render_gbtc_sample(viewer, gbtc_sample, picking_mode=False, selected_mode=False):
    """
    Render a GBTC Sample object showing layers as planes

    Args:
        viewer: OpenGL viewer
        gbtc_sample: Dictionary containing GBTC sample parameters
        picking_mode: Boolean, if True render for object picking
        selected_mode: Boolean, if True render with selected colors
    """
    if gbtc_sample is None:
        return

    params = gbtc_sample['parameters']

    # Extract sample parameters
    mut = params.get('mut', [])  # List of layers
    max_plane_size = 0.1  # Maximum width/height = 0.1m

    if not mut:
        return  # No layers to render

    empty_obj = {
        'parameters': {
            'position': params.get('offset', (0, 0, 0)),  # No additional translation
            'rotation': params['rotation']
        }
    }
    glPushMatrix()
    viewer.render_transform(empty_obj)

    # Calculate total thickness
    total_thickness = sum(layer.get('thickness', 0.001) for layer in mut)

    # Start position (layers stack from z=0)
    current_z = 0.0

    if not picking_mode:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_LIGHTING)

    _mut = deepcopy(mut)
    _mut.append({})
    # Render each layer as a plane
    for i, layer in enumerate(_mut):
        # Position this layer
        layer_z = current_z  # Center of layer

        # Set color based on layer index and selection
        if not picking_mode:
            if selected_mode:
                viewer.set_to_selected_color()
            else:
                # Different color for each layer (cycling through colors)
                colors = [
                    (0.8, 0.2, 0.2, 0.6),  # Red
                    (0.2, 0.8, 0.2, 0.6),  # Green
                    (0.2, 0.2, 0.8, 0.6),  # Blue
                    (0.8, 0.8, 0.2, 0.6),  # Yellow
                    (0.8, 0.2, 0.8, 0.6),  # Magenta
                    (0.2, 0.8, 0.8, 0.6),  # Cyan
                ]
                color = colors[i % len(colors)] if i < len(_mut) -1 else (0.5, 0.5, 0.5, 0.6)
                glColor4f(*color)

        # Render plane
        half_size = max_plane_size / 2

        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)

        # Layer plane (horizontal)
        glVertex3f(-half_size, -half_size, layer_z)
        glVertex3f(half_size, -half_size, layer_z)
        glVertex3f(half_size, half_size, layer_z)
        glVertex3f(-half_size, half_size, layer_z)

        glEnd()

        # Draw outline for better visibility (only in normal mode)
        if not picking_mode and selected_mode:
            glColor3f(0.8, 0.5, 0.4)  # Dark outline
            glLineWidth(2.0)
            glBegin(GL_LINE_LOOP)
            glVertex3f(-half_size, -half_size, layer_z)
            glVertex3f(half_size, -half_size, layer_z)
            glVertex3f(half_size, half_size, layer_z)
            glVertex3f(-half_size, half_size, layer_z)
            glEnd()

        # Move to next layer
        thickness = layer.get('thickness', 0.)  # Default 1mm
        current_z += thickness

    # Draw side edges to show layer structure (only in normal mode)
    if not picking_mode:
        glColor4f(0.5, 0.5, 0.5, 0.8)  # Gray edges
        glLineWidth(1.0)
        glBegin(GL_LINES)

        # Vertical edges at corners
        half_size = max_plane_size / 2
        corners = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]

        for x, y in corners:
            glVertex3f(x, y, 0)
            glVertex3f(x, y, total_thickness)

        glEnd()

    glPopMatrix()

    # Restore OpenGL state
    if not picking_mode:
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)