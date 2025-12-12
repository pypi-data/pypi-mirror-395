from PySide6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QGridLayout,
                               QDialog, QDialogButtonBox, QComboBox, QDoubleSpinBox, QAbstractSpinBox)


class ShapeCreateDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Create Shape")
        self.setModal(True)
        self.resize(400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = setup_shape_parameters(self, layout)

        # Fill form with existing data if provided
        if data:
            fill_shape_form(self.form, data)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_parameters(self):
        return get_shape_parameters(self.form)


class ShapeMeshEdit(QGroupBox):
    def __init__(self, callback_fn):
        super().__init__("Shape Mesh")

        shape_mesh_layout = QVBoxLayout()
        self.setLayout(shape_mesh_layout)

        self.form = setup_shape_parameters(self, shape_mesh_layout)

        # Apply Pose button
        apply_btn = QPushButton("Apply modifications")
        apply_btn.clicked.connect(callback_fn)
        shape_mesh_layout.addWidget(apply_btn)

    def fill(self, data):
        fill_shape_form(self.form, data)

    def get_parameters(self):
        return get_shape_parameters(self.form)


def get_shape_parameters(form):
    try:
        # Get shape type
        shape_type = form['shape']['type_combo_box'].currentData()

        # Get shape-specific parameters as tuple
        shape_params = ()
        if shape_type == "rect":
            shape_params = (
                form['shape']['width'].value() * 1e-3,
                form['shape']['height'].value() * 1e-3
            )
        elif shape_type == "box":
            shape_params = (
                form['shape']['width'].value() * 1e-3,
                form['shape']['height'].value() * 1e-3,
                form['shape']['depth'].value() * 1e-3
            )
        elif shape_type == "disk":
            shape_params = (
                form['shape']['radius_u'].value() * 1e-3,
                form['shape']['radius_v'].value() * 1e-3,
            )
        elif shape_type == "cylinder":
            shape_params = (
                form['shape']['radius'].value() * 1e-3,
                form['shape']['length'].value() * 1e-3
            )
        elif shape_type == "sphere":
            shape_params = (
                form['shape']['radius'].value() * 1e-3,
                form['shape']['angle1'].value(),
                form['shape']['angle2'].value(),
                form['shape']['angle3'].value()
            )

        element_size = form['shape']['element_size'].value()
        if shape_type == 'rect' or shape_type == 'box':
            element_size = 1000.

        return {
            'shape_type': shape_type,
            'shape_params': shape_params,
            'element_size': element_size,
            'position': (
                form['pose']['x'].value() * 1e-3,
                form['pose']['y'].value() * 1e-3,
                form['pose']['z'].value() * 1e-3
            ),
            'rotation': (
                form['pose']['rx'].value(),
                form['pose']['ry'].value(),
                form['pose']['rz'].value()
            ),
            'medium': {
                'type': form['medium']['type_combo_box'].currentIndex(),
                'value': form['medium']['real_part'].value() - 1j * form['medium']['imag_part'].value()
            }
        }
    except ValueError as e:
        print(f"Error parsing parameters: {e}")
        return None


def fill_shape_form(form, data):
    """
    Fill the form with existing data

    Args:
        form: The form dictionary created by setup_shape_parameters
        data: Dictionary containing shape data with keys:
            - 'shape_type': str (rect, box, disk, cylinder, sphere)
            - 'shape_params': tuple of parameters
            - 'position': tuple (x, y, z)
            - 'rotation': tuple (rx, ry, rz)
            - 'medium': dict with 'type' and 'value' keys
    """
    if data is None:
        return

    if 'parameters' in data:
        data = data['parameters']

    try:
        # Set shape type
        shape_type = data.get('shape_type', 'rect')
        combo_box = form['shape']['type_combo_box']
        for i in range(combo_box.count()):
            if combo_box.itemData(i) == shape_type:
                combo_box.setCurrentIndex(i)
                break

        # Set shape parameters based on type
        shape_params = data.get('shape_params', ())
        if shape_type == "rect" and len(shape_params) >= 2:
            form['shape']['width'].setValue(shape_params[0] * 1e3)
            form['shape']['height'].setValue(shape_params[1] * 1e3)
        elif shape_type == "box" and len(shape_params) >= 3:
            form['shape']['width'].setValue(shape_params[0] * 1e3)
            form['shape']['height'].setValue(shape_params[1] * 1e3)
            form['shape']['depth'].setValue(shape_params[2] * 1e3)
        elif shape_type == "disk" and len(shape_params) >= 1:
            form['shape']['radius_u'].setValue(shape_params[0] * 1e3)
            form['shape']['radius_v'].setValue(shape_params[1] * 1e3)
        elif shape_type == "cylinder" and len(shape_params) >= 2:
            form['shape']['radius'].setValue(shape_params[0] * 1e3)
            form['shape']['length'].setValue(shape_params[1] * 1e3)
        elif shape_type == "sphere" and len(shape_params) >= 4:
            form['shape']['radius'].setValue(shape_params[0] * 1e3)
            form['shape']['angle1'].setValue(shape_params[1])
            form['shape']['angle2'].setValue(shape_params[2])
            form['shape']['angle3'].setValue(shape_params[3])

        # Set element size
        element_size = data.get('element_size', 2.0)
        form['shape']['element_size'].setValue(element_size)

        # Set position
        position = data.get('position', (0.0, 0.0, 0.0))
        if len(position) >= 3:
            form['pose']['x'].setValue(position[0] * 1e3)
            form['pose']['y'].setValue(position[1] * 1e3)
            form['pose']['z'].setValue(position[2] * 1e3)

        # Set rotation
        rotation = data.get('rotation', (0.0, 0.0, 0.0))
        if len(rotation) >= 3:
            form['pose']['rx'].setValue(rotation[0])
            form['pose']['ry'].setValue(rotation[1])
            form['pose']['rz'].setValue(rotation[2])

        # Set medium
        medium = data.get('medium', {})
        if 'type' in medium:
            medium_type = medium['type']
            if 0 <= medium_type < form['medium']['type_combo_box'].count():
                form['medium']['type_combo_box'].setCurrentIndex(medium_type)

        if 'value' in medium:
            medium_value = medium['value']
            if isinstance(medium_value, complex):
                form['medium']['real_part'].setValue(medium_value.real)
                form['medium']['imag_part'].setValue(medium_value.imag)
            else:
                # Handle case where value is real number
                form['medium']['real_part'].setValue(medium_value)
                form['medium']['imag_part'].setValue("0.0")

    except (ValueError, KeyError, IndexError) as e:
        print(f"Error filling form: {e}")


def setup_shape_parameters(self, layout) -> dict:
    form = {
        'medium': {
            'type_combo_box': QComboBox(),
            'real_part': QDoubleSpinBox(),
            'imag_part': QDoubleSpinBox(),
        },
        'shape': {
            'type_combo_box': QComboBox(),
            # Parameters for different shapes
            'width': QDoubleSpinBox(),
            'height': QDoubleSpinBox(),
            'depth': QDoubleSpinBox(),
            'radius': QDoubleSpinBox(),
            'radius_u': QDoubleSpinBox(),
            'radius_v': QDoubleSpinBox(),
            'length': QDoubleSpinBox(),
            'angle1': QDoubleSpinBox(),
            'angle2': QDoubleSpinBox(),
            'angle3': QDoubleSpinBox(),
            'element_size': QDoubleSpinBox()
        },
        'pose': {
            'x': QDoubleSpinBox(),
            'y': QDoubleSpinBox(),
            'z': QDoubleSpinBox(),
            'rx': QDoubleSpinBox(),
            'ry': QDoubleSpinBox(),
            'rz': QDoubleSpinBox()
        }
    }

    form['medium']['imag_part'].setDecimals(5)
    form['medium']['imag_part'].setRange(1e-6, 1e31)

    for key, item in form['shape'].items():
        if key == 'type_combo_box':
            continue
        if 'angle' in key:
            item.setSuffix(' °')
            if key == 'angle3':
                item.setRange(0, 360)
            else:
                item.setRange(-90, 90)
        else:
            item.setSuffix(' mm')
            item.setRange(0, 1e4)
        item.setDecimals(3)

    for _, item in form['pose'].items():
        item.setValue(0.)
        item.setDecimals(4)
        item.setRange(-1e4, 1e4)
        item.setButtonSymbols(QAbstractSpinBox.NoButtons)

    def update_shape_parameters():
        """Update visible parameters based on selected shape type"""
        shape_type = form['shape']['type_combo_box'].currentData()

        # Hide all parameter widgets first
        for param_name in ['width', 'height', 'depth', 'radius', 'radius_u', 'radius_v', 'length', 'angle1', 'angle2',
                           'angle3']:
            widget = form['shape'][param_name]
            label = widget.property('label')
            if label:
                label.setVisible(False)
            widget.setVisible(False)

        # Show relevant parameters based on shape type
        if shape_type == "rect":
            form['shape']['width'].setVisible(True)
            form['shape']['width'].property('label').setVisible(True)
            form['shape']['height'].setVisible(True)
            form['shape']['height'].property('label').setVisible(True)
            form['shape']['element_size'].setVisible(False)
            form['shape']['element_size'].property('label').setVisible(False)
        elif shape_type == "box":
            form['shape']['width'].setVisible(True)
            form['shape']['width'].property('label').setVisible(True)
            form['shape']['height'].setVisible(True)
            form['shape']['height'].property('label').setVisible(True)
            form['shape']['depth'].setVisible(True)
            form['shape']['depth'].property('label').setVisible(True)
            form['shape']['element_size'].setVisible(False)
            form['shape']['element_size'].property('label').setVisible(False)
        elif shape_type == "disk":
            form['shape']['radius_u'].setVisible(True)
            form['shape']['radius_u'].property('label').setVisible(True)
            form['shape']['radius_v'].setVisible(True)
            form['shape']['radius_v'].property('label').setVisible(True)
            form['shape']['element_size'].setVisible(True)
            form['shape']['element_size'].property('label').setVisible(True)
        elif shape_type == "cylinder":
            form['shape']['radius'].setVisible(True)
            form['shape']['radius'].property('label').setVisible(True)
            form['shape']['length'].setVisible(True)
            form['shape']['length'].property('label').setVisible(True)
            form['shape']['element_size'].setVisible(True)
            form['shape']['element_size'].property('label').setVisible(True)
        elif shape_type == "sphere":
            form['shape']['radius'].setVisible(True)
            form['shape']['radius'].property('label').setVisible(True)
            form['shape']['angle1'].setVisible(True)
            form['shape']['angle1'].property('label').setVisible(True)
            form['shape']['angle2'].setVisible(True)
            form['shape']['angle2'].property('label').setVisible(True)
            form['shape']['angle3'].setVisible(True)
            form['shape']['angle3'].property('label').setVisible(True)
            form['shape']['element_size'].setVisible(True)
            form['shape']['element_size'].property('label').setVisible(True)

    # Medium group
    medium_group = QGroupBox("Medium")
    medium_layout = QGridLayout()
    medium_group.setLayout(medium_layout)
    layout.addWidget(medium_group)

    type_combo_box = form['medium']['type_combo_box']
    type_combo_box.addItem("Complex permittivity", 0)
    type_combo_box.addItem("Complex IOR", 1)
    type_combo_box.addItem("PEC", 2)
    medium_layout.addWidget(type_combo_box, 0, 0, 1, 4)

    # Set placeholders for medium
    form['medium']['real_part'].setValue(1.0)
    form['medium']['imag_part'].setValue(0.0)
    label1 = QLabel(" - ")
    label2 = QLabel("j")
    label1.setFixedWidth(16)
    label2.setFixedWidth(11)
    medium_layout.addWidget(form['medium']['real_part'], 1, 0)
    medium_layout.addWidget(label1, 1, 1)
    medium_layout.addWidget(form['medium']['imag_part'], 1, 2)
    medium_layout.addWidget(label2, 1, 3)

    def update_medium_parameters():
        hidden = form['medium']['type_combo_box'].currentIndex() == 2
        form['medium']['real_part'].setHidden(hidden)
        form['medium']['imag_part'].setHidden(hidden)
        label1.setHidden(hidden)
        label2.setHidden(hidden)

    type_combo_box.currentTextChanged.connect(update_medium_parameters)

    # Shape group
    shape_group = QGroupBox("Shape")
    shape_layout = QGridLayout()
    shape_group.setLayout(shape_layout)
    layout.addWidget(shape_group)

    # Shape type selection
    shape_type_combo = form['shape']['type_combo_box']
    shape_type_combo.addItem("Plane (Rectangle)", "rect")
    shape_type_combo.addItem("Box", "box")
    shape_type_combo.addItem("Disk", "disk")
    shape_type_combo.addItem("Cylinder", "cylinder")
    shape_type_combo.addItem("Sphere", "sphere")
    shape_type_combo.currentTextChanged.connect(update_shape_parameters)
    shape_layout.addWidget(QLabel("Shape Type:"), 0, 0)
    shape_layout.addWidget(shape_type_combo, 0, 1, 1, 2)

    # Shape parameters (with labels and placeholders)
    row = 1
    parameters = [
        ('width', 'Width:', 70.0),
        ('height', 'Height:', 70.0),
        ('depth', 'Depth:', 10.0),
        ('radius', 'Radius:', 50.0),
        ('radius_u', 'Radius u:', 50.0),
        ('radius_v', 'Radius v:', 50.0),
        ('length', 'Length:', 5.0),
        ('angle1', 'Angle 1:', -90.0),
        ('angle2', 'Angle 2:', 90.0),
        ('angle3', 'Angle 3:', 360.0),
        ('element_size', 'Element size:', 5.0)
    ]

    for param_name, label_text, placeholder in parameters:
        label = QLabel(label_text)
        widget = form['shape'][param_name]
        widget.setValue(placeholder)
        widget.setProperty('label', label)  # Store reference to label
        shape_layout.addWidget(label, row, 0)
        shape_layout.addWidget(widget, row, 1, 1, 2)
        row += 1

    # Initial pose group
    pose_group = QGroupBox("Initial Pose")
    pose_layout = QGridLayout()
    pose_group.setLayout(pose_layout)
    layout.addWidget(pose_group)

    # Position
    pose_layout.addWidget(QLabel("Position (mm):"), 0, 0, 1, 3)
    pose_layout.addWidget(form['pose']['x'], 1, 0)
    pose_layout.addWidget(form['pose']['y'], 1, 1)
    pose_layout.addWidget(form['pose']['z'], 1, 2)

    # Rotation (in degrees)
    pose_layout.addWidget(QLabel("Rotation (°):"), 2, 0, 1, 3)
    pose_layout.addWidget(form['pose']['rx'], 3, 0)
    pose_layout.addWidget(form['pose']['ry'], 3, 1)
    pose_layout.addWidget(form['pose']['rz'], 3, 2)

    # Initialize with default shape (rect)
    update_shape_parameters()

    return form


# Example usage
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Example data for testing the fill function
    test_data = {
        'shape_type': 'box',
        'shape_params': (.0150, .0200, .025),
        'position': (.05, .005, -.003),
        'rotation': (90.0, 45.0, 0.0),
        'medium': {
            'type': 1,
            'value': 1.5 - 0.1j
        }
    }

    dialog = ShapeCreateDialog(data=test_data)

    if dialog.exec() == QDialog.Accepted:
        params = dialog.get_parameters()
        if params:
            print("Shape parameters:", params)
        else:
            print("Invalid parameters")

    sys.exit()