import gmsh
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QGroupBox, QDialog, QHBoxLayout, QDialogButtonBox,
                               QMessageBox, QComboBox, QFormLayout, QDoubleSpinBox, QWidget, QPushButton, QCheckBox,
                               QSpinBox)
from PySide6.QtCore import Qt


class BiconvexLensCreateDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)

        if data is None:
            self.setWindowTitle("Create Biconvex Lens")
        else:
            self.setWindowTitle("Edit Biconvex Lens")
        self.setModal(True)
        self.resize(350, 300)
        self.setMaximumHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create main form
        self.form = setup_lens_parameters(layout)

        # OK/Cancel buttons (create before connecting signals)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        layout.addWidget(button_box)

        # Connect validation signals
        self.connect_validation_signals()
        self.validate_form()

    def connect_validation_signals(self):
        """Connect signals for form validation"""
        self.form['focal_length'].valueChanged.connect(self.validate_form)
        self.form['R1'].valueChanged.connect(self.validate_form)
        self.form['R2'].valueChanged.connect(self.validate_form)
        self.form['radius'].valueChanged.connect(self.validate_form)
        self.form['thickness'].valueChanged.connect(self.validate_form)
        self.form['ior'].valueChanged.connect(self.validate_form)
        self.form['element_size'].valueChanged.connect(self.validate_form)

    def validate_form(self):
        """Validate form inputs and enable/disable OK button"""
        # Check required fields
        # Common validations
        focal_length_valid = self.form['focal_length'].value() != 0.0  # Can be negative
        radius_valid = self.form['radius'].value() > 0
        thickness_valid = self.form['thickness'].value() > 0
        ior_valid = self.form['ior'].value() >= 1.0

        is_valid = (focal_length_valid and radius_valid and thickness_valid and ior_valid)
        self.ok_button.setEnabled(is_valid)

        # Set tooltip based on validation state
        if not focal_length_valid:
            self.ok_button.setToolTip("Focal length cannot be zero.")
        elif not radius_valid:
            self.ok_button.setToolTip("Lens radius must be greater than 0.")
        elif not thickness_valid:
            self.ok_button.setToolTip("Thickness must be greater than 0.")
        elif not ior_valid:
            self.ok_button.setToolTip("Index of refraction must be ≥ 1.0.")
        else:
            self.ok_button.setToolTip("Ready to create lens.")

    def get_data(self):
        """Return form data"""
        return get_lens_parameters(self.form)

    def accept(self):
        """Override accept to collect form data"""
        try:
            data = self.get_data()
            if data:
                super().accept()
        except Exception as e:
            QMessageBox.warning(self, "Invalid Input",
                                f"Please check your input values:\n{str(e)}")


class BiconvexLensEdit(QGroupBox):
    def __init__(self, callback_fn, parent=None):
        super().__init__(parent)

        self.setTitle("Biconvex Lens")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = setup_lens_parameters(layout)

        # Button
        apply_btn = QPushButton("Apply modifications")
        apply_btn.clicked.connect(callback_fn)
        layout.addWidget(apply_btn)

    def fill(self, data, managers):
        """Fill the form with existing data"""

        if 'focal' in data:
            self.form['focal_length'].setValue(data['focal'] * 1000)  # Convert m to mm
        if 'R1' in data:
            self.form['R1'].setValue(abs(data['R1']) * 1000)  # Convert m to mm
        if 'R2' in data:
            self.form['R2'].setValue(abs(data['R2']) * 1000)  # Convert m to mm
        if 'radius' in data:
            self.form['radius'].setValue(data['radius'] * 1000)  # Convert m to mm
        if 'thickness' in data:
            self.form['thickness'].setValue(data['thickness'] * 1000)  # Convert m to mm
        if 'ior' in data:
            self.form['ior'].setValue(data['ior'])
        if 'element_size' in data:
            self.form['element_size'].setValue(data['element_size'])  # Keep in mm

        # Handle position
        if 'position' in data:
            pos = data['position']
            self.form['position_x'].setValue(pos[0] * 1000)  # Convert m to mm
            self.form['position_y'].setValue(pos[1] * 1000)  # Convert m to mm
            self.form['position_z'].setValue(pos[2] * 1000)  # Convert m to mm

        # Handle rotation (assuming degrees)
        if 'rotation' in data:
            rot = data['rotation']
            self.form['rotation_x'].setValue(rot[0])
            self.form['rotation_y'].setValue(rot[1])
            self.form['rotation_z'].setValue(rot[2])

    def get_parameters(self):
        """Return form parameters"""
        return get_lens_parameters(self.form)

    def update_parameters(self, obj):
        """Set form parameters"""
        obj['parameters'] = get_lens_parameters(self.form)


