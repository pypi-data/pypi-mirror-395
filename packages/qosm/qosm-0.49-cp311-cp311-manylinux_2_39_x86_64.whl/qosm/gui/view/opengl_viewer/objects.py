from qosm.gui.managers import SimulationManager

from qosm.gui.dialogs.objects.LensDialog import create_lens_mesh
from OpenGL.GL import *
from numpy import min, max, zeros_like

def render_grid(viewer, grid, picking_mode=False, selected_mode=False):
    """Render a Grid object as a semi-transparent plane"""
    if grid is None:
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
        if grid['type'] == 'GBE':
            glPolygonOffset(2, 2)
        else:
            glPolygonOffset(.5, .5)

    # Get grid points
    # don't apply translation to grid point as this will be done by opengl
    if grid['type'] == 'GBE':
        points = SimulationManager.gbe_grid_from_parameters(grid, do_translation=False).points.numpy()
    else:
        points = SimulationManager.nf_grid_from_parameters(grid).points.numpy()

    # Calculate bounds for each dimension
    min_coords = min(points, axis=0)
    max_coords = max(points, axis=0)

    # Determine plane type and create corners
    if grid['parameters']['plane'] == 'ZX':
        # ZX plane (Y constant)
        y = points[0, 1]
        corners = [
            [min_coords[0], y, min_coords[2]],
            [max_coords[0], y, min_coords[2]],
            [max_coords[0], y, max_coords[2]],
            [min_coords[0], y, max_coords[2]]
        ]
        normal = [0, 1, 0]
    elif grid['parameters']['plane'] == 'ZY':
        # ZY plane (X constant)
        x = points[0, 0]
        corners = [
            [x, min_coords[1], min_coords[2]],
            [x, max_coords[1], min_coords[2]],
            [x, max_coords[1], max_coords[2]],
            [x, min_coords[1], max_coords[2]]
        ]
        normal = [1, 0, 0]
    else:
        # Fallback to XY plane
        z = points[0, 2] if points.shape[0] > 0 else 0
        corners = [
            [min_coords[0], min_coords[1], z],
            [max_coords[0], min_coords[1], z],
            [max_coords[0], max_coords[1], z],
            [min_coords[0], max_coords[1], z]
        ]
        normal = [0, 0, 1]

    # Draw semi-transparent plane
    if not picking_mode:
        if selected_mode:
            viewer.set_to_selected_color()
        else:
            if grid['type'] == 'GBE':
                glColor4f(0.5, 0.5, 1.0, 0.7)  # Blue when not selected
            else:
                if grid.get('enabled', True):
                    glColor4f(0.5, 1.0, 0.5, 0.3)  # Blue when not selected AND enabled
                else:
                    glColor4f(0.65, 0.65, 0.65, 0.3)  # Grey when not selected AND disabled

    glBegin(GL_QUADS)
    glNormal3f(*normal)
    for corner in corners:
        glVertex3f(*corner)
    glEnd()

    # Optional: Draw grid lines for better visualization
    if not picking_mode:
        if selected_mode:
            viewer.set_to_selected_color()
        else:
            if grid['type'] == 'GBE':
                glColor4f(0.3, 0.3, 0.7, 0.7)  # Darker blue for lines
            else:
                if grid.get('enabled', True):
                    glColor4f(0.3, 0.7, 0.3, 0.7)  # Darker Green for lines
                else:
                    glColor4f(0.6, 0.6, 0.6, 0.7)

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
        glDisable(GL_POLYGON_OFFSET_FILL)

