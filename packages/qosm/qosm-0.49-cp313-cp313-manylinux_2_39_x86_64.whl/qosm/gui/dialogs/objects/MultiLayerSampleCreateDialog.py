from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox, QDialog, QDialogButtonBox,
                               QMessageBox, QComboBox, QFormLayout, QDoubleSpinBox, QWidget, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox, QFileDialog, QCompleter,
                               QCheckBox)
from PySide6.QtCore import Qt, QLocale
import csv
import numpy as np
import os


class MultiLayerSampleCreateDialog(QDialog):
    def __init__(self, managers, parent=None, data=None):
        super().__init__(parent)

        if data is None:
            self.setWindowTitle("Create MultiLayer Sample")
        else:
            self.setWindowTitle("Edit MultiLayer Sample")
        self.setModal(True)
        self.resize(700, 700)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create main form
        self.form = setup_multilayer_sample_parameters(layout)
        prepare_multilayer_sample_parameters(self.form, managers)

        # OK/Cancel buttons (create before connecting signals)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        layout.addWidget(button_box)

        # Connect validation signals
        self.connect_validation_signals()

        if data:
            self.fill_form(data, managers)

        # Initial validation
        self.validate_form()

    def fill_form(self, data, managers):
        """Fill the form with existing data"""
        prepare_multilayer_sample_parameters(self.form, managers)

        # Handle number of reflections
        if 'num_reflections' in data:
            self.form['num_reflections'].setValue(data['num_reflections'])

        # Handle rotation
        if 'rotation' in data:
            rot = data['rotation']
            if isinstance(rot, (list, tuple)) and len(rot) >= 3:
                self.form['rotation_x'].setValue(rot[0])
                self.form['rotation_y'].setValue(rot[1])
                self.form['rotation_z'].setValue(rot[2])

        # Handle sample offset
        if 'offset' in data:
            offset = data['offset']
            if isinstance(offset, (list, tuple)) and len(offset) >= 3:
                self.form['offset_x'].setValue(offset[0] * 1000)  # Convert m to mm
                self.form['offset_y'].setValue(offset[1] * 1000)  # Convert m to mm
                self.form['offset_z'].setValue(offset[2] * 1000)  # Convert m to mm

        # Handle layers (MUT)
        if 'mut' in data:
            layers = data['mut']
            self.form['layers_table'].setRowCount(len(layers))

            for i, layer in enumerate(layers):
                # CSV Browse button
                browse_btn = QPushButton("\U0001F4C1")
                browse_btn.setFixedWidth(40)
                browse_btn.clicked.connect(lambda checked, row=i: self.browse_csv_for_row(row))
                self.form['layers_table'].setCellWidget(i, 0, browse_btn)

                # Epsilon_r
                epsilon_r = layer.get('epsilon_r', 1.0)
                if isinstance(epsilon_r, str) and epsilon_r.endswith('.csv'):
                    # It's a CSV file path
                    epsilon_str = epsilon_r
                elif isinstance(epsilon_r, complex):
                    epsilon_str = f"{epsilon_r.real:.6g}{epsilon_r.imag:+.6g}j"
                else:
                    epsilon_str = f"{epsilon_r:.6g}"
                self.form['layers_table'].setItem(i, 1, QTableWidgetItem(epsilon_str))

                # Thickness
                thickness = layer.get('thickness', 0.0)
                thickness_str = f"{thickness * 1000:.6g}"  # Convert m to mm
                self.form['layers_table'].setItem(i, 2, QTableWidgetItem(thickness_str))

    def browse_csv_for_row(self, row):
        """Browse CSV file for specific row"""
        # Get current file path if it exists
        current_item = self.form['layers_table'].item(row, 1)
        start_directory = ""

        if current_item and current_item.text().strip():
            current_path = current_item.text().strip()
            # Check if current text is a file path
            if current_path.endswith('.csv'):
                if os.path.exists(current_path):
                    start_directory = os.path.dirname(current_path)
                elif os.path.exists(os.path.dirname(current_path)):
                    start_directory = os.path.dirname(current_path)

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV file for epsilon_r",
            start_directory,
            "CSV files (*.csv);;All files (*)"
        )

        if file_path:
            # Convert to relative path if checkbox is checked
            if self.form['use_relative_paths'].isChecked():
                try:
                    file_path = os.path.relpath(file_path)
                except ValueError:
                    # If relative path conversion fails (different drives on Windows), keep absolute
                    pass
            # Set the CSV file path in the epsilon_r column
            self.form['layers_table'].setItem(row, 1, QTableWidgetItem(file_path))
            self.validate_form()

    def connect_validation_signals(self):
        """Connect signals for form validation"""
        self.form['num_reflections'].valueChanged.connect(self.validate_form)
        self.form['layers_table'].cellChanged.connect(self.validate_form)
        self.form['use_relative_paths'].toggled.connect(self.on_relative_paths_changed)

    def on_relative_paths_changed(self, checked):
        """Convert all CSV paths in table when checkbox is toggled"""
        for row in range(self.form['layers_table'].rowCount()):
            epsilon_item = self.form['layers_table'].item(row, 1)
            if epsilon_item:
                current_path = epsilon_item.text().strip()
                if current_path and current_path.endswith('.csv'):
                    try:
                        if checked:
                            # Convert to relative path
                            if os.path.isabs(current_path):
                                relative_path = os.path.relpath(current_path)
                                epsilon_item.setText(relative_path)
                        else:
                            # Convert to absolute path
                            if not os.path.isabs(current_path):
                                absolute_path = os.path.abspath(current_path)
                                epsilon_item.setText(absolute_path)
                    except (ValueError, OSError):
                        # If conversion fails, keep current path
                        pass

    def validate_form(self):
        """Validate form inputs and enable/disable OK button"""
        # Check if we have at least one layer
        layers_valid = self.form['layers_table'].rowCount() > 0

        # Check if all layers have valid data
        all_layers_valid = True
        for row in range(self.form['layers_table'].rowCount()):
            epsilon_item = self.form['layers_table'].item(row, 1)
            thickness_item = self.form['layers_table'].item(row, 2)

            if not epsilon_item or not thickness_item:
                all_layers_valid = False
                break

            epsilon_text = epsilon_item.text().strip()
            thickness_text = thickness_item.text().strip()

            if not epsilon_text or not thickness_text:
                all_layers_valid = False
                break

            # Try to parse epsilon_r
            try:
                self.parse_epsilon_r(epsilon_text)
            except:
                all_layers_valid = False
                break

            # Try to parse thickness
            try:
                float(thickness_text)
            except:
                all_layers_valid = False
                break

        # Number of reflections validation
        reflections_valid = self.form['num_reflections'].value() >= 0

        # Enable OK button if all validations pass
        is_valid = (layers_valid and all_layers_valid and reflections_valid)

        self.ok_button.setEnabled(is_valid)

        # Update remove button state
        self.update_remove_button_state()

        # Set tooltip based on validation state
        if not layers_valid:
            self.ok_button.setToolTip("At least one layer is required.")
        elif not all_layers_valid:
            self.ok_button.setToolTip("All layers must have valid epsilon_r and thickness values.")
        elif not reflections_valid:
            self.ok_button.setToolTip("Number of reflections must be >= 0.")
        else:
            self.ok_button.setToolTip("Ready to create MultiLayer Sample.")

    def update_remove_button_state(self):
        """Update the remove button state based on number of layers"""
        if hasattr(self.form, 'remove_layer_btn'):
            # Disable remove button if only 1 layer remains
            layer_count = self.form['layers_table'].rowCount()
            self.form['remove_layer_btn'].setEnabled(layer_count > 1)

    def parse_epsilon_r(self, text):
        """Parse epsilon_r from text - can be real number, complex, or CSV file path"""
        text = text.strip().replace(' ', '')

        # Check if it's a file path
        if text.endswith('.csv'):
            return text  # Return file path as-is

        # Try to parse as complex number
        try:
            # Handle different complex number formats
            if 'j' in text or 'i' in text:
                # Replace 'i' with 'j' for Python complex parsing
                text = text.replace('i', 'j')
                return complex(text)
            else:
                # Real number
                return float(text)
        except:
            raise ValueError(f"Invalid epsilon_r format: {text}")

    def get_data(self):
        """Return form data"""
        return get_multilayer_sample_parameters(self.form)

    def accept(self):
        """Override accept to collect form data"""
        try:
            data = self.get_data()
            if data:
                super().accept()
        except Exception as e:
            QMessageBox.warning(self, "Invalid Input",
                                f"Please check your input values:\n{str(e)}")


