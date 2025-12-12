import traceback

import toml
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QGroupBox, QGridLayout, QDialog, QDialogButtonBox,
                               QComboBox, QPushButton, QFormLayout, QCheckBox, QHBoxLayout, QDoubleSpinBox, QSpinBox,
                               QFileDialog, QMessageBox)
from PySide6.QtCore import QLocale
import json
import numpy as np

from qosm.gui.managers.GBTCSimulationManager import GBTCSimulationManager
from qosm.utils.toml_config import prepare_config_for_toml, save_config_to_toml


class GBTCRequestCreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create GBTC Request")
        self.setModal(True)
        self.resize(450, 450)  # Increased height for new options

        # Link objects
        object_manager = parent.object_manager if hasattr(parent, "object_manager") else None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set fields and combobox
        self.form = setup_gbtc_request_parameters(layout)
        prepare_gbtc_request_parameters(self.form, object_manager)

        # Connect calibration change signal to show/hide TRL options
        self.form['calibration'].currentTextChanged.connect(self.on_calibration_changed)

        # Create button layout
        button_layout = QHBoxLayout()

        # Add spacer
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # OK/Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        layout.addWidget(button_box)

        # Connect validation signals
        self.connect_validation_signals()

        # Initial calibration setup and validation
        self.on_calibration_changed()
        self.validate_form()

    def on_calibration_changed(self):
        """Show/hide TRL-specific fields based on calibration method"""
        is_trl = self.form['calibration'].currentData() == 'trl'
        self.form['trl_line_offset'].setVisible(is_trl)
        self.form['trl_line_offset_label'].setVisible(is_trl)

    def connect_validation_signals(self):
        """Connect signals for form validation"""
        self.form['port1'].currentTextChanged.connect(self.validate_form)
        self.form['port2'].currentTextChanged.connect(self.validate_form)
        self.form['freq_start'].valueChanged.connect(self.validate_form)
        self.form['freq_stop'].valueChanged.connect(self.validate_form)
        self.form['freq_num_points'].valueChanged.connect(self.validate_form)
        self.form['trl_line_offset'].valueChanged.connect(self.validate_form)

    def validate_form(self):
        """Validate form inputs and enable/disable OK button"""
        # Port 1 validation (mandatory)
        port1_valid = self.form['port1'].currentData() is not None

        # Port 2 validation (mandatory)
        port2_valid = self.form['port2'].currentData() is not None

        # Port validation - same port cannot be in both Port 1 and Port 2
        port1_uuid = self.form['port1'].currentData()
        port2_uuid = self.form['port2'].currentData()
        ports_different = (port1_uuid != port2_uuid if (port1_uuid and port2_uuid) else True)

        # Frequency sweep validation
        freq_start = self.form['freq_start'].value()
        freq_stop = self.form['freq_stop'].value()
        freq_num_points = self.form['freq_num_points'].value()

        freq_valid = (freq_start > 0 and freq_stop > freq_start and freq_num_points >= 2)

        # TRL validation - line offset must be positive when TRL is selected
        trl_valid = True
        if self.form['calibration'].currentData() == 'trl':
            trl_valid = self.form['trl_line_offset'].value() > 0

        # Enable OK button if all validations pass
        is_valid = port1_valid and port2_valid and ports_different and freq_valid and trl_valid

        self.ok_button.setEnabled(is_valid)

        # Set tooltip based on validation state
        if not port1_valid:
            self.ok_button.setToolTip("Port 1 selection is required.")
        elif not port2_valid:
            self.ok_button.setToolTip("Port 2 selection is required.")
        elif not ports_different:
            self.ok_button.setToolTip("Port 1 and Port 2 must be different ports.")
        elif not freq_valid:
            if freq_start <= 0:
                self.ok_button.setToolTip("Start frequency must be greater than 0.")
            elif freq_stop <= freq_start:
                self.ok_button.setToolTip("Stop frequency must be greater than start frequency.")
            else:
                self.ok_button.setToolTip("Number of points must be at least 2.")
        elif not trl_valid:
            self.ok_button.setToolTip("Line offset must be greater than 0 mm for TRL calibration.")
        else:
            self.ok_button.setToolTip("Ready to create GBTC Request.")


    def get_parameters(self):
        try:
            return get_gbtc_request_parameters(self.form)
        except ValueError as e:
            print(e)
            return None


