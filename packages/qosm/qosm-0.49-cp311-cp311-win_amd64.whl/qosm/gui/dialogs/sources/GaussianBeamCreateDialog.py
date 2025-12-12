from PySide6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QGroupBox, QDialog, QHBoxLayout, QDialogButtonBox,
                               QMessageBox, QComboBox, QFormLayout, QDoubleSpinBox, QWidget)
from PySide6.QtCore import Qt


class GaussianBeamCreateDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = {}

        if data is None:
            self.setWindowTitle("Create Gaussian Beam")
        else:
            self.setWindowTitle("Edit Gaussian Beam")
        self.setModal(True)
        self.resize(450, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create main form
        self.form = self.create_form()

        # OK/Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        layout.addWidget(button_box)

        # Connect validation signals
        self.connect_validation_signals()

        # Connect polarization change signal
        self.form['pol_combo'].currentTextChanged.connect(self.on_polarization_changed)

        # Initialize visibility
        self.on_polarization_changed(self.form['pol_combo'].currentText())

        if data:
            self.fill_form(data)

        # Initial validation
        self.validate_form()

    def create_form(self) -> dict:
        """Create the parameter input form"""
        form = {
            'source_name': QLineEdit(),
            'w0': QDoubleSpinBox(),
            'z0': QDoubleSpinBox(),
            'frequency_GHz': QDoubleSpinBox(),
            'pol_combo': QComboBox(),
            'pol_x': QDoubleSpinBox(),
            'pol_y': QDoubleSpinBox(),
        }

        # Configure source name
        form['source_name'].setPlaceholderText("e.g., GaussianBeam1")

        # Configure w0 - Waist radius
        form['w0'].setSuffix(' mm')
        form['w0'].setDecimals(4)
        form['w0'].setRange(0.001, 1000.0)
        form['w0'].setValue(2.3)

        # Configure z0 - Waist position offset
        form['z0'].setSuffix(' mm')
        form['z0'].setDecimals(4)
        form['z0'].setRange(-1000.0, 1000.0)
        form['z0'].setValue(0.0)

        # Configure frequency
        form['frequency_GHz'].setSuffix(' GHz')
        form['frequency_GHz'].setDecimals(2)
        form['frequency_GHz'].setRange(0.001, 1000.0)
        form['frequency_GHz'].setValue(275)

        # Configure polarization combo
        form['pol_combo'].addItems(["X", "Y", "Custom"])

        # Configure polarization components
        form['pol_x'].setDecimals(6)
        form['pol_x'].setRange(-1000.0, 1000.0)
        form['pol_x'].setValue(1.0)

        form['pol_y'].setDecimals(6)
        form['pol_y'].setRange(-1000.0, 1000.0)
        form['pol_y'].setValue(0.0)

        # Source name at the top
        source_group = QGroupBox("Source Information")
        source_layout = QFormLayout()
        source_layout.addRow("Source name:", form['source_name'])
        source_group.setLayout(source_layout)
        self.layout().addWidget(source_group)

        # GroupBox for beam parameters
        beam_group = QGroupBox("Gaussian Beam Parameters")
        beam_layout = QFormLayout()

        beam_layout.addRow("Waist radius w0:", form['w0'])
        beam_layout.addRow("Frequency:", form['frequency_GHz'])
        beam_layout.addRow("Waist position offset z0:", form['z0'])

        beam_group.setLayout(beam_layout)
        self.layout().addWidget(beam_group)

        # GroupBox for polarization
        pol_group = QGroupBox("Polarization")
        pol_layout = QVBoxLayout()

        # ComboBox for polarization type
        pol_type_layout = QHBoxLayout()
        pol_type_layout.addWidget(QLabel("Polarization type:"))
        pol_type_layout.addWidget(form['pol_combo'])
        pol_type_layout.addStretch()
        pol_layout.addLayout(pol_type_layout)

        # Custom polarization inputs (initially hidden)
        self.custom_pol_widget = QGroupBox("Custom Polarization Components")
        custom_pol_layout = QFormLayout()

        custom_pol_layout.addRow("X component:", form['pol_x'])
        custom_pol_layout.addRow("Y component:", form['pol_y'])

        self.custom_pol_widget.setLayout(custom_pol_layout)
        self.custom_pol_widget.setVisible(False)  # Initially hidden
        pol_layout.addWidget(self.custom_pol_widget)

        pol_group.setLayout(pol_layout)
        self.layout().addWidget(pol_group)

        return form

    def fill_form(self, data):
        """Fill the form with existing data"""
        if 'source_name' in data:
            self.form['source_name'].setText(data['source_name'])
        if 'w0' in data:
            self.form['w0'].setValue(data['w0'])
            self.form['z0'].setValue(data['z0'] )
        if 'frequency_GHz' in data:
            self.form['frequency_GHz'].setValue(data['frequency_GHz'])

        # Handle polarization
        if 'polarization' in data:
            pol_data = data['polarization']
            if isinstance(pol_data, str):
                # Simple string polarization
                if pol_data == 'X':
                    self.form['pol_combo'].setCurrentText('X')
                elif pol_data == 'Y':
                    self.form['pol_combo'].setCurrentText('Y')
                else:
                    self.form['pol_combo'].setCurrentText('Custom')
            elif isinstance(pol_data, dict):
                # Dictionary polarization
                pol_type = pol_data.get('type', 'Custom')
                if pol_type in ['X', 'Y']:
                    self.form['pol_combo'].setCurrentText(pol_type)
                else:
                    self.form['pol_combo'].setCurrentText('Custom')
                    self.form['pol_x'].setValue(pol_data.get('x', 1.0))
                    self.form['pol_y'].setValue(pol_data.get('y', 0.0))

    def on_polarization_changed(self, text):
        """Handle polarization type change"""
        if text == "Custom":
            self.custom_pol_widget.setVisible(True)
        else:
            self.custom_pol_widget.setVisible(False)
            # Set default values for X and Y polarization
            if text == "X":
                self.form['pol_x'].setValue(1.0)
                self.form['pol_y'].setValue(0.0)
            elif text == "Y":
                self.form['pol_x'].setValue(0.0)
                self.form['pol_y'].setValue(1.0)
        self.validate_form()

    def connect_validation_signals(self):
        """Connect signals for form validation"""
        self.form['source_name'].textChanged.connect(self.validate_form)
        self.form['w0'].valueChanged.connect(self.validate_form)
        self.form['z0'].valueChanged.connect(self.validate_form)
        self.form['frequency_GHz'].valueChanged.connect(self.validate_form)
        self.form['pol_x'].valueChanged.connect(self.validate_form)
        self.form['pol_y'].valueChanged.connect(self.validate_form)
        self.form['pol_combo'].currentTextChanged.connect(self.validate_form)

    def validate_form(self):
        """Validate form inputs and enable/disable OK button"""
        # Check required fields
        source_name_valid = bool(self.form['source_name'].text().strip())
        w0_valid = self.form['w0'].value() > 0
        freq_valid = self.form['frequency_GHz'].value() > 0

        # Check custom polarization if selected
        pol_valid = True
        if self.form['pol_combo'].currentText() == "Custom":
            # Check that at least one component is non-zero
            x_val = self.form['pol_x'].value()
            y_val = self.form['pol_y'].value()
            pol_valid = (x_val != 0.0 or y_val != 0.0)

        # Enable OK button if all validations pass
        is_valid = source_name_valid and w0_valid and freq_valid and pol_valid
        self.ok_button.setEnabled(is_valid)

        # Set tooltip based on validation state
        if not source_name_valid:
            self.ok_button.setToolTip("Source name is required.")
        elif not w0_valid:
            self.ok_button.setToolTip("Waist radius must be greater than 0.")
        elif not freq_valid:
            self.ok_button.setToolTip("Frequency must be greater than 0.")
        elif not pol_valid:
            self.ok_button.setToolTip("At least one polarization component must be non-zero.")
        else:
            self.ok_button.setToolTip("Ready to create Gaussian beam.")

    def accept(self):
        """Override accept to collect form data"""
        try:
            # Get polarization data
            pol_type = self.form['pol_combo'].currentText()
            if pol_type == "X":
                polarization = {"type": "X", "x": 1.0, "y": 0.0}
            elif pol_type == "Y":
                polarization = {"type": "Y", "x": 0.0, "y": 1.0}
            else:  # Custom
                polarization = {
                    "type": "Custom",
                    "x": self.form['pol_x'].value(),
                    "y": self.form['pol_y'].value()
                }

            # Collect all data
            self.data = {
                "source_name": self.form['source_name'].text().strip(),
                "w0": self.form['w0'].value(),
                "z0": self.form['z0'].value(),
                "frequency_GHz": self.form['frequency_GHz'].value(),
                "polarization": polarization
            }

            super().accept()

        except Exception as e:
            QMessageBox.warning(self, "Invalid Input",
                                f"Please check your input values:\n{str(e)}")

    def get_data(self):
        """Return form data"""
        if not self.data:
            return None
        return self.data


# Test application
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit


    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Gaussian Beam Dialog Test")
            self.setGeometry(100, 100, 600, 400)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            # Button to open create dialog
            create_btn = QPushButton("Create New Gaussian Beam")
            create_btn.clicked.connect(self.create_beam)
            layout.addWidget(create_btn)

            # Button to open edit dialog
            edit_btn = QPushButton("Edit Existing Gaussian Beam")
            edit_btn.clicked.connect(self.edit_beam)
            layout.addWidget(edit_btn)

            # Text area to display results
            self.result_text = QTextEdit()
            self.result_text.setReadOnly(True)
            layout.addWidget(self.result_text)

        def create_beam(self):
            dialog = GaussianBeamCreateDialog(self)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.display_result("Created Gaussian Beam", data)

        def edit_beam(self):
            # Sample existing data
            existing_data = {
                'source_name': 'TestBeam',
                'w0': 0.010,  # 10mm in meters
                'z0': 0.005,  # 5mm in meters
                'frequency_GHz': 12.5,
                'polarization': {
                    'type': 'Custom',
                    'x': 0.707,
                    'y': 0.707
                }
            }

            dialog = GaussianBeamCreateDialog(self, existing_data)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.display_result("Edited Gaussian Beam", data)

        def display_result(self, title, data):
            result_text = f"\n{title}:\n"
            result_text += f"Source Name: {data['source_name']}\n"
            result_text += f"Waist Radius: {data['w0'] * 1000:.4f} mm\n"
            result_text += f"Waist Position: {data['z0'] * 1000:.4f} mm\n"
            result_text += f"Frequency: {data['frequency_GHz']:.3f} GHz\n"

            pol = data['polarization']
            result_text += f"Polarization Type: {pol['type']}\n"
            result_text += f"X Component: {pol['x']:.6f}\n"
            result_text += f"Y Component: {pol['y']:.6f}\n"

            self.result_text.append(result_text)


    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())