class MultiLayerSampleEdit(QGroupBox):
    def __init__(self, callback_fn, parent=None):
        super().__init__(parent)

        self.setTitle("MultiLayer Sample")
        self.setWindowTitle('GBTC Multilayer Sample')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = setup_multilayer_sample_parameters(layout)

        # Connect the relative paths checkbox signal
        self.form['use_relative_paths'].toggled.connect(self.on_relative_paths_changed)

        # Button
        apply_btn = QPushButton("Apply modifications")
        apply_btn.clicked.connect(callback_fn)
        layout.addWidget(apply_btn)

    def on_relative_paths_changed(self, checked):
        """Convert all CSV paths in table when checkbox is toggled"""
        for row in range(self.form['layers_table'].rowCount()):
            epsilon_item = self.form['layers_table'].item(row, 1)
            if epsilon_item:
                current_path = epsilon_item.text().strip()
                if current_path and current_path.endswith('.csv'):
                    try:
                        if checked:
                            # Convert to relative path
                            if os.path.isabs(current_path):
                                relative_path = os.path.relpath(current_path)
                                epsilon_item.setText(relative_path)
                        else:
                            # Convert to absolute path
                            if not os.path.isabs(current_path):
                                absolute_path = os.path.abspath(current_path)
                                epsilon_item.setText(absolute_path)
                    except (ValueError, OSError):
                        # If conversion fails, keep current path
                        pass

    def browse_csv_for_row(self, row):
        """Browse CSV file for specific row"""
        # Get current file path if it exists
        current_item = self.form['layers_table'].item(row, 1)
        start_directory = ""

        if current_item and current_item.text().strip():
            current_path = current_item.text().strip()
            # Check if current text is a file path
            if current_path.endswith('.csv'):
                if os.path.exists(current_path):
                    start_directory = os.path.dirname(current_path)
                elif os.path.exists(os.path.dirname(current_path)):
                    start_directory = os.path.dirname(current_path)

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV file for epsilon_r",
            start_directory,
            "CSV files (*.csv);;All files (*)"
        )

        if file_path:
            # Convert to relative path if checkbox is checked
            if self.form['use_relative_paths'].isChecked():
                try:
                    file_path = os.path.relpath(file_path)
                except ValueError:
                    # If relative path conversion fails (different drives on Windows), keep absolute
                    pass
            # Set the CSV file path in the epsilon_r column
            self.form['layers_table'].setItem(row, 1, QTableWidgetItem(file_path))

    def fill(self, data, managers):
        """Fill the form with existing data"""
        prepare_multilayer_sample_parameters(self.form, managers)

        # Handle number of reflections
        if 'num_reflections' in data:
            self.form['num_reflections'].setValue(data['num_reflections'])

        # Handle rotation
        if 'rotation' in data:
            rot = data['rotation']
            if isinstance(rot, (list, tuple)) and len(rot) >= 3:
                self.form['rotation_x'].setValue(rot[0])
                self.form['rotation_y'].setValue(rot[1])
                self.form['rotation_z'].setValue(rot[2])

        # Handle sample offset
        if 'offset' in data:
            offset = data['offset']
            if isinstance(offset, (list, tuple)) and len(offset) >= 3:
                self.form['offset_x'].setValue(offset[0] * 1000)  # Convert m to mm
                self.form['offset_y'].setValue(offset[1] * 1000)  # Convert m to mm
                self.form['offset_z'].setValue(offset[2] * 1000)  # Convert m to mm

        # Handle layers (MUT)
        if 'mut' in data:
            layers = data['mut']
            self.form['layers_table'].setRowCount(len(layers))

            # Check if any paths are relative to set checkbox
            has_relative_paths = any(
                isinstance(layer.get('epsilon_r'), str) and
                layer.get('epsilon_r', '').endswith('.csv') and
                not os.path.isabs(layer.get('epsilon_r', ''))
                for layer in layers
            )
            self.form['use_relative_paths'].setChecked(has_relative_paths)

            for i, layer in enumerate(layers):
                # CSV Browse button
                browse_btn = QPushButton("\U0001F4C1")
                browse_btn.setFixedWidth(40)
                browse_btn.clicked.connect(lambda checked, row=i: self.browse_csv_for_row(row))
                self.form['layers_table'].setCellWidget(i, 0, browse_btn)

                # Epsilon_r
                epsilon_r = layer.get('epsilon_r', 1.0)
                if isinstance(epsilon_r, str) and epsilon_r.endswith('.csv'):
                    # It's a CSV file path
                    epsilon_str = epsilon_r
                elif isinstance(epsilon_r, complex):
                    epsilon_str = f"{epsilon_r.real:.6g}{epsilon_r.imag:+.6g}j"
                else:
                    epsilon_str = f"{epsilon_r:.6g}"
                self.form['layers_table'].setItem(i, 1, QTableWidgetItem(epsilon_str))

                # Thickness
                thickness = layer.get('thickness', 0.0)
                thickness_str = f"{thickness * 1000:.6g}"  # Convert m to mm
                self.form['layers_table'].setItem(i, 2, QTableWidgetItem(thickness_str))

    def get_parameters(self):
        """Return form parameters"""
        return get_multilayer_sample_parameters(self.form)

    def update_parameters(self, obj):
        """Return form parameters"""
        obj['parameters'] = get_multilayer_sample_parameters(self.form)


def get_multilayer_sample_parameters(form):
    """Get parameters from form"""

    # Parse layers from table
    layers = []
    for row in range(form['layers_table'].rowCount()):
        epsilon_item = form['layers_table'].item(row, 1)
        thickness_item = form['layers_table'].item(row, 2)

        if epsilon_item and thickness_item:
            epsilon_text = epsilon_item.text().strip()
            thickness_text = thickness_item.text().strip()

            if epsilon_text and thickness_text:
                # Parse epsilon_r
                if epsilon_text.endswith('.csv'):
                    epsilon_r = epsilon_text  # Keep as file path
                else:
                    epsilon_text = epsilon_text.replace(' ', '')
                    try:
                        if 'j' in epsilon_text or 'i' in epsilon_text:
                            epsilon_text = epsilon_text.replace('i', 'j')
                            epsilon_r = complex(epsilon_text)
                        else:
                            epsilon_r = float(epsilon_text)
                    except:
                        epsilon_r = 1.0

                # Parse thickness
                try:
                    thickness = float(thickness_text) * 1e-3  # Convert mm to m
                except:
                    thickness = 0.0

                layers.append({
                    'epsilon_r': epsilon_r,
                    'thickness': thickness
                })

    # Get rotation vector
    rotation_vector = [
        form['rotation_x'].value(),
        form['rotation_y'].value(),
        form['rotation_z'].value()
    ]

    # Get sample offset vector (convert mm to m)
    offset_vector = [
        form['offset_x'].value() * 1e-3,  # Convert mm to m
        form['offset_y'].value() * 1e-3,  # Convert mm to m
        form['offset_z'].value() * 1e-3  # Convert mm to m
    ]

    return {
        'mut': layers,
        'num_reflections': form['num_reflections'].value(),
        'rotation': rotation_vector,
        'offset': offset_vector
    }


def setup_multilayer_sample_parameters(layout) -> dict:
    """Create the parameter input form"""

    # Force locale to use dots for decimal separator
    QLocale.setDefault(QLocale.c())

    form = {
        'num_reflections': QSpinBox(minimum=0, maximum=100, value=2),
        'rotation_x': QDoubleSpinBox(prefix='rx: ', suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
        'rotation_y': QDoubleSpinBox(prefix='ry: ', suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
        'rotation_z': QDoubleSpinBox(prefix='rz: ', suffix=' °', decimals=2, minimum=-360.0, maximum=360.0, value=0.0),
        'offset_x': QDoubleSpinBox(prefix='x: ', suffix=' mm', decimals=3, minimum=-1000.0, maximum=1000.0, value=0.0),
        'offset_y': QDoubleSpinBox(prefix='y: ', suffix=' mm', decimals=3, minimum=-1000.0, maximum=1000.0, value=0.0),
        'offset_z': QDoubleSpinBox(prefix='z: ', suffix=' mm', decimals=3, minimum=-1000.0, maximum=1000.0, value=0.0),
        'layers_table': QTableWidget(),
        'add_layer_btn': QPushButton("Add Layer"),
        'remove_layer_btn': QPushButton("Remove Layer"),
        'use_relative_paths': QCheckBox("Use relative paths for CSV files")
    }

    # Set locale for all QDoubleSpinBox widgets
    for key, widget in form.items():
        if isinstance(widget, QDoubleSpinBox):
            widget.setLocale(QLocale.c())

    # Set default for relative paths
    form['use_relative_paths'].setChecked(True)

    # GroupBox for sample parameters
    sample_group = QGroupBox("Sample Parameters")
    sample_layout = QFormLayout()

    sample_layout.addRow("Number of Reflections:", form['num_reflections'])

    sample_group.setLayout(sample_layout)
    layout.addWidget(sample_group)

    # GroupBox for rotation
    rotation_group = QGroupBox("Rotation")
    rotation_layout = QHBoxLayout()

    rotation_layout.addWidget(form['rotation_x'])
    rotation_layout.addWidget(form['rotation_y'])
    rotation_layout.addWidget(form['rotation_z'])

    rotation_group.setLayout(rotation_layout)
    layout.addWidget(rotation_group)

    # GroupBox for sample offset
    offset_group = QGroupBox("Offset")
    offset_layout = QHBoxLayout()

    offset_layout.addWidget(form['offset_x'])
    offset_layout.addWidget(form['offset_y'])
    offset_layout.addWidget(form['offset_z'])

    offset_group.setLayout(offset_layout)
    layout.addWidget(offset_group)

    # GroupBox for layers
    layers_group = QGroupBox("Layers (Material Under Test)")
    layers_layout = QVBoxLayout()

    # Add relative paths checkbox
    layers_layout.addWidget(form['use_relative_paths'])

    # Table for layers - 3 columns now
    form['layers_table'].setColumnCount(3)
    form['layers_table'].setHorizontalHeaderLabels(["Load", "Epsilon_r (complex)", "Thickness (mm)"])

    # Configure table to use full width
    header = form['layers_table'].horizontalHeader()

    # Column widths: Browse button (100px), Epsilon_r (stretch), Thickness (120px)
    header.setSectionResizeMode(0, QHeaderView.Fixed)
    header.resizeSection(0, 40)  # Fixed width for browse button

    header.setSectionResizeMode(1, QHeaderView.Stretch)  # Epsilon_r takes remaining space

    header.setSectionResizeMode(2, QHeaderView.Fixed)
    header.resizeSection(2, 120)  # Fixed width for thickness

    # Set minimum height and ensure table stretches
    form['layers_table'].setMinimumHeight(200)
    form['layers_table'].setSizePolicy(form['layers_table'].sizePolicy().horizontalPolicy(),
                                       form['layers_table'].sizePolicy().verticalPolicy())

    layers_layout.addWidget(form['layers_table'])

    # Buttons for layer management
    button_layout = QHBoxLayout()
    button_layout.addWidget(form['add_layer_btn'])
    button_layout.addWidget(form['remove_layer_btn'])
    button_layout.addStretch()

    layers_layout.addLayout(button_layout)
    layers_group.setLayout(layers_layout)
    layout.addWidget(layers_group)

    # Connect button signals
    form['add_layer_btn'].clicked.connect(lambda: add_layer(form))
    form['remove_layer_btn'].clicked.connect(lambda: remove_layer(form))

    # Add initial layer
    add_layer(form)

    return form


def add_layer(form):
    """Add a new layer to the table"""
    current_rows = form['layers_table'].rowCount()
    form['layers_table'].insertRow(current_rows)

    # Add browse button in first column
    browse_btn = QPushButton("\U0001F4C1")
    browse_btn.setFixedWidth(40)
    # We need to get the parent dialog/widget to connect the signal properly
    parent_widget = form['layers_table'].parent()
    while parent_widget and not hasattr(parent_widget, 'browse_csv_for_row'):
        parent_widget = parent_widget.parent()

    if parent_widget and hasattr(parent_widget, 'browse_csv_for_row'):
        browse_btn.clicked.connect(lambda checked, row=current_rows: parent_widget.browse_csv_for_row(row))

    form['layers_table'].setCellWidget(current_rows, 0, browse_btn)

    # Set default values for epsilon_r and thickness
    form['layers_table'].setItem(current_rows, 1, QTableWidgetItem("1.0"))
    form['layers_table'].setItem(current_rows, 2, QTableWidgetItem("1.0"))

    # Update remove button state
    update_remove_button_state(form)


def remove_layer(form):
    """Remove the selected layer from the table"""
    current_row = form['layers_table'].currentRow()

    # Don't allow removal if only 1 layer remains
    if form['layers_table'].rowCount() <= 1:
        QMessageBox.information(None, "Cannot Remove Layer",
                                "At least one layer must be present.")
        return

    if current_row >= 0:
        form['layers_table'].removeRow(current_row)
    else:
        # If no row is selected, remove the last row
        if form['layers_table'].rowCount() > 1:
            form['layers_table'].removeRow(form['layers_table'].rowCount() - 1)

    # Update remove button state
    update_remove_button_state(form)


def update_remove_button_state(form):
    """Update the remove button state based on number of layers"""
    if 'remove_layer_btn' in form:
        # Disable remove button if only 1 layer remains
        layer_count = form['layers_table'].rowCount()
        form['remove_layer_btn'].setEnabled(layer_count > 1)


def prepare_multilayer_sample_parameters(form, managers):
    """Prepare the form with available parameters"""
    # This function is kept for compatibility but no longer does anything
    # since we removed source_port configuration
    pass


# Test application
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit


    class MockObjectManager:
        def get_objects_by_type(self):
            # Mock GBTC Ports for testing
            return {
                'GBTCPort': (
                    ('port-uuid-1', {
                        'name': 'Main TX',
                        'parameters': {
                            'port_type': 'TX Port',
                            'lens': {'focal': 0.1}
                        }}),
                    ('port-uuid-2', {
                        'name': 'RX1',
                        'parameters': {
                            'port_type': 'RX Port',
                            'lens': {'focal': 0.1}
                        }}),
                    ('port-uuid-3', {
                        'name': 'RX1',
                        'parameters': {
                            'port_type': 'TX Port',
                            'source_name': 'Secondary TX',
                            'lens': {'focal': 0.15}
                        }})
                )
            }


    class MockSourceManager:
        def get_sources(self, only_type=None):
            return []


    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("MultiLayer Sample Dialog Test")
            self.setGeometry(100, 100, 900, 600)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            # Button to open create dialog
            create_btn = QPushButton("Create New MultiLayer Sample")
            create_btn.clicked.connect(self.create_sample)
            layout.addWidget(create_btn)

            # Button to open edit dialog
            edit_btn = QPushButton("Edit Existing MultiLayer Sample")
            edit_btn.clicked.connect(self.edit_sample)
            layout.addWidget(edit_btn)

            # Text area to display results
            self.result_text = QTextEdit()
            self.result_text.setReadOnly(True)
            layout.addWidget(self.result_text)

        def create_sample(self):
            managers = [MockObjectManager(), MockSourceManager()]
            dialog = MultiLayerSampleCreateDialog(managers, self)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.display_result("Created MultiLayer Sample", data)

        def edit_sample(self):
            managers = [MockObjectManager(), MockSourceManager()]

            # Sample existing data
            existing_data = {
                'mut': [
                    {
                        'epsilon_r': 2.1,
                        'thickness': 0.001  # 1mm in meters
                    },
                    {
                        'epsilon_r': 30.5 - 16j,
                        'thickness': 0.0006  # 0.6mm in meters
                    }
                ],
                'num_reflections': 3,
                'rotation': [10.0, 20.0, 30.0],
                'offset': [0.001, 0.002, 0.003]  # 1mm, 2mm, 3mm in meters
            }

            dialog = MultiLayerSampleCreateDialog(managers, self, existing_data)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.display_result("Edited MultiLayer Sample", data)

        def display_result(self, title, data):
            result_text = f"\n{title}:\n"
            result_text += f"Number of Reflections: {data['num_reflections']}\n"

            result_text += f"Rotation: [{data['rotation'][0]:.2f}°, {data['rotation'][1]:.2f}°, {data['rotation'][2]:.2f}°]\n"

            result_text += f"Sample Offset: [{data['offset'][0] * 1000:.3f}mm, {data['offset'][1] * 1000:.3f}mm, {data['offset'][2] * 1000:.3f}mm]\n"

            result_text += f"\nLayers ({len(data['mut'])}):\n"
            for i, layer in enumerate(data['mut']):
                result_text += f"  Layer {i + 1}:\n"
                result_text += f"    Epsilon_r: {layer['epsilon_r']}\n"
                result_text += f"    Thickness: {layer['thickness'] * 1000:.4f} mm\n"

            # Display the raw data structure
            result_text += f"\nRaw Data Structure:\n{data}\n"

            self.result_text.append(result_text)


    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())