def get_lens_parameters(form):
    """Get parameters from form"""
    # Base data structure
    data = {
        'focal': form['focal_length'].value() * 1e-3,  # Convert mm to m
        'R1': -form['R1'].value() * 1e-3,  # Convert mm to m
        'R2': -form['R2'].value() * 1e-3,  # Convert mm to m
        'radius': form['radius'].value() * 1e-3,  # Convert mm to m
        'thickness': form['thickness'].value() * 1e-3,  # Convert mm to m
        'ior': form['ior'].value(),
        'element_size': form['element_size'].value(),  # Keep in mm (no conversion)
        'position': (form['position_x'].value() * 1e-3,  # Convert mm to m
                     form['position_y'].value() * 1e-3,  # Convert mm to m
                     form['position_z'].value() * 1e-3  # Convert mm to m
                     ),
        'rotation': (form['rotation_x'].value(),
                     form['rotation_y'].value(),
                     form['rotation_z'].value()
                     )
    }

    return data


def setup_lens_parameters(layout) -> dict:
    """Create the parameter input form"""
    form = {
        'focal_length': QDoubleSpinBox(suffix=' mm', decimals=4, minimum=-10000.0, maximum=10000.0, value=100.0),
        'R1': QDoubleSpinBox(suffix=' mm', decimals=4, minimum=.0, maximum=10000.0, value=0.0),
        'R2': QDoubleSpinBox(suffix=' mm', decimals=4, minimum=.0, maximum=10000.0, value=40.0),
        'radius': QDoubleSpinBox(suffix=' mm', decimals=4, minimum=0.001, maximum=1000.0, value=50.0),
        'thickness': QDoubleSpinBox(suffix=' mm', decimals=4, minimum=0.001, maximum=1000.0, value=13.0),
        'ior': QDoubleSpinBox(decimals=6, minimum=1.0, maximum=10.0, value=1.4),
        'element_size': QDoubleSpinBox(suffix=' mm', minimum=0, maximum=100.0, value=8.0),
        'position_x': QDoubleSpinBox(suffix=' mm', decimals=2, minimum=-10000.0, maximum=10000.0, value=0.0),
        'position_y': QDoubleSpinBox(suffix=' mm', decimals=2, minimum=-10000.0, maximum=10000.0, value=0.0),
        'position_z': QDoubleSpinBox(suffix=' mm', decimals=3, minimum=-10000.0, maximum=10000.0, value=100.0),
        'rotation_x': QDoubleSpinBox(suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
        'rotation_y': QDoubleSpinBox(suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
        'rotation_z': QDoubleSpinBox(suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
    }

    # GroupBox for lens parameters and positioning
    lens_group = QGroupBox("Parameters")
    lens_layout = QFormLayout()

    lens_layout.addRow("Focal length:", form['focal_length'])
    lens_layout.addRow("Radius of curvature R1:", form['R1'])
    lens_layout.addRow("Radius of curvature R2:", form['R2'])
    lens_layout.addRow("Lens radius:", form['radius'])
    lens_layout.addRow("Thickness:", form['thickness'])
    lens_layout.addRow("Index of refraction:", form['ior'])
    lens_layout.addRow("Element size:", form['element_size'])

    lens_group.setLayout(lens_layout)
    layout.addWidget(lens_group)

    # GroupBox for port positioning
    form['port_group'] = QGroupBox("Positioning")
    port_layout = QFormLayout()

    # Position layout
    position_widget = QWidget()
    position_layout = QHBoxLayout(position_widget)
    position_layout.setContentsMargins(0, 0, 0, 0)
    position_layout.addWidget(form['position_x'])
    position_layout.addWidget(form['position_y'])
    position_layout.addWidget(form['position_z'])
    port_layout.addRow("Pos:", position_widget)

    # Rotation layout
    rotation_widget = QWidget()
    rotation_layout = QHBoxLayout(rotation_widget)
    rotation_layout.setContentsMargins(0, 0, 0, 0)
    rotation_layout.addWidget(form['rotation_x'])
    rotation_layout.addWidget(form['rotation_y'])
    rotation_layout.addWidget(form['rotation_z'])
    port_layout.addRow("Rot:", rotation_widget)

    form['port_group'].setLayout(port_layout)
    layout.addWidget(form['port_group'])

    return form


def create_lens_mesh(lens_config):
    # Extract lens parameters
    R1 = lens_config.get('R1', 0.0)  # m (0 means flat)
    R2 = lens_config.get('R2', -0.04)  # m (0 means flat)
    radius = lens_config.get('radius', 0.05)  # m - lens radius
    thickness = lens_config.get('thickness', 0.013)  # m - distance between extremes

    # Lens radius (half of diameter)
    lens_radius = radius / 2.0

    # Initialize Gmsh and suppress logs
    if not gmsh.is_initialized:
        gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.clear()
    gmsh.model.add("Lens")

    # Positions of the faces
    z_face1 = 0.0  # First surface at origin
    z_face2 = thickness  # Second surface

    # Extension to ensure intersections work properly
    extension = lens_radius * 0.1

    # Create main cylinder that defines the lens boundary
    cylinder_height = thickness + 2 * extension
    cylinder_z = z_face1 - extension

    cylinder = gmsh.model.occ.addCylinder(0, 0, cylinder_z, 0, 0, cylinder_height, lens_radius)
    current_volume = [(3, cylinder)]

    # Face 1 (z_min side)
    if R1 != 0:  # Spherical surface
        # Sphere center for face 1
        if R1 > 0:  # Convex (center behind the surface)
            center_z1 = z_face1 - R1
        else:  # Concave (center in front of the surface)
            center_z1 = z_face1 - R1

        # Create sphere with sufficient radius
        sphere_radius = abs(R1)
        sphere1 = gmsh.model.occ.addSphere(0, 0, center_z1, sphere_radius)

        # Intersection with the sphere
        result = gmsh.model.occ.intersect(current_volume, [(3, sphere1)])
        current_volume = result[0]  # Take only the resulting volumes

        # Remove temporary entities
        gmsh.model.occ.remove([(3, sphere1)], True)

    else:
        # Flat surface - cut with a plane
        # Create a box that keeps the cylinder part from z_face1 onwards
        box_size = lens_radius * 2
        cut_box = gmsh.model.occ.addBox(-box_size, -box_size, z_face1,
                                        2 * box_size, 2 * box_size, cylinder_z + cylinder_height - z_face1)

        result = gmsh.model.occ.intersect(current_volume, [(3, cut_box)])
        current_volume = result[0]

        # Remove temporary box
        gmsh.model.occ.remove([(3, cut_box)], True)

    # Check that we still have a volume
    if not current_volume:
        print("Error: No volume after face 1")
        gmsh.finalize()
        return

    # Face 2 (z_max side)
    if R2 != 0:  # Spherical surface
        # Sphere center for face 2
        if R2 > 0:  # Convex (center behind the surface)
            center_z2 = z_face2 + R2
        else:  # Concave (center in front of the surface)
            center_z2 = z_face2 + R2

        # Create sphere
        sphere_radius = abs(R2)
        sphere2 = gmsh.model.occ.addSphere(0, 0, center_z2, sphere_radius)

        # Intersection with the sphere
        result = gmsh.model.occ.intersect(current_volume, [(3, sphere2)])
        current_volume = result[0]

        # Remove temporary sphere
        gmsh.model.occ.remove([(3, sphere2)], True)

    else:
        # Flat surface - cut with a plane
        # Create a box that keeps the cylinder part up to z_face2
        box_size = lens_radius * 2
        cut_box = gmsh.model.occ.addBox(-box_size, -box_size, cylinder_z,
                                        2 * box_size, 2 * box_size, z_face2 - cylinder_z)

        result = gmsh.model.occ.intersect(current_volume, [(3, cut_box)])
        current_volume = result[0]

        # Remove temporary box
        gmsh.model.occ.remove([(3, cut_box)], True)

    # Check that we still have a volume
    if not current_volume:
        print("Error: No volume after face 2")
        gmsh.finalize()
        return

    # Synchronization with Gmsh model
    gmsh.model.occ.synchronize()

    # FORCER l'orientation cohérente de TOUTES les surfaces
    volumes = gmsh.model.getEntities(3)
    for vol in volumes:
        surfaces = gmsh.model.getBoundary([vol], oriented=True)
        for surf in surfaces:
            # Forcer orientation extérieure (normale sortante)
            gmsh.model.setVisibility([surf], True)

    gmsh.model.occ.synchronize()

    # Check that we have a volume
    volumes = gmsh.model.getEntities(3)
    if not volumes:
        print("Error: No volume created!")
        gmsh.finalize()
        return

    # Use MshMesh like in the original code
    from qosm import MshMesh

    mesh = MshMesh()
    element_size = lens_config.get('element_size', 10) * 1e-3
    mesh.load_mesh(element_size, view=False, show_vectors=False)


    return mesh


# Test application
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit


    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Lens Dialog Test")
            self.setGeometry(100, 100, 800, 600)

            # Central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            # Title
            title = QLabel("Lens Parameter Dialog Test")
            title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
            layout.addWidget(title)

            # Test buttons
            button_layout = QHBoxLayout()

            create_dialog_btn = QPushButton("Test Create Lens Dialog")
            create_dialog_btn.clicked.connect(self.test_create_dialog)
            button_layout.addWidget(create_dialog_btn)

            edit_dialog_btn = QPushButton("Test Edit Lens Dialog")
            edit_dialog_btn.clicked.connect(self.test_edit_dialog)
            button_layout.addWidget(edit_dialog_btn)

            layout.addLayout(button_layout)

            # Lens Edit Widget Test
            self.lens_edit = BiconvexLensEdit(self.on_lens_apply)
            layout.addWidget(self.lens_edit)

            # Text area for output
            self.output = QTextEdit()
            self.output.setPlaceholderText("Test results will appear here...")
            self.output.setMaximumHeight(200)
            layout.addWidget(self.output)

            # Fill lens edit with sample data
            self.fill_sample_data()

        def fill_sample_data(self):
            """Fill the lens edit widget with sample data"""
            sample_data = {
                'focal': 0.1,  # 100mm in meters
                'R1': 0.0,  # Flat surface
                'R2': -0.04,  # -40mm in meters
                'radius': 0.025,  # 25mm in meters
                'thickness': 0.013,  # 13mm in meters
                'ior': 1.5,
                'element_size': 5.0,  # 5mm
                'position': (0.01, 0.02, 0.03),  # 10, 20, 30mm in meters
                'rotation': (10.0, 20.0, 30.0)  # degrees
            }
            self.lens_edit.fill(sample_data, None)

        def test_create_dialog(self):
            """Test the create lens dialog"""
            dialog = BiconvexLensCreateDialog(self)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.output.append("=== CREATE LENS DIALOG RESULT ===")
                self.display_lens_data(data)
            else:
                self.output.append("Create dialog cancelled\n")

        def test_edit_dialog(self):
            """Test the edit lens dialog with existing data"""
            # Sample existing data
            existing_data = {
                'focal': 0.05,  # 50mm
                'R1': 0.02,  # 20mm convex
                'R2': -0.03,  # -30mm concave
                'radius': 0.015,  # 15mm
                'thickness': 0.008,  # 8mm
                'ior': 1.52,
                'element_size': 3.0,
                'position': (0.005, 0.0, 0.01),  # 5, 0, 10mm
                'rotation': (0.0, 0.0, 45.0)
            }

            dialog = BiconvexLensCreateDialog(self, existing_data)
            # Fill dialog with existing data
            dialog.form['focal_length'].setValue(existing_data['focal'] * 1000)
            dialog.form['R1'].setValue(existing_data['R1'] * 1000)
            dialog.form['R2'].setValue(existing_data['R2'] * 1000)
            dialog.form['radius'].setValue(existing_data['radius'] * 1000)
            dialog.form['thickness'].setValue(existing_data['thickness'] * 1000)
            dialog.form['ior'].setValue(existing_data['ior'])
            dialog.form['element_size'].setValue(existing_data['element_size'])
            dialog.form['position_x'].setValue(existing_data['position'][0] * 1000)
            dialog.form['position_y'].setValue(existing_data['position'][1] * 1000)
            dialog.form['position_z'].setValue(existing_data['position'][2] * 1000)
            dialog.form['rotation_x'].setValue(existing_data['rotation'][0])
            dialog.form['rotation_y'].setValue(existing_data['rotation'][1])
            dialog.form['rotation_z'].setValue(existing_data['rotation'][2])

            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.output.append("=== EDIT LENS DIALOG RESULT ===")
                self.display_lens_data(data)
            else:
                self.output.append("Edit dialog cancelled\n")

        def on_lens_apply(self):
            """Handle lens edit apply button"""
            data = self.lens_edit.get_parameters()
            self.output.append("=== LENS EDIT WIDGET RESULT ===")
            self.display_lens_data(data)

        def display_lens_data(self, data):
            """Display lens data in a formatted way"""
            self.output.append(f"Focal length: {data['focal'] * 1000:.2f} mm")
            self.output.append(f"R1: {data['R1'] * 1000:.2f} mm")
            self.output.append(f"R2: {data['R2'] * 1000:.2f} mm")
            self.output.append(f"Radius: {data['radius'] * 1000:.2f} mm")
            self.output.append(f"Thickness: {data['thickness'] * 1000:.2f} mm")
            self.output.append(f"Index of refraction: {data['ior']:.6f}")
            self.output.append(f"Element size: {data['element_size']:.1f} mm")
            self.output.append(
                f"Position: ({data['position'][0] * 1000:.2f}, {data['position'][1] * 1000:.2f}, {data['position'][2] * 1000:.2f}) mm")
            self.output.append(
                f"Rotation: ({data['rotation'][0]:.2f}, {data['rotation'][1]:.2f}, {data['rotation'][2]:.2f}) degrees")
            self.output.append("=" * 40 + "\n")


    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())
