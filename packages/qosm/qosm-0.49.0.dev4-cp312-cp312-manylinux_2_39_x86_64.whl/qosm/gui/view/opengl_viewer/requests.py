import math
from OpenGL.GL import *
from numpy import arange


def render_far_field(viewer, ff_request, picking_mode=False, selected_mode=False):
    """Render a Far Field Request object as a portion of circle (arc)"""
    if ff_request is None:
        return

    if not picking_mode:
        # Enable transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Enable depth testing for 3D masking
        glEnable(GL_DEPTH_TEST)

        # Disable lighting to avoid shading
        glDisable(GL_LIGHTING)

        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1.0, 1.0)

        # Get parameters
    params = ff_request['parameters']
    phi = math.radians(params['phi'])  # Cut-plane angle (rotation around z-axis)
    theta_start = math.radians(params['theta_range'][0])  # Start angle
    theta_stop = math.radians(params['theta_range'][1])  # Stop angle
    theta_step = math.radians(params['theta_range'][2])  # Step angle

    # Arc radius for visualization (adjust as needed)
    radius = 0.1

    # Generate arc points
    theta_angles = arange(theta_start, theta_stop + theta_step, theta_step)
    arc_points = []

    # Calculate 3D points for the arc
    for theta in theta_angles:
        # Spherical to Cartesian conversion
        # theta is angle from z-axis (elevation)
        # phi is angle around z-axis (azimuth)
        x = radius * math.sin(theta) * math.cos(phi)
        y = radius * math.sin(theta) * math.sin(phi)
        z = radius * math.cos(theta)
        arc_points.append([x, y, z])

    # Add center point for creating triangular sectors
    center = [0, 0, 0]

    # Draw the arc as a series of triangular sectors
    if picking_mode:
        if len(arc_points) > 1:
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(*center)  # Center vertex
            for point in arc_points:
                glVertex3f(*point)
            glEnd()

    # Draw the arc outline
    if not picking_mode:
        if selected_mode:
            viewer.set_to_selected_color()
        else:
            if ff_request.get('enabled', True):
                glColor4f(0.3, 0.7, 0.3, 0.7)  # Darker red for lines
            else:
                glColor4f(0.6, 0.6, 0.6, 0.7)  # Grey for lines

        glLineWidth(1.0)

        # Draw arc outline
        glBegin(GL_LINE_STRIP)
        for point in arc_points:
            glVertex3f(*point)
        glEnd()

        # Draw radial lines from center to arc endpoints
        glBegin(GL_LINES)
        # Line to start point
        glVertex3f(*center)
        glVertex3f(*arc_points[0])
        # Line to end point
        glVertex3f(*center)
        glVertex3f(*arc_points[-1])
        glEnd()

    # Optional: Draw theta angle indicators
    if not picking_mode and len(arc_points) > 1:
        glLineWidth(1.0)
        # Draw small tick marks at regular intervals
        for i, point in enumerate(arc_points[::max(1, len(arc_points) // theta_angles.shape[0])]):  # Show ~8 ticks max
            tick_inner = [p * 1 for p in point]
            tick_outer = [p * 1.02 for p in point]
            glBegin(GL_LINES)
            glVertex3f(*tick_inner)
            glVertex3f(*tick_outer)
            glEnd()

    # Restore OpenGL state
    if not picking_mode:
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glDisable(GL_POLYGON_OFFSET_FILL)