class GBTCRequestEdit(QDialog):
    def __init__(self, callback_fn, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GBTC Request")
        self.setModal(True)
        self.resize(450, 500)  # Increased height for new options
        self.parent = parent
        self.object_manager = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set fields and combobox
        self.form = setup_gbtc_request_parameters(layout)

        # Connect calibration change signal
        self.form['calibration'].currentTextChanged.connect(self.on_calibration_changed)

        # Create button layout
        button_layout = QHBoxLayout()

        # Export configuration button
        self.export_config_btn = QPushButton("Export Config")
        button_layout.addWidget(self.export_config_btn)

        # Add spacer
        button_layout.addStretch()

        # Update button
        request_update = QPushButton("Update")
        request_update.clicked.connect(callback_fn)
        button_layout.addWidget(request_update)

        layout.addLayout(button_layout)

    def on_calibration_changed(self):
        """Show/hide TRL-specific fields based on calibration method"""
        is_trl = self.form['calibration'].currentData() == 'trl'
        self.form['trl_line_offset'].setVisible(is_trl)
        self.form['trl_line_offset_label'].setVisible(is_trl)

    def fill(self, data, managers):
        prepare_gbtc_request_parameters(self.form, managers[0])
        self.object_manager = managers[0]
        try:
            self.export_config_btn.clicked.disconnect()
        except TypeError:
            pass
        self.export_config_btn.clicked.connect(lambda: export_configuration(self, managers))

        # Set Port 1
        if 'port1' in data:
            index = self.form['port1'].findData(data['port1'])
            if index >= 0:
                self.form['port1'].setCurrentIndex(index)

        # Set Port 2
        if 'port2' in data:
            index = self.form['port2'].findData(data['port2'])
            if index >= 0:
                self.form['port2'].setCurrentIndex(index)

        # Set frequency sweep
        if 'frequency_sweep' in data:
            freq_sweep = data['frequency_sweep']
            if 'start' in freq_sweep:
                self.form['freq_start'].setValue(freq_sweep['start'])
            if 'stop' in freq_sweep:
                self.form['freq_stop'].setValue(freq_sweep['stop'])
            if 'num_points' in freq_sweep:
                self.form['freq_num_points'].setValue(freq_sweep['num_points'])

        # Set calibration
        if 'calibration' in data:
            if isinstance(data['calibration'], str):
                # Old format - just the method name
                calib_map = {'norm': 0, 'trl': 1}
                self.form['calibration'].setCurrentIndex(calib_map.get(data['calibration'], 0))
            else:
                # New format - dict with method and TRL parameters
                calib_method = data['calibration'].get('method', 'norm')
                calib_map = {'norm': 0, 'trl': 1}
                self.form['calibration'].setCurrentIndex(calib_map.get(calib_method, 0))

                # Set TRL line offset if present
                if calib_method == 'trl' and 'trl' in data['calibration']:
                    trl_params = data['calibration']['trl']
                    if 'line_offset' in trl_params:
                        self.form['trl_line_offset'].setValue(trl_params['line_offset'] * 1e3)

        # Set analysis options
        if 'analysis_options' in data:
            options = data['analysis_options']
            self.form['compare_plane_wave'].setChecked(options.get('compare_plane_wave', False))
            self.form['thru_line_by_reflection'].setChecked(options.get('thru_line_by_reflection', False))

        # Update TRL visibility after setting calibration
        self.on_calibration_changed()

    def get_parameters(self):
        try:
            return get_gbtc_request_parameters(self.form)
        except ValueError as e:
            print(e)
            return None

    def update_parameters(self, obj):
        obj['parameters'] = get_gbtc_request_parameters(self.form)


def get_gbtc_request_parameters(form):
    calibration_method = form['calibration'].currentData()

    if calibration_method == 'trl':
        calibration = {
            'method': 'trl',
            'trl': {
                'line_offset': form['trl_line_offset'].value() * 1e-3,
                'type_reflector': 'cc'
            }
        }
    else:
        calibration = {
            'method': 'norm'
        }

    return {
        'port1': form['port1'].currentData(),
        'port2': form['port2'].currentData(),
        'frequency_sweep': {
            'start': form['freq_start'].value(),
            'stop': form['freq_stop'].value(),
            'num_points': int(form['freq_num_points'].value())
        },
        'calibration': calibration,
        'analysis_options': {
            'compare_plane_wave': form['compare_plane_wave'].isChecked(),
            'thru_line_by_reflection': form['thru_line_by_reflection'].isChecked()
        }
    }

def export_configuration(self, managers):
    """Export current configuration to JSON file"""
    try:
        # Get current parameters
        params = get_gbtc_request_parameters(self.form)
        if params is None:
            QMessageBox.critical(self, "Export Configuration", "Cannot export invalid configuration.")
            return

        ports_data = [obj for obj in managers[0].objects.values() if obj['type'] == 'GBTCPort']
        sample_data = [obj for obj in managers[0].objects.values() if obj['type'] == 'GBTCSample']
        request_data = {'parameters': params}
        if len(sample_data) == 0:
            QMessageBox.critical(self, "Export Configuration", "Cannot export, GBTC Sample is missing.")

        sim_manager = GBTCSimulationManager(request_data, ports_data, sample_data[0], load_csv=False)

        # Open file dialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export GBTC Configuration",
            "gbtc_config.toml",
            "TOML Files (*.toml);;All Files (*)"
        )

        if filename:
            save_config_to_toml(sim_manager.config, filename, header_comment=None)
            QMessageBox.information(self, "Export Configuration", f"Configuration exported to {filename}")

    except Exception as e:
        traceback.print_exc()
        QMessageBox.critical(self, "Export Configuration", f"Error exporting configuration:\n{str(e)}")

def setup_gbtc_request_parameters(layout) -> dict:
    # Force locale to use dots for decimal separator
    QLocale.setDefault(QLocale.c())

    # Initialization
    form = {
        'port1': QComboBox(),
        'port2': QComboBox(),
        'freq_start': QDoubleSpinBox(prefix='Start: ', suffix=' GHz', decimals=2, minimum=10, maximum=1000.0,
                                     value=220.0),
        'freq_stop': QDoubleSpinBox(prefix='Stop: ', suffix=' GHz', decimals=2, minimum=10, maximum=1000.0,
                                    value=330.0),
        'freq_num_points': QSpinBox(prefix='Num Pts: ', minimum=2, maximum=10000, value=1001),
        'calibration': QComboBox(),
        'trl_line_offset': QDoubleSpinBox(suffix=' mm', decimals=3, minimum=0.001, maximum=1000.0, value=1.0),
        'compare_plane_wave': QCheckBox("Comparison with Plane Wave Model"),
        'thru_line_by_reflection': QCheckBox("Thru & Line obtained by reflection"),
    }

    # Ports group
    ports_group = QGroupBox("Ports")
    ports_layout = QFormLayout()
    ports_group.setLayout(ports_layout)

    ports_layout.addRow(QLabel("Port 1:"), form['port1'])
    ports_layout.addRow(QLabel("Port 2:"), form['port2'])

    layout.addWidget(ports_group)

    # Frequency sweep group
    freq_group = QGroupBox("Frequency Sweep")
    freq_layout = QHBoxLayout()
    freq_group.setLayout(freq_layout)

    freq_layout.addWidget(form['freq_start'])
    freq_layout.addWidget(form['freq_stop'])
    freq_layout.addWidget(form['freq_num_points'])

    layout.addWidget(freq_group)

    # Calibration group
    calib_group = QGroupBox("Calibration")
    calib_layout = QFormLayout()
    calib_group.setLayout(calib_layout)

    # Configure calibration
    form['calibration'].addItem("Norm", 'norm')
    form['calibration'].addItem("TRL", 'trl')

    calib_layout.addRow(QLabel("Method:"), form['calibration'])

    # TRL Line Offset (initially hidden)
    form['trl_line_offset_label'] = QLabel("Line Offset:")
    calib_layout.addRow(form['trl_line_offset_label'], form['trl_line_offset'])

    # Initially hide TRL fields
    form['trl_line_offset'].setVisible(False)
    form['trl_line_offset_label'].setVisible(False)

    layout.addWidget(calib_group)

    # Analysis Options group
    analysis_group = QGroupBox("Analysis Options")
    analysis_layout = QVBoxLayout()
    analysis_group.setLayout(analysis_layout)

    analysis_layout.addWidget(form['compare_plane_wave'])
    analysis_layout.addWidget(form['thru_line_by_reflection'])

    layout.addWidget(analysis_group)

    return form


def prepare_gbtc_request_parameters(form, object_manager):
    """Prepare the form with available GBTC ports"""
    if object_manager is None:
        return

    # Get all GBTC objects
    list_gbtc_objects = object_manager.get_objects_by_type().get('GBTCPort', [])

    # Clear existing items
    form['port1'].clear()
    form['port2'].clear()

    # Port 2 is now mandatory, so no "None" option

    for item_id, item in list_gbtc_objects:
        # Get port name
        port_name = item.get('name', f'Port {item_id[:8]}')

        # Add to both comboboxes
        form['port1'].addItem(port_name, item_id)
        form['port2'].addItem(port_name, item_id)

    # If no ports available, add placeholder for both ports
    if form['port1'].count() == 0:
        form['port1'].addItem("No Ports available", None)
        form['port1'].setEnabled(False)
        form['port2'].addItem("No Ports available", None)
        form['port2'].setEnabled(False)
    else:
        form['port1'].setEnabled(True)
        form['port2'].setEnabled(True)


# Test application
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit


    class MockObjectManager:
        def get_objects_by_type(self):
            return {
                'GBTCPort': [
                    ("12345678-1234-1234-1234-123456789abc", {
                        "name": "GBTC Port 1",
                        "parameters": {
                            "beam": {"w0": 0.01, "z0": 0.0},
                            "lenses": [{"focal": 0.1}]
                        }
                    }),
                    ("87654321-4321-4321-4321-cba987654321", {
                        "name": "GBTC Port 2",
                        "parameters": {
                            "beam": {"w0": 0.008, "z0": 0.0},
                            "lenses": [{"focal": 0.15}]
                        }
                    }),
                    ("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", {
                        "name": "GBTC Port 3",
                        "parameters": {
                            "beam": {"w0": 0.012, "z0": 0.0},
                            "lenses": [{"focal": 0.12}]
                        }
                    })
                ]
            }


    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("GBTC Request Dialog Test")
            self.setGeometry(100, 100, 600, 400)

            # Mock object manager
            self.object_manager = MockObjectManager()

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            # Button to open create dialog
            create_btn = QPushButton("Create New GBTC Request")
            create_btn.clicked.connect(self.create_request)
            layout.addWidget(create_btn)

            # Button to open edit dialog
            edit_btn = QPushButton("Edit Existing GBTC Request")
            edit_btn.clicked.connect(self.edit_request)
            layout.addWidget(edit_btn)

            # Text area to display results
            self.result_text = QTextEdit()
            self.result_text.setReadOnly(True)
            layout.addWidget(self.result_text)

        def create_request(self):
            dialog = GBTCRequestCreateDialog(self)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_parameters()
                self.display_result("Created GBTC Request", data)

        def edit_request(self):
            # Sample existing data with TRL calibration and analysis options
            existing_data = {
                'port1': '12345678-1234-1234-1234-123456789abc',
                'port2': '87654321-4321-4321-4321-cba987654321',
                'frequency_sweep': {
                    'start': 240.0,
                    'stop': 350.0,
                    'num_points': 501
                },
                'calibration': {
                    'method': 'trl',
                    'trl': {
                        'line_offset': 2.5,
                        'type_reflector': 'cc'
                    }
                },
                'analysis_options': {
                    'compare_plane_wave': True,
                    'thru_line_by_reflection': False
                }
            }

            dialog = GBTCRequestEdit(lambda: self.display_result("Updated GBTC Request", dialog.get_parameters()), self)
            dialog.fill(existing_data, [self.object_manager])
            dialog.exec()

        def display_result(self, title, data):
            if data is None:
                self.result_text.append(f"\n{title}: Invalid parameters\n")
                return

            result_text = f"\n{title}:\n"
            result_text += f"Port 1: {data['port1']}\n"
            result_text += f"Port 2: {data['port2']}\n"

            freq = data['frequency_sweep']
            result_text += f"Frequency Sweep:\n"
            result_text += f"  Start: {freq['start']:.2f} GHz\n"
            result_text += f"  Stop: {freq['stop']:.2f} GHz\n"
            result_text += f"  Points: {freq['num_points']}\n"

            calib = data['calibration']
            result_text += f"Calibration Method: {calib['method'].upper()}\n"
            if calib['method'] == 'trl':
                trl_params = calib['trl']
                result_text += f"  Line Offset: {trl_params['line_offset']:.3f} mm\n"
                result_text += f"  Type Reflector: {trl_params['type_reflector']}\n"

            # Display analysis options
            analysis = data.get('analysis_options', {})
            result_text += f"Analysis Options:\n"
            result_text += f"  Compare with Plane Wave Model: {analysis.get('compare_plane_wave', False)}\n"
            result_text += f"  S21 obtained by reflection: {analysis.get('thru_line_by_reflection', False)}\n"

            result_text += f"Raw Data Structure: {data}\n"

            self.result_text.append(result_text)


    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())