def render_mesh(viewer, obj, picking_mode=False, selected_mode=False, domain_mode=False, show_lines=True):
    """Render a StepMesh object"""
    if obj is None:
        return
    mesh = obj['parameters']

    if not picking_mode:
        # Define material and color (only in normal mode)
        if domain_mode:
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.1, 0.5, 0.3, 1.0])
        elif selected_mode:
            if viewer.object_move_mode:
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.0, 1.0, 1.0, 1.0])
            else:
                viewer.set_to_selected_color()
        else:
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.6, 0.6, 0.6, 1.0])

        # frame transformation already applied by render_transform
        _vertices = mesh['vertices']
        glBegin(GL_TRIANGLES)
        for tri in mesh['triangles']:
            for i in tri:
                normal = mesh['normals'][i] if i < mesh['normals'].shape[0] else (0.0, 0.0, 1.0)
                glNormal3f(*normal)
                glVertex3f(*_vertices[i])
        glEnd()

        if viewer.show_normals:
            render_normals(mesh['vertices'], mesh['normals'])

        # Draw triangle edges (wireframe overlay)
        glDisable(GL_LIGHTING)  # Disable lighting to ensure pure color for lines
        glColor4f(0.0, 0.0, 0.0, .8)  # Black color for edges
        glLineWidth(2.0)

        if show_lines:
            glBegin(GL_LINES)
            for tri in mesh['triangles']:
                i0, i1, i2 = tri
                v0, v1, v2 = _vertices[i0], _vertices[i1], _vertices[i2]

                glVertex3f(*v0)
                glVertex3f(*v1)  # Edge v0-v1
                glVertex3f(*v1)
                glVertex3f(*v2)  # Edge v1-v2
                glVertex3f(*v2)
                glVertex3f(*v0)  # Edge v2-v0
            glEnd()

        glEnable(GL_LIGHTING)  # Re-enable lighting for subsequent objects
    else:
        # Picking mode - no normals needed
        # frame transformation already applied by render_transform
        _vertices = mesh['vertices']
        glBegin(GL_TRIANGLES)
        for tri in mesh['triangles']:
            for i in tri:
                glVertex3f(*_vertices[i])
        glEnd()

def render_lens(viewer, lens_config, picking_mode=False, selected_mode=False, show_lines=True):
    """
    Render a lens object using Gmsh geometry generation

    Args:
        viewer: OpenGL viewer
        lens_config: Dictionary containing lens parameters:
            - R1: float, radius of curvature for first surface (m, 0 means flat)
            - R2: float, radius of curvature for second surface (m, 0 means flat)
            - radius: float, lens radius (m)
            - thickness: float, distance between surfaces (m)
            - focal: float, focal length (m) - optional, for reference
        picking_mode: Boolean, if True render for object picking
        selected_mode: Boolean, if True render with selected colors
    """
    if lens_config is None:
        return

    mesh = create_lens_mesh(lens_config)

    # Create lens object like StepMesh
    lens_obj = {
        'type': 'StepMesh',
        'parameters': {
            'vertices': mesh.vertices,
            'triangles': mesh.triangles,
            'normals': mesh.normals if hasattr(mesh, 'normals') else zeros_like(mesh.vertices)
        }
    }

    # Set material properties for lens rendering:
    if not picking_mode:
        if selected_mode:
            viewer.set_to_selected_color()
        else:
            # Glass-like material properties
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.7, 0.8, 0.9, 0.8])
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.9, 0.9, 0.9, 1.0])
            glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)

    # Render the lens mesh
    render_mesh(viewer, lens_obj, picking_mode, selected_mode, show_lines=show_lines)
    if viewer.show_normals and not picking_mode and hasattr(mesh, 'normals'):
        render_normals(mesh.vertices, mesh.normals, lens_config.get('radius', 0.05) * 0.05)

def render_normals(vertices, normals, scale=0.005):
    """
    Render normal vectors as lines

    Args:
        vertices: numpy array of vertex positions (N, 3)
        normals: numpy array of normal vectors (N, 3)
        scale: float, length of normal lines
    """
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 0.0, 0.0)  # Red color for normals
    glLineWidth(1.0)

    glBegin(GL_LINES)
    for i in range(len(vertices)):
        # Start point (vertex position)
        glVertex3f(vertices[i][0], vertices[i][1], vertices[i][2])

        # End point (vertex + scaled normal)
        end_point = vertices[i] + normals[i] * scale
        glVertex3f(end_point[0], end_point[1], end_point[2])
    glEnd()

    glEnable(GL_LIGHTING)


