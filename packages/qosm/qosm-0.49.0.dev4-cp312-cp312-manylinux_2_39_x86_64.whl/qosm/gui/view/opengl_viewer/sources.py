import math

from OpenGL.GL import *

def render_feko_grid(grid_info, picking_mode=False, selected_mode=False):
    if not picking_mode:
        # Enable transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Enable depth testing for 3D masking
        glEnable(GL_DEPTH_TEST)
        # Disable lighting to avoid shading
        glDisable(GL_LIGHTING)

    # Determine plane type and create corners
    if grid_info['y_range'][2] == 1:
        # ZX plane (Y constant)
        y = grid_info['y_range'][0]
        corners = [
            [grid_info['x_range'][0], y, grid_info['z_range'][0]],
            [grid_info['x_range'][1], y, grid_info['z_range'][0]],
            [grid_info['x_range'][1], y, grid_info['z_range'][1]],
            [grid_info['x_range'][0], y, grid_info['z_range'][1]]
        ]
        normal = [0, 1, 0]
    elif grid_info['x_range'][2] == 1:
        # ZY plane (X constant)
        x = grid_info['x_range'][0]
        corners = [
            [x, grid_info['y_range'][0], grid_info['z_range'][0]],
            [x, grid_info['y_range'][1], grid_info['z_range'][0]],
            [x, grid_info['y_range'][1], grid_info['z_range'][1]],
            [x, grid_info['y_range'][0], grid_info['z_range'][1]]
        ]
        normal = [1, 0, 0]
    else:
        # XY plane (Z constant)
        z = grid_info['z_range'][0]
        corners = [
            [grid_info['x_range'][0], grid_info['y_range'][0], z],
            [grid_info['x_range'][1], grid_info['y_range'][0], z],
            [grid_info['x_range'][1], grid_info['y_range'][1], z],
            [grid_info['x_range'][0], grid_info['x_range'][1], z]
        ]
        normal = [0, 0, 1]

    # Draw semi-transparent plane
    glColor4f(0.1, 0.3, 0.6, 0.9)

    glBegin(GL_QUADS)
    glNormal3f(*normal)
    for corner in corners:
        glVertex3f(*corner)
    glEnd()

    # Optional: Draw grid lines for better visualization
    if not picking_mode:
        if selected_mode:
            glColor4f(0.8, 0.3, 0.1, 0.7)  # Darker orange for lines
        else:
            glColor4f(0.1, 0.1, 0.5, 0.7)  # Darker blue for lines

        glLineWidth(1.0)
        # You could add grid line drawing here if needed

        # Draw border
        glBegin(GL_LINE_LOOP)
        for corner in corners:
            glVertex3f(*corner)
        glEnd()

    # Restore OpenGL state
    if not picking_mode:
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

def render_gaussian_beam(viewer, beam_data, picking_mode=False, selected_mode=False):
    """
    Render a Gaussian Beam source as a disk aperture with polarization arrow
    Note: Center is at (0, 0, z0)

    Args:
        viewer: OpenGL viewer
        beam_data: Dictionary containing beam parameters
        picking_mode: Boolean, if True render for object picking
        selected_mode: Boolean, if True render with selected colors
    """
    if beam_data is None:
        return

    if not picking_mode:
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

    # Extract beam parameters
    w0 = beam_data['w0'] * 1e-3  # Beam waist radius
    z0 = beam_data['z0'] * 1e-3  # Z-offset
    polarization = beam_data['polarization']

    # Set colors
    if not picking_mode:
        if selected_mode:
            viewer.set_to_selected_color()
        else:
            if beam_data.get('enabled', True):
                glColor3f(0.2, 0.8, 0.2)  # Green color for Gaussian beam
            else:
                glColor3f(0.5, 0.5, 0.5)  # Grey when disabled

    # Render disk aperture directly at z0
    num_segments = 32  # Number of segments for circle

    # Render filled disk
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 0, 1)

    # Center vertex
    glVertex3f(0, 0, z0)

    # Circle vertices
    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = w0 * math.cos(angle)
        y = w0 * math.sin(angle)
        glVertex3f(x, y, z0)

    glEnd()

    # Render circle outline for better visibility
    if not picking_mode:
        current_color = glGetFloatv(GL_CURRENT_COLOR)
        glColor3f(0.1, 0.1, 0.1)  # Dark outline
        glLineWidth(2.0)

        glBegin(GL_LINE_LOOP)
        for i in range(num_segments):
            angle = 2.0 * math.pi * i / num_segments
            x = w0 * math.cos(angle)
            y = w0 * math.sin(angle)
            glVertex3f(x, y, z0)
        glEnd()

        # Restore original color for arrow
        glColor4fv(current_color)

        # Render polarization arrow
        arrow_length = 1.5 * w0

        # Normalize polarization vector (use only x,y components for 2D arrow)
        pol_x = polarization['x']
        pol_y = polarization['y']

        # Normalize to arrow length
        pol_magnitude = math.sqrt(pol_x * pol_x + pol_y * pol_y)
        pol_x = (pol_x / pol_magnitude) * arrow_length
        pol_y = (pol_y / pol_magnitude) * arrow_length

        # Set arrow color (contrasting with beam color)
        glColor3f(0.8, 0.2, 0.2)  # Red arrow
        glLineWidth(3.0)

        # Draw main arrow line
        glBegin(GL_LINES)
        glVertex3f(0, 0, z0 - 0.0001)  # Slightly above disk to avoid z-fighting
        glVertex3f(pol_x, pol_y, z0 - 0.0001)
        glEnd()

        # Draw arrowhead
        arrowhead_length = 0.2 * arrow_length
        arrowhead_angle = math.pi / 6  # 30 degrees

        # Calculate arrowhead direction (opposite to arrow direction)
        arrow_angle = math.atan2(pol_y, pol_x)

        # Arrowhead points
        head1_angle = arrow_angle + math.pi - arrowhead_angle
        head2_angle = arrow_angle + math.pi + arrowhead_angle

        head1_x = pol_x + arrowhead_length * math.cos(head1_angle)
        head1_y = pol_y + arrowhead_length * math.sin(head1_angle)

        head2_x = pol_x + arrowhead_length * math.cos(head2_angle)
        head2_y = pol_y + arrowhead_length * math.sin(head2_angle)

        glBegin(GL_LINES)
        # First arrowhead line
        glVertex3f(pol_x, pol_y, z0 - 0.0001)
        glVertex3f(head1_x, head1_y, z0 - 0.0001)

        # Second arrowhead line
        glVertex3f(pol_x, pol_y, z0 - 0.0001)
        glVertex3f(head2_x, head2_y, z0 - 0.0001)
        glEnd()

    # Restore OpenGL state
    if not picking_mode:
        glEnable(GL_LIGHTING)

def render_horn(viewer, horn_data, picking_mode=False, selected_mode=False):
    """
    Render a Horn object as a pyramid structure
    Note: Base (aperture) center is always positioned at the origin (0,0,0)

    Args:
        viewer: OpenGL viewer
        horn_data: Dictionary containing horn parameters
        picking_mode: Boolean, if True render for object picking
        selected_mode: Boolean, if True render with selected colors
    """
    if horn_data is None:
        return

    if not picking_mode:
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

    # Extract horn parameters
    aperture_a = horn_data.get('a', 0.015)  # Aperture width
    aperture_b = horn_data.get('b', 0.015)  # Aperture height
    length = horn_data.get('length', 0.01)  # Horn length

    # Set colors
    if not picking_mode:
        if selected_mode:
            viewer.set_to_selected_color()
        else:
            if horn_data.get('enabled', True):
                glColor3f(0.8, 0.6, 0.2)  # Golden color
            else:
                glColor3f(0.5, 0.5, 0.5)  # Grey when disabled

    # Define pyramid
    half_a = aperture_a / 2
    half_b = aperture_b / 2

    # Base corners at z=0 (aperture)
    base_corners = [
        (-half_a, -half_b, 0),  # Bottom-left
        (half_a, -half_b, 0),  # Bottom-right
        (half_a, half_b, 0),  # Top-right
        (-half_a, half_b, 0)  # Top-left
    ]

    # Apex point at z=-length
    apex = (0, 0, -length)

    # Render pyramid faces
    glBegin(GL_TRIANGLES)

    # Base face (at z=0)
    glNormal3f(0, 0, 1)
    glVertex3f(*base_corners[0])
    glVertex3f(*base_corners[1])
    glVertex3f(*base_corners[2])

    glVertex3f(*base_corners[0])
    glVertex3f(*base_corners[2])
    glVertex3f(*base_corners[3])

    # Side faces (triangles from base edges to apex)
    # Bottom face
    glNormal3f(0, -1, 0)
    glVertex3f(*base_corners[0])
    glVertex3f(*base_corners[1])
    glVertex3f(*apex)

    # Right face
    glNormal3f(1, 0, 0)
    glVertex3f(*base_corners[1])
    glVertex3f(*base_corners[2])
    glVertex3f(*apex)

    # Top face
    glNormal3f(0, 1, 0)
    glVertex3f(*base_corners[2])
    glVertex3f(*base_corners[3])
    glVertex3f(*apex)

    # Left face
    glNormal3f(-1, 0, 0)
    glVertex3f(*base_corners[3])
    glVertex3f(*base_corners[0])
    glVertex3f(*apex)

    glEnd()

    # Draw edges for better visibility
    if not picking_mode:
        glColor3f(0.2, 0.2, 0.2)  # Dark edges
        glLineWidth(2.0)

        # Base edges
        glBegin(GL_LINE_LOOP)
        for corner in base_corners:
            glVertex3f(*corner)
        glEnd()

        # Edges from base to apex
        glBegin(GL_LINES)
        for corner in base_corners:
            glVertex3f(*corner)
            glVertex3f(*apex)
        glEnd()

    # Restore OpenGL state
    if not picking_mode:
        glEnable(GL_LIGHTING)