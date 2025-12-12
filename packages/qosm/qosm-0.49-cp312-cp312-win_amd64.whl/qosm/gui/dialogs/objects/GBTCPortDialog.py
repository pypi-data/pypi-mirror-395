from PySide6.QtWidgets import (QGroupBox, QDialog, QHBoxLayout, QDialogButtonBox, QMessageBox, QFormLayout, QCheckBox,
                               QTableWidget, QDoubleSpinBox, QTableWidgetItem, QHeaderView, QVBoxLayout, QPushButton)


class GBTCPortCreateDialog(QDialog):
    def __init__(self, managers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create GBTC Port")
        self.setModal(True)
        self.resize(600, 700)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create main form
        self.form = setup_gbtc_port_parameters(layout)

        # OK/Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        layout.addWidget(button_box)

        # Connect signals
        self.connect_signals()

        # Initial validation
        self.validate_form()

    def connect_signals(self):
        """Connect all signals"""
        self.form['w0'].valueChanged.connect(self.validate_form)
        self.form['distance_sample_output_lens'].valueChanged.connect(self.validate_form)
        self.form['lenses_table'].cellChanged.connect(self.validate_form)
        self.form['follow_sample'].toggled.connect(self.on_follow_sample_changed)

    def on_follow_sample_changed(self, checked):
        """Handle follow sample checkbox change"""
        self.form['rx'].setEnabled(not checked)
        self.form['ry'].setEnabled(not checked)
        self.form['rz'].setEnabled(not checked)
        if checked:
            self.form['rx'].setValue(0.0)
            self.form['ry'].setValue(0.0)
            self.form['rz'].setValue(0.0)

    def validate_form(self):
        """Validate form inputs and enable/disable OK button"""
        is_valid = True

        # Beam validation
        if self.form['w0'].value() <= 0:
            is_valid = False

        # Distance validation
        if self.form['distance_sample_output_lens'].value() <= 0:
            is_valid = False

        # Lenses validation
        for col in range(self.form['lenses_table'].columnCount()):
            for row in range(7):
                item = self.form['lenses_table'].item(row, col)
                if not item or not item.text().strip():
                    is_valid = False
                    break

                try:
                    value = float(item.text())
                    if row == 0 and value == 0:  # Focal cannot be zero
                        is_valid = False
                        break
                    elif row in [1, 2, 3, 4, 6] and value < 0:  # R1, R2, radius, thickness, distance must be positive
                        is_valid = False
                        break
                    elif row == 5 and value < 1.0:  # IOR must be >= 1.0
                        is_valid = False
                        break
                except ValueError:
                    is_valid = False
                    break

            if not is_valid:
                break

        self.ok_button.setEnabled(is_valid)
        self.update_remove_button_state()

    def update_remove_button_state(self):
        """Update the remove button state"""
        if hasattr(self.form, 'remove_lens_btn'):
            lens_count = self.form['lenses_table'].columnCount()
            self.form['remove_lens_btn'].setEnabled(lens_count > 1)

    def get_data(self):
        """Return form data"""
        return get_gbtc_port_parameters(self.form)

    def accept(self):
        """Override accept to collect form data"""
        try:
            data = self.get_data()
            if data:
                super().accept()
        except Exception as e:
            QMessageBox.warning(self, "Invalid Input", f"Please check your input values:\n{str(e)}")


class GBTCPortEdit(QGroupBox):
    def __init__(self, callback_fn, parent=None):
        super().__init__(parent)
        self.setTitle("GBTC Port")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = setup_gbtc_port_parameters(layout)

        # Connect signals
        self.form['follow_sample'].toggled.connect(self.on_follow_sample_changed)

        # Button
        apply_btn = QPushButton("Apply modifications")
        apply_btn.clicked.connect(callback_fn)
        layout.addWidget(apply_btn)

    def on_follow_sample_changed(self, checked):
        """Handle follow sample checkbox change"""
        self.form['rx'].setEnabled(not checked)
        self.form['ry'].setEnabled(not checked)
        self.form['rz'].setEnabled(not checked)
        if checked:
            self.form['rx'].setValue(0.0)
            self.form['ry'].setValue(0.0)
            self.form['rz'].setValue(0.0)

    def fill(self, data, managers):
        """Fill the form with existing data"""
        # Handle beam parameters
        if 'beam' in data:
            beam_data = data['beam']
            if 'w0' in beam_data:
                self.form['w0'].setValue(beam_data['w0'] * 1000)  # Convert m to mm
            if 'z0' in beam_data:
                self.form['z0'].setValue(beam_data['z0'] * 1000)  # Convert m to mm

        # Handle distance and positioning
        if 'distance_sample_output_lens' in data:
            self.form['distance_sample_output_lens'].setValue(data['distance_sample_output_lens'] * 1000)

        # Handle port offset
        if 'offset' in data:
            offset = data['offset']
            if isinstance(offset, (list, tuple)) and len(offset) >= 3:
                self.form['offset_x'].setValue(offset[0] * 1000)  # Convert m to mm
                self.form['offset_y'].setValue(offset[1] * 1000)  # Convert m to mm
                self.form['offset_z'].setValue(offset[2] * 1000)  # Convert m to mm

        # Handle attitude (backward compatibility with rotation_angle)
        if 'attitude' in data:
            attitude = data['attitude']
            self.form['rx'].setValue(attitude[0])
            self.form['ry'].setValue(attitude[1])
            self.form['rz'].setValue(attitude[2])
        elif 'rotation_angle' in data:
            # Backward compatibility - assume rotation_angle was around Z axis
            self.form['rx'].setValue(0.0)
            self.form['ry'].setValue(0.0)
            self.form['rz'].setValue(data['rotation_angle'])

        if 'follow_sample' in data:
            self.form['follow_sample'].setChecked(data['follow_sample'])

        # Handle lenses
        if 'lenses' in data:
            lenses = data['lenses']
            self.form['lenses_table'].setColumnCount(len(lenses))

            # Set column headers
            headers = [f"Lens {i + 1}" for i in range(len(lenses))]
            self.form['lenses_table'].setHorizontalHeaderLabels(headers)

            for lens_idx, lens in enumerate(lenses):
                # Focal length
                focal = lens.get('focal', 0.1)
                self.form['lenses_table'].setItem(0, lens_idx, QTableWidgetItem(f"{focal * 1000:.4f}"))

                # R1 - use absolute value for display
                R1 = abs(lens.get('R1', 0.0))
                self.form['lenses_table'].setItem(1, lens_idx, QTableWidgetItem(f"{R1 * 1000:.4f}"))

                # R2 - use absolute value for display
                R2 = abs(lens.get('R2', 40.0))
                self.form['lenses_table'].setItem(2, lens_idx, QTableWidgetItem(f"{R2 * 1000:.4f}"))

                # Radius
                radius = lens.get('radius', 50.0)
                self.form['lenses_table'].setItem(3, lens_idx, QTableWidgetItem(f"{radius * 1000:.4f}"))

                # Thickness
                thickness = lens.get('thickness', 13.0)
                self.form['lenses_table'].setItem(4, lens_idx, QTableWidgetItem(f"{thickness * 1000:.4f}"))

                # IOR
                ior = lens.get('ior', 1.4)
                self.form['lenses_table'].setItem(5, lens_idx, QTableWidgetItem(f"{ior:.6f}"))

                # Distance from previous
                distance_from_previous = lens.get('distance_from_previous', 95.0)
                self.form['lenses_table'].setItem(6, lens_idx, QTableWidgetItem(f"{distance_from_previous * 1000:.4f}"))

        # Apply follow sample state
        self.on_follow_sample_changed(self.form['follow_sample'].isChecked())

    def get_parameters(self):
        """Return form parameters"""
        return get_gbtc_port_parameters(self.form)

    def update_parameters(self, obj):
        obj['parameters'] = get_gbtc_port_parameters(self.form)


def get_gbtc_port_parameters(form):
    """Get parameters from form"""
    # Parse lenses from table
    lenses = []
    for col in range(form['lenses_table'].columnCount()):
        items = []
        for row in range(7):
            item = form['lenses_table'].item(row, col)
            if item and item.text().strip():
                try:
                    value = float(item.text())
                    items.append(value)
                except ValueError:
                    items.append(0.0)
            else:
                items.append(0.0)

        if len(items) == 7:
            lens_data = {
                'focal': items[0] * 1e-3,
                'R1': -items[1] * 1e-3,
                'R2': -items[2] * 1e-3,
                'radius': items[3] * 1e-3,
                'thickness': items[4] * 1e-3,
                'ior': items[5],
                'distance_from_previous': items[6] * 1e-3
            }
            lenses.append(lens_data)

    # Get port offset vector (convert mm to m)
    offset_vector = [
        form['offset_x'].value() * 1e-3,  # Convert mm to m
        form['offset_y'].value() * 1e-3,  # Convert mm to m
        form['offset_z'].value() * 1e-3   # Convert mm to m
    ]

    return {
        'beam': {
            'w0': form['w0'].value() * 1e-3,
            'z0': form['z0'].value() * 1e-3
        },
        'distance_sample_output_lens': form['distance_sample_output_lens'].value() * 1e-3,
        'offset': offset_vector,
        'attitude': (form['rx'].value(), form['ry'].value(), form['rz'].value()),
        'follow_sample': form['follow_sample'].isChecked(),
        'lenses': lenses
    }


def setup_gbtc_port_parameters(layout) -> dict:
    """Create the parameter input form"""
    form = {
        'w0': QDoubleSpinBox(suffix=' mm', decimals=4, minimum=0.001, maximum=1000.0, value=10.0),
        'z0': QDoubleSpinBox(suffix=' mm', decimals=4, minimum=-1000.0, maximum=1000.0, value=0.0),
        'distance_sample_output_lens': QDoubleSpinBox(suffix=' mm', decimals=4, minimum=0.001, maximum=10000.0,
                                                      value=100.0),
        'offset_x': QDoubleSpinBox(prefix='x: ', suffix=' mm', decimals=3, minimum=-1000.0, maximum=1000.0, value=0.0),
        'offset_y': QDoubleSpinBox(prefix='y: ', suffix=' mm', decimals=3, minimum=-1000.0, maximum=1000.0, value=0.0),
        'offset_z': QDoubleSpinBox(prefix='z: ', suffix=' mm', decimals=3, minimum=-1000.0, maximum=1000.0, value=0.0),
        'rx': QDoubleSpinBox(prefix='rx: ', suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
        'ry': QDoubleSpinBox(prefix='ry: ', suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
        'rz': QDoubleSpinBox(prefix='rz: ', suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
        'follow_sample': QCheckBox("Follow sample"),
        'lenses_table': QTableWidget(),
        'add_lens_btn': QPushButton("Add Lens"),
        'remove_lens_btn': QPushButton("Remove Lens")
    }

    # Beam parameters
    beam_group = QGroupBox("Beam Parameters")
    beam_layout = QFormLayout()
    beam_layout.addRow("Waist radius w0:", form['w0'])
    beam_layout.addRow("Waist position offset z0:", form['z0'])
    beam_group.setLayout(beam_layout)
    layout.addWidget(beam_group)

    # Positioning
    positioning_group = QGroupBox("Positioning")
    positioning_layout = QFormLayout()
    positioning_layout.addRow("Dist. sample - lens:", form['distance_sample_output_lens'])

    # Port offset row with horizontal layout
    offset_layout = QHBoxLayout()
    offset_layout.addWidget(form['offset_x'])
    offset_layout.addWidget(form['offset_y'])
    offset_layout.addWidget(form['offset_z'])

    positioning_layout.addRow("Port Offset:", offset_layout)

    # Attitude row with horizontal layout
    attitude_layout = QHBoxLayout()
    attitude_layout.addWidget(form['rx'])
    attitude_layout.addWidget(form['ry'])
    attitude_layout.addWidget(form['rz'])

    positioning_layout.addRow("Attitude wrt sample:", attitude_layout)
    positioning_layout.addRow("", form['follow_sample'])
    positioning_group.setLayout(positioning_layout)
    layout.addWidget(positioning_group)

    # Lenses
    lenses_group = QGroupBox("Lenses (distances in mm)")
    lenses_layout = QVBoxLayout()

    # Table setup
    form['lenses_table'].setRowCount(7)
    form['lenses_table'].setColumnCount(1)

    # Row headers
    form['lenses_table'].setVerticalHeaderLabels([
        "Focal", "R1", "R2", "Lens radius",
        "Thickness", "IOR", "Distance from previous"
    ])

    # Column header
    form['lenses_table'].setHorizontalHeaderLabels(["Lens 1"])

    # Configure table
    header = form['lenses_table'].horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)

    form['lenses_table'].verticalHeader().setVisible(True)
    form['lenses_table'].verticalHeader().setFixedWidth(120)
    form['lenses_table'].setMinimumHeight(250)
    form['lenses_table'].setMaximumHeight(300)

    lenses_layout.addWidget(form['lenses_table'])

    # Buttons
    button_layout = QHBoxLayout()
    button_layout.addWidget(form['add_lens_btn'])
    button_layout.addWidget(form['remove_lens_btn'])
    button_layout.addStretch()

    lenses_layout.addLayout(button_layout)
    lenses_group.setLayout(lenses_layout)
    layout.addWidget(lenses_group)

    # Connect button signals
    form['add_lens_btn'].clicked.connect(lambda: add_lens(form))
    form['remove_lens_btn'].clicked.connect(lambda: remove_lens(form))

    # Add initial lens with default values
    default_values = [100.0, 0.0, 40.0, 50.0, 13.0, 1.4, 95.0]
    for row, value in enumerate(default_values):
        form['lenses_table'].setItem(row, 0, QTableWidgetItem(str(value)))

    return form


def add_lens(form):
    """Add a new lens to the table"""
    current_cols = form['lenses_table'].columnCount()
    form['lenses_table'].insertColumn(current_cols)

    # Update headers
    headers = [f"Lens {i + 1}" for i in range(current_cols + 1)]
    form['lenses_table'].setHorizontalHeaderLabels(headers)

    # Set default values
    default_values = [100.0, 0.0, 40.0, 50.0, 13.0, 1.4, 95.0]
    for row, value in enumerate(default_values):
        form['lenses_table'].setItem(row, current_cols, QTableWidgetItem(str(value)))

    # Update remove button state
    update_remove_button_state(form)


def remove_lens(form):
    """Remove the selected lens from the table"""
    current_col = form['lenses_table'].currentColumn()

    if form['lenses_table'].columnCount() <= 1:
        QMessageBox.information(None, "Cannot Remove Lens", "At least one lens must be present.")
        return

    if current_col >= 0:
        form['lenses_table'].removeColumn(current_col)
    else:
        if form['lenses_table'].columnCount() > 1:
            form['lenses_table'].removeColumn(form['lenses_table'].columnCount() - 1)

    # Update headers
    headers = [f"Lens {i + 1}" for i in range(form['lenses_table'].columnCount())]
    form['lenses_table'].setHorizontalHeaderLabels(headers)

    update_remove_button_state(form)


def update_remove_button_state(form):
    """Update the remove button state"""
    if 'remove_lens_btn' in form:
        lens_count = form['lenses_table'].columnCount()
        form['remove_lens_btn'].setEnabled(lens_count > 1)


def prepare_gbtc_port_parameters(form, managers):
    """Prepare the form - kept for compatibility"""
    pass


# Test application
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit


    class MockObjectManager:
        def get_objects_by_type(self):
            return {}


    class MockSourceManager:
        def get_sources(self, only_type=None):
            return []


    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("GBTC Port Dialog Test")
            self.setGeometry(100, 100, 800, 600)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            # Create button
            create_btn = QPushButton("Create New GBTC Port")
            create_btn.clicked.connect(self.create_port)
            layout.addWidget(create_btn)

            # Edit button
            edit_btn = QPushButton("Edit Existing GBTC Port")
            edit_btn.clicked.connect(self.edit_port)
            layout.addWidget(edit_btn)

            # Results
            self.result_text = QTextEdit()
            self.result_text.setReadOnly(True)
            layout.addWidget(self.result_text)

        def create_port(self):
            managers = [MockObjectManager(), MockSourceManager()]
            dialog = GBTCPortCreateDialog(managers, self)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.display_result("Created GBTC Port", data)

        def edit_port(self):
            managers = [MockObjectManager(), MockSourceManager()]

            # Sample data for editing
            existing_data = {
                'beam': {
                    'w0': 0.01,  # 10mm in meters
                    'z0': 0.0
                },
                'distance_sample_output_lens': 0.1,  # 100mm in meters
                'offset': [0.001, 0.002, 0.003],  # 1mm, 2mm, 3mm in meters
                'attitude': (10.0, 20.0, 45.0),
                'follow_sample': True,
                'lenses': [
                    {
                        'focal': 0.1,  # 100mm in meters
                        'R1': 0.0,
                        'R2': -0.04,  # -40mm in meters
                        'radius': 0.05,  # 50mm in meters
                        'thickness': 0.013,  # 13mm in meters
                        'ior': 1.4,
                        'distance_from_previous': 0.095  # 95mm in meters
                    },
                    {
                        'focal': 0.15,  # 150mm in meters
                        'R1': 0.02,  # 20mm in meters
                        'R2': -0.06,  # -60mm in meters
                        'radius': 0.06,  # 60mm in meters
                        'thickness': 0.015,  # 15mm in meters
                        'ior': 1.5,
                        'distance_from_previous': 0.1  # 100mm in meters
                    }
                ]
            }

            # Create edit widget
            edit_widget = GBTCPortEdit(lambda: self.apply_edit(edit_widget), self)
            edit_widget.fill(existing_data, managers)

            # Show in dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit GBTC Port")
            dialog.setModal(True)
            dialog.resize(600, 700)
            dialog_layout = QVBoxLayout(dialog)
            dialog_layout.addWidget(edit_widget)

            if dialog.exec() == QDialog.Accepted:
                data = edit_widget.get_parameters()
                self.display_result("Edited GBTC Port", data)

        def apply_edit(self, edit_widget):
            # Just close the parent dialog
            edit_widget.parent().accept()

        def display_result(self, title, data):
            result_text = f"\n{title}:\n"

            result_text += f"Beam Parameters:\n"
            beam = data['beam']
            result_text += f"  Waist Radius: {beam['w0'] * 1000:.4f} mm\n"
            result_text += f"  Waist Position: {beam['z0'] * 1000:.4f} mm\n"

            result_text += f"\nPositioning:\n"
            result_text += f"  Distance Sample-Output Lens: {data['distance_sample_output_lens'] * 1000:.4f} mm\n"

            offset = data['offset']
            result_text += f"  Port Offset: [{offset[0]*1000:.3f}mm, {offset[1]*1000:.3f}mm, {offset[2]*1000:.3f}mm]\n"

            attitude = data['attitude']
            result_text += f"  Attitude wrt Sample:\n"
            result_text += f"    rx: {attitude[0]:.2f}°\n"
            result_text += f"    ry: {attitude[1]:.2f}°\n"
            result_text += f"    rz: {attitude[2]:.2f}°\n"
            result_text += f"  Follow Sample: {data['follow_sample']}\n"

            result_text += f"\nLenses ({len(data['lenses'])}):\n"
            for i, lens in enumerate(data['lenses']):
                result_text += f"  Lens {i + 1}:\n"
                result_text += f"    Focal: {lens['focal'] * 1000:.4f} mm\n"
                result_text += f"    R1: {lens['R1'] * 1000:.4f} mm\n"
                result_text += f"    R2: {lens['R2'] * 1000:.4f} mm\n"
                result_text += f"    Radius: {lens['radius'] * 1000:.4f} mm\n"
                result_text += f"    Thickness: {lens['thickness'] * 1000:.4f} mm\n"
                result_text += f"    IOR: {lens['ior']:.6f}\n"
                result_text += f"    Distance from Previous: {lens['distance_from_previous'] * 1000:.4f} mm\n"

            # Display the raw data structure
            result_text += f"\nRaw Data Structure:\n{data}\n"

            self.result_text.append(result_text)


    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())