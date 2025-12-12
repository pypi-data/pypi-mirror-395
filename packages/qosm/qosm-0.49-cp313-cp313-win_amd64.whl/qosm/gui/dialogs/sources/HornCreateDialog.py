import math

from PySide6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QGroupBox, QDialog, QHBoxLayout, QDialogButtonBox,
                               QMessageBox, QComboBox, QFormLayout, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
                               QPushButton, QSpinBox, QHeaderView, QWidget, QProgressBar, QCheckBox)
from PySide6.QtGui import QDoubleValidator, QPalette
from PySide6.QtCore import Qt
from numpy import sqrt


class HornCreateDialog(QDialog):
    def __init__(self, parent=None, data=None, name=None):
        super().__init__(parent)
        self.data = {}

        if data is None:
            self.setWindowTitle("Create Horn")
        else:
            self.setWindowTitle(f"Edit Horn '{name}'")
        self.setModal(True)
        self.resize(450, 600)

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

        # Connect validation
        self.form['source_name'].textChanged.connect(self.validate_form)

        layout.addWidget(button_box)

        # Connect signals after everything is created
        self.form['shape'].currentTextChanged.connect(self.update_dimension_labels)
        self.form['enable_mode_matching'].toggled.connect(self.update_mode_matching_visibility)
        self.form['waveguide_type'].currentTextChanged.connect(self.update_custom_waveguide_visibility)

        # Initialize visibility
        self.update_dimension_labels()
        self.update_mode_matching_visibility()
        self.update_custom_waveguide_visibility()

        if data:
            self.fill_form(data)

        # Initial validation
        self.validate_form()

    def fill_form(self, data):
        """Fill the form with existing data"""
        if 'source_name' in data:
            self.form['source_name'].setText(data['source_name'])
        if 'frequency_GHz' in data:
            self.form['freq_GHz'].setValue(data['frequency_GHz'])
        if 'shape' in data:
            index = self.form['shape'].findData(data['shape'])
            if index >= 0:
                self.form['shape'].setCurrentIndex(index)
        if 'length' in data:
            self.form['L_mm'].setValue(data['length'] * 1e3)
        if 'a' in data:
            self.form['a_mm'].setValue(data['a'] * 1e3)
        if 'b' in data:
            self.form['b_mm'].setValue(data['b'] * 1e3)
        if 'rot_z_deg' in data:
            self.form['rot_z_deg'].setValue(data['rot_z_deg'])
        if 'radius' in data:
            self.form['a_mm'].setValue(data['radius'] * 1e3)
        if 'enable_mode_matching' in data:
            self.form['enable_mode_matching'].setChecked(data['enable_mode_matching'])
        if 'num_discontinuities' in data:
            self.form['num_discontinuities'].setValue(data['num_discontinuities'])
        if 'waveguide_type' in data:
            index = self.form['waveguide_type'].findData(data['waveguide_type'])
            if index >= 0:
                self.form['waveguide_type'].setCurrentIndex(index)
        if 'custom_wg_a' in data:
            self.form['custom_wg_a'].setValue(data['custom_wg_a'] * 1e3)  # Convert m to mm
        if 'custom_wg_b' in data:
            self.form['custom_wg_b'].setValue(data['custom_wg_b'] * 1e3)  # Convert m to mm

        # Fill modes data
        if 'modes' in data:
            self.populate_modes_table(data['modes'])
            # Update power after loading data
            self.update_power_display()

    def populate_modes_table(self, modes):
        """Populate the modes table with existing data"""
        self.modes_table.setRowCount(0)

        for i, mode in enumerate(modes):
            self.modes_table.insertRow(i)

            # Type (TE/TM)
            type_combo = QComboBox()
            type_combo.addItems(['TE', 'TM'])
            type_combo.setCurrentText(mode.get('type', 'TE'))
            self.modes_table.setCellWidget(i, 0, type_combo)

            # Get indices tuple (m, n)
            indices = mode.get('indices', (0, 1))

            # M index
            m_spinbox = QSpinBox()
            m_spinbox.setRange(0, 99)
            m_spinbox.setValue(indices[0])
            self.modes_table.setCellWidget(i, 1, m_spinbox)

            # N index
            n_spinbox = QSpinBox()
            n_spinbox.setRange(0, 99)
            n_spinbox.setValue(indices[1])
            self.modes_table.setCellWidget(i, 2, n_spinbox)

            # Complex coefficient
            coeff_widget = self.create_complex_widget(mode.get('coefficient', 1.0 + 0j))
            self.modes_table.setCellWidget(i, 3, coeff_widget)

    def create_form(self) -> dict:
        """Create the parameter input form"""
        form = {
            'source_name': QLineEdit(),
            'freq_GHz': QDoubleSpinBox(suffix=' GHz', decimals=3, minimum=0.001, maximum=1000.0, value=275),
            'shape': QComboBox(),
            'a_mm': QDoubleSpinBox(suffix=' mm', decimals=3, minimum=0.01, maximum=1000.0, value=5.6),
            'b_mm': QDoubleSpinBox(suffix=' mm', decimals=3, minimum=0.01, maximum=1000.0, value=5.6),
            'L_mm': QDoubleSpinBox(suffix=' mm', decimals=2, minimum=0.01, maximum=1000.0, value=56.),
            'rot_z_deg': QDoubleSpinBox(suffix=' °', decimals=1, minimum=0, maximum=360, value=45.),
            'enable_mode_matching': QCheckBox(),
            'num_discontinuities': QSpinBox(),
            'waveguide_type': QComboBox(),
            'custom_wg_a': QDoubleSpinBox(),
            'custom_wg_b': QDoubleSpinBox(),
        }

        # Configure mode matching controls
        form['enable_mode_matching'].setText("Enable Mode Matching")
        form['enable_mode_matching'].setChecked(False)
        form['enable_mode_matching'].setVisible(False)  # So far, method not yet available -> future version

        form['num_discontinuities'].setRange(1, 100)
        form['num_discontinuities'].setValue(10)
        form['num_discontinuities'].setSuffix(" steps")

        # Configure custom waveguide dimensions
        form['custom_wg_a'].setSuffix(' mm')
        form['custom_wg_a'].setDecimals(3)
        form['custom_wg_a'].setRange(0.001, 100)
        form['custom_wg_a'].setValue(7.112)  # WR28 default

        form['custom_wg_b'].setSuffix(' mm')
        form['custom_wg_b'].setDecimals(3)
        form['custom_wg_b'].setRange(0.001, 100)
        form['custom_wg_b'].setValue(3.556)  # WR28 default

        # Populate waveguide types for higher frequency bands (Ka, W, D, J and around)
        waveguide_types = [
            ("WR28", "WR28 (26.5-40 GHz) - Ka Band"),
            ("WR22", "WR22 (33-50 GHz) - Q Band"),
            ("WR19", "WR19 (40-60 GHz) - U Band"),
            ("WR15", "WR15 (50-75 GHz) - V Band"),
            ("WR12", "WR12 (60-90 GHz) - E Band"),
            ("WR10", "WR10 (75-110 GHz) - W Band"),
            ("WR8", "WR8 (90-140 GHz) - F Band"),
            ("WR6.5", "WR6.5 (110-170 GHz) - D Band"),
            ("WR5.1", "WR5.1 (140-220 GHz) - G Band"),
            ("WR4.3", "WR4.3 (170-260 GHz) - Y Band"),
            ("WR3.4", "WR3.4 (220-325 GHz) - J Band"),
            ("WR2.8", "WR2.8 (265-400 GHz)"),
            ("WR2.2", "WR2.2 (325-500 GHz)"),
            ("WR1.9", "WR1.9 (400-600 GHz)"),
            ("WR1.5", "WR1.5 (500-750 GHz)"),
            ("WR1.2", "WR1.2 (600-900 GHz)"),
            ("WR1.0", "WR1.0 (750-1100 GHz)"),
            ("CUSTOM", "Custom Dimensions"),
        ]

        for wr_code, description in waveguide_types:
            form['waveguide_type'].addItem(description, wr_code)
        form['waveguide_type'].setCurrentIndex(0)  # Default to WR28 (Ka Band)

        # Source name at the top
        source_group = QGroupBox("Source Information")
        source_layout = QFormLayout()

        form['source_name'].setPlaceholderText("e.g., Horn1")
        source_layout.addRow("Source name:", form['source_name'])

        source_group.setLayout(source_layout)
        self.layout().addWidget(source_group)

        # GroupBox for beam parameters
        params_group = QGroupBox("Horn Parameters")
        params_layout = QFormLayout()

        # Shape selection
        form['shape'].addItem("Rectangular", "rect")
        # form['shape'].addItem("Circular", "circ")   # So far, shape not yet available -> future version
        params_layout.addRow("Shape:", form['shape'])

        # Horn size (in mm)
        self.a_label = QLabel("Width:")
        params_layout.addRow(self.a_label, form['a_mm'])

        self.b_label = QLabel("Height:")
        params_layout.addRow(self.b_label, form['b_mm'])

        self.rot_z_label = QLabel("Rot. z:")
        params_layout.addRow(self.rot_z_label, form['rot_z_deg'])

        # Mode matching controls
        params_layout.addRow("", form['enable_mode_matching'])

        self.length_label = QLabel("Length:")
        params_layout.addRow(self.length_label, form['L_mm'])

        self.discontinuities_label = QLabel("Discontinuities:")
        params_layout.addRow(self.discontinuities_label, form['num_discontinuities'])

        self.waveguide_label = QLabel("Waveguide Type:")
        params_layout.addRow(self.waveguide_label, form['waveguide_type'])

        self.custom_wg_a_label = QLabel("Custom WG Width (a):")
        params_layout.addRow(self.custom_wg_a_label, form['custom_wg_a'])

        self.custom_wg_b_label = QLabel("Custom WG Height (b):")
        params_layout.addRow(self.custom_wg_b_label, form['custom_wg_b'])

        # Frequency [GHz]
        params_layout.addRow("Frequency:", form['freq_GHz'])

        params_group.setLayout(params_layout)
        self.layout().addWidget(params_group)

        # GroupBox for TE/TM modes
        modes_group = QGroupBox("Aperture Modes")
        modes_layout = QVBoxLayout()

        # Create modes table
        self.modes_table = QTableWidget()
        self.modes_table.setColumnCount(4)
        self.modes_table.setHorizontalHeaderLabels(['Type', 'M', 'N', 'Coefficient'])

        # Set column widths
        header = self.modes_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.modes_table.setMinimumHeight(150)

        # Add default TE10 mode
        self.add_mode_row()

        modes_layout.addWidget(self.modes_table)

        # Buttons for adding/removing modes
        modes_buttons_layout = QHBoxLayout()

        add_mode_btn = QPushButton("Add Mode")
        add_mode_btn.clicked.connect(self.add_mode_row)
        modes_buttons_layout.addWidget(add_mode_btn)

        remove_mode_btn = QPushButton("Remove Mode")
        remove_mode_btn.clicked.connect(self.remove_mode_row)
        modes_buttons_layout.addWidget(remove_mode_btn)

        modes_buttons_layout.addStretch()
        modes_layout.addLayout(modes_buttons_layout)

        # Power control section
        power_control_layout = QHBoxLayout()

        # Total power label and display
        power_control_layout.addWidget(QLabel("Total Power:"))

        self.power_label = QLabel("1.000000")
        self.power_label.setStyleSheet("QLabel { font-weight: bold; padding: 5px; background-color: #66bb6a; }")
        self.power_label.setMinimumWidth(80)
        power_control_layout.addWidget(self.power_label)

        power_control_layout.addStretch()
        modes_layout.addLayout(power_control_layout)

        modes_group.setLayout(modes_layout)
        self.layout().addWidget(modes_group)

        return form

    def get_waveguide_dimensions(self, waveguide_type):
        """Get standard waveguide dimensions in meters"""
        # Standard waveguide dimensions (width, height) in mm
        waveguide_dims = {
            "WR28": (7.112, 3.556),
            "WR22": (5.690, 2.845),
            "WR19": (4.775, 2.388),
            "WR15": (3.759, 1.880),
            "WR12": (3.099, 1.549),
            "WR10": (2.540, 1.270),
            "WR8": (2.032, 1.016),
            "WR6.5": (1.651, 0.826),
            "WR5.1": (1.295, 0.648),
            "WR4.3": (1.092, 0.546),
            "WR3.4": (0.864, 0.432),
            "WR2.8": (0.711, 0.356),
            "WR2.2": (0.569, 0.284),
            "WR1.9": (0.483, 0.241),
            "WR1.5": (0.381, 0.191),
            "WR1.2": (0.305, 0.152),
            "WR1.0": (0.254, 0.127),
        }

        if waveguide_type in waveguide_dims:
            width_mm, height_mm = waveguide_dims[waveguide_type]
            return width_mm * 1e-3, height_mm * 1e-3  # Convert mm to meters
        else:
            return None, None

    def update_mode_matching_visibility(self):
        """Update visibility of mode matching controls"""
        is_enabled = self.form['enable_mode_matching'].isChecked()

        # Show/hide length control
        self.length_label.setVisible(is_enabled)
        self.form['L_mm'].setVisible(is_enabled)

        # Show/hide discontinuities control
        self.discontinuities_label.setVisible(is_enabled)
        self.form['num_discontinuities'].setVisible(is_enabled)

        # Show/hide waveguide type control
        self.waveguide_label.setVisible(is_enabled)
        self.form['waveguide_type'].setVisible(is_enabled)

        # Update custom controls based on current state
        self.update_custom_waveguide_visibility()

    def update_custom_waveguide_visibility(self):
        """Update visibility of custom waveguide dimension controls"""
        is_mode_matching_enabled = self.form['enable_mode_matching'].isChecked()
        is_custom_selected = self.form['waveguide_type'].currentData() == "CUSTOM"

        # Show custom controls only if mode matching is enabled AND custom is selected
        show_custom = is_mode_matching_enabled and is_custom_selected

        self.custom_wg_a_label.setVisible(show_custom)
        self.form['custom_wg_a'].setVisible(show_custom)

        self.custom_wg_b_label.setVisible(show_custom)
        self.form['custom_wg_b'].setVisible(show_custom)

    def calculate_total_power(self):
        """Calculate total power of all modes"""
        total_power = 0.0
        for row in range(self.modes_table.rowCount()):
            coeff_widget = self.modes_table.cellWidget(row, 3)
            if coeff_widget:
                coeff = self.get_complex_value(coeff_widget)
                total_power += abs(coeff) ** 2
        return total_power

    def update_power_display(self):
        """Update the power display and validation"""
        # Safety check - only update if power label exists
        if not hasattr(self, 'power_label'):
            return

        total_power = self.calculate_total_power()

        # Update power label
        self.power_label.setText(f"{total_power:.6f}")

        # Change color based on power level
        power_tolerance = 0.01  # 1% tolerance
        if total_power > (1.0 + power_tolerance):
            # Red for over-power
            self.power_label.setStyleSheet("QLabel { font-weight: bold; padding: 5px; background-color: #ff6b6b; }")
        elif abs(total_power - 1.0) <= power_tolerance:
            # Green for essentially 100% power
            self.power_label.setStyleSheet("QLabel { font-weight: bold; padding: 5px; background-color: #66bb6a; }")
        else:
            # Orange for under-power
            self.power_label.setStyleSheet("QLabel { font-weight: bold; padding: 5px; background-color: #ffa726; }")

        # Update form validation
        self.validate_form()

    def update_dimension_labels(self):
        """Update dimension labels based on selected shape"""
        current_shape = self.form['shape'].currentData()

        if current_shape == 'circ':
            self.a_label.setText("Radius:")
            self.b_label.hide()
            self.rot_z_label.hide()
            self.form['b_mm'].hide()
        else:
            self.a_label.setText("Width:")
            self.rot_z_label.show()
            self.b_label.show()
            self.form['b_mm'].show()

    def create_complex_widget(self, initial_value=1.0 + 0j):
        """Create a widget for complex number input"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        # Real part
        real_spinbox = QDoubleSpinBox()
        real_spinbox.setRange(-9999.0, 9999.0)
        real_spinbox.setDecimals(6)
        real_spinbox.setValue(initial_value.real)
        real_spinbox.setObjectName("real")
        real_spinbox.valueChanged.connect(self.update_power_display)
        layout.addWidget(real_spinbox)

        # Plus sign
        plus_label = QLabel("+")
        layout.addWidget(plus_label)

        # Imaginary part
        imag_spinbox = QDoubleSpinBox()
        imag_spinbox.setRange(-9999.0, 9999.0)
        imag_spinbox.setDecimals(6)
        imag_spinbox.setValue(initial_value.imag)
        imag_spinbox.setObjectName("imag")
        imag_spinbox.valueChanged.connect(self.update_power_display)
        layout.addWidget(imag_spinbox)

        # j label
        j_label = QLabel("j")
        layout.addWidget(j_label)

        return widget

    def get_complex_value(self, widget):
        """Extract complex value from complex widget"""
        real_spinbox = widget.findChild(QDoubleSpinBox, "real")
        imag_spinbox = widget.findChild(QDoubleSpinBox, "imag")

        if real_spinbox and imag_spinbox:
            return complex(real_spinbox.value(), imag_spinbox.value())
        return 1.0 + 0j

    def add_mode_row(self):
        """Add a new mode row to the table"""
        row = self.modes_table.rowCount()
        self.modes_table.insertRow(row)

        # Type (TE/TM) combo box
        type_combo = QComboBox()
        type_combo.addItems(['TE', 'TM'])
        self.modes_table.setCellWidget(row, 0, type_combo)

        # M index spin box
        m_spinbox = QSpinBox()
        m_spinbox.setRange(0, 99)
        m_spinbox.setValue(1 if row == 0 else 0)
        self.modes_table.setCellWidget(row, 1, m_spinbox)

        # N index spin box
        n_spinbox = QSpinBox()
        n_spinbox.setRange(0, 99)
        n_spinbox.setValue(0 if row == 0 else 1)
        self.modes_table.setCellWidget(row, 2, n_spinbox)

        # Complex coefficient widget
        default_coeff = 1.0 + 0j if row == 0 else 0.0 + 0j
        coeff_widget = self.create_complex_widget(default_coeff)
        self.modes_table.setCellWidget(row, 3, coeff_widget)

        # Update power after adding new mode
        self.update_power_display()

    def remove_mode_row(self):
        """Remove the selected mode row"""
        current_row = self.modes_table.currentRow()
        if current_row < 0:
            current_row = self.modes_table.rowCount() - 1

        if current_row >= 0 and self.modes_table.rowCount() > 1:
            self.modes_table.removeRow(current_row)
            # Update power after removing mode
            self.update_power_display()
        elif self.modes_table.rowCount() <= 1:
            QMessageBox.information(self, "Cannot Remove", "At least one mode must be present.")

    def get_modes_data(self):
        """Extract modes data from the table"""
        modes = []
        for row in range(self.modes_table.rowCount()):
            type_combo = self.modes_table.cellWidget(row, 0)
            m_spinbox = self.modes_table.cellWidget(row, 1)
            n_spinbox = self.modes_table.cellWidget(row, 2)
            coeff_widget = self.modes_table.cellWidget(row, 3)

            if type_combo and m_spinbox and n_spinbox and coeff_widget:
                mode = {
                    'type': type_combo.currentText(),
                    'indices': (m_spinbox.value(), n_spinbox.value()),
                    'coefficient': self.get_complex_value(coeff_widget)
                }
                modes.append(mode)
        return modes

    def validate_form(self):
        """Validate form and enable/disable OK button"""
        source_name = self.form['source_name'].text().strip()
        total_power = self.calculate_total_power()

        # Simple validation: just check if source name exists
        # Power validation is now optional (user can decide)
        power_tolerance = 0.01  # 1% tolerance
        is_power_valid = abs(total_power - 1.0) <= power_tolerance

        is_valid = bool(source_name)
        self.ok_button.setEnabled(is_valid and is_power_valid)

        # Show tooltip
        if not source_name:
            self.ok_button.setToolTip("Source name is required.")
        elif not is_power_valid:
            self.ok_button.setToolTip(f"Warning: Total power is {total_power:.3f} (not 100%).")
        else:
            self.ok_button.setToolTip("Ready to create horn.")

    def accept(self):
        """Override accept to collect form data"""
        self.data = {
            "shape": self.form['shape'].currentData(),
            "frequency_GHz": self.form['freq_GHz'].value(),
            "source_name": self.form['source_name'].text().strip(),
            "modes": self.get_modes_data(),
            "enable_mode_matching": self.form['enable_mode_matching'].isChecked(),
        }

        # Add mode matching parameters if enabled
        if self.form['enable_mode_matching'].isChecked():
            self.data['length'] = self.form['L_mm'].value() * 1e-3
            self.data['num_discontinuities'] = self.form['num_discontinuities'].value()
            self.data['waveguide_type'] = self.form['waveguide_type'].currentData()

            # Always populate custom_wg_a and custom_wg_b based on selected waveguide type
            if self.form['waveguide_type'].currentData() == "CUSTOM":
                # Use user-specified custom dimensions
                self.data['custom_wg_a'] = self.form['custom_wg_a'].value() * 1e-3  # Convert mm to m
                self.data['custom_wg_b'] = self.form['custom_wg_b'].value() * 1e-3  # Convert mm to m
            else:
                # Use standard waveguide dimensions
                wg_a, wg_b = self.get_waveguide_dimensions(self.form['waveguide_type'].currentData())
                if wg_a is not None and wg_b is not None:
                    self.data['custom_wg_a'] = wg_a
                    self.data['custom_wg_b'] = wg_b

        if self.data['shape'] == 'rect':
            self.data['a'] = self.form['a_mm'].value() * 1e-3
            self.data['b'] = self.form['b_mm'].value() * 1e-3
            self.data['rot_z_deg'] = self.form['rot_z_deg'].value()
        elif self.data['shape'] == 'circ':
            self.data['radius'] = self.form['a_mm'].value() * 1e-3

        super().accept()

    def get_data(self):
        """Return form data"""
        if not self.data:
            return None
        return self.data


def get_all_te_modes(existing_modes, shape, a, b=None, frequency_GHz=10.0):
   """
   Extracts TE modes and sorts them by increasing guided wavenumber.
   Fills with zeros if there are gaps.

   Parameters:
   -----------
   existing_modes : list
       List of modes [{'type': 'TE', 'indices': (m,n), 'coefficient': complex}, ...]
   shape : str
       'rect' for rectangular, 'circ' for circular
   a : float
       Guide width (m) or radius for circular
   b : float, optional
       Guide height (m), required for rectangular
   frequency_GHz : float
       Working frequency in GHz
   max_modes : int
       Maximum number of modes to consider

   Returns:
   --------
   list : [coef_te0, coef_te1, coef_te2, ...] sorted by increasing guided wavenumber
   """

   c = 3e8  # Speed of light (m/s)
   frequency_Hz = frequency_GHz * 1e9
   k0 = 2 * math.pi * frequency_Hz / c  # Wavenumber in vacuum

   # Create a dictionary of existing TE modes
   te_modes_dict = {}
   for mode in existing_modes:
       if mode['type'] == 'TE':
           m, n = mode['indices']
           te_modes_dict[(m, n)] = mode['coefficient']

   # Generate all possible TE modes with their guided wavenumber
   all_te_modes = []

   max_m = max([m for m, n in te_modes_dict.keys()], default=0) + 1
   max_n = max([n for m, n in te_modes_dict.keys()], default=0) + 1

   if shape == 'rect':
       # Rectangular modes
       for m in range(0, max_m):  # Reasonable limit
           for n in range(0, max_n):
               if m > 0 or n > 0:  # At least one non-zero index for TE
                   # Cutoff frequency
                   fc = (c / (2 * math.pi)) * math.sqrt((m * math.pi / a) ** 2 + (n * math.pi / b) ** 2)

                   # Guided wavenumber
                   beta = sqrt(k0 ** 2 - (2 * math.pi * fc / c) ** 2 + 0j)

                   all_te_modes.append({
                       'indices': (m, n),
                       'guided_wavenumber': beta,
                       'coefficient': te_modes_dict.get((m, n), 0.0 + 0j)
                   })

   elif shape == 'circ':
       # Circular modes - simple approximation with first Bessel zeros
       te_zeros = {
           0: [3.832, 7.016, 10.174, 13.324, 16.471],
           1: [1.841, 5.331, 8.536, 11.706, 14.864],
           2: [3.054, 6.706, 9.970, 13.170, 16.348],
           3: [4.201, 8.015, 11.346, 14.586, 17.789],
           4: [5.318, 9.282, 12.682, 15.964, 19.196],
       }

       for m in range(max_m):
           for n in range(1, max_n):
               if m < len(te_zeros) and n <= len(te_zeros[m]):
                   chi_mn = te_zeros[m][n - 1]
                   fc = (c * chi_mn) / (2 * math.pi * a)

                   beta = sqrt(k0 ** 2 - (2 * math.pi * fc / c) ** 2 + 0j)

                   all_te_modes.append({
                       'indices': (m, n),
                       'guided_wavenumber': beta,
                       'coefficient': te_modes_dict.get((m, n), 0.0 + 0j)
                   })

   # Sort by increasing guided wavenumber
   all_te_modes.sort(key=lambda x: (abs(x['guided_wavenumber']), x['indices']))
   all_te_modes = [mode for mode in all_te_modes if mode['guided_wavenumber'].real > 0]
   all_te_modes = [mode for mode in all_te_modes if abs(mode['coefficient']) > 0]

   # Extract only the coefficients
   coefficients = [mode['coefficient'] for mode in all_te_modes]

   return coefficients, all_te_modes

# Test application
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit


    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Horn Dialog Test")
            self.setGeometry(100, 100, 600, 400)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            # Button to open create dialog
            create_btn = QPushButton("Create New Horn")
            create_btn.clicked.connect(self.create_horn)
            layout.addWidget(create_btn)

            # Button to open edit dialog
            edit_btn = QPushButton("Edit Existing Horn")
            edit_btn.clicked.connect(self.edit_horn)
            layout.addWidget(edit_btn)

            # Text area to display results
            self.result_text = QTextEdit()
            self.result_text.setReadOnly(True)
            layout.addWidget(self.result_text)

        def create_horn(self):
            dialog = HornCreateDialog(self)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.display_result("Created Horn", data)

        def edit_horn(self):
            # Sample existing data
            existing_data = {
                'source_name': 'TestHorn',
                'frequency_GHz': 12.5,
                'shape': 'rect',
                'a': 0.015,  # 15mm
                'b': 0.015,  # 12mm
                'enable_mode_matching': True,
                'length': 0.08,  # 80mm
                'num_discontinuities': 15,
                'waveguide_type': 'WR28',
                'modes': [
                    {'type': 'TE', 'indices': (1, 0), 'coefficient': 0.707 + 0j},
                    {'type': 'TE', 'indices': (0, 1), 'coefficient': 0.707 + 0j},
                    {'type': 'TM', 'indices': (1, 1), 'coefficient': 0.3 + 0.3j}
                ]
            }

            res = get_all_te_modes(existing_modes=existing_data['modes'], shape=existing_data['shape'],
                                   a=existing_data['a'], b=existing_data['b'],
                                   frequency_GHz=existing_data['frequency_GHz'])
            print(res)

            dialog = HornCreateDialog(self, existing_data)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                self.display_result("Edited Horn", data)

        def display_result(self, title, data):
            result_text = f"\n{title}:\n"
            result_text += f"Source Name: {data['source_name']}\n"
            result_text += f"Shape: {data['shape']}\n"
            result_text += f"Frequency: {data['frequency_GHz']} GHz\n"

            if data.get('enable_mode_matching', False):
                result_text += f"Mode Matching: Enabled\n"
                result_text += f"Length: {data['length'] * 1000:.2f} mm\n"
                result_text += f"Discontinuities: {data['num_discontinuities']}\n"
                result_text += f"Waveguide Type: {data['waveguide_type']}\n"
                if 'custom_wg_a' in data and 'custom_wg_b' in data:
                    result_text += f"Waveguide Width: {data['custom_wg_a'] * 1000:.3f} mm\n"
                    result_text += f"Waveguide Height: {data['custom_wg_b'] * 1000:.3f} mm\n"
            else:
                result_text += f"Mode Matching: Disabled\n"

            if data['shape'] == 'rect':
                result_text += f"Width: {data['a'] * 1000:.2f} mm\n"
                result_text += f"Height: {data['b'] * 1000:.2f} mm\n"
            elif data['shape'] == 'circ':
                result_text += f"Radius: {data['radius'] * 1000:.2f} mm\n"

            result_text += "Modes:\n"
            for mode in data['modes']:
                indices = mode['indices']
                coeff = mode['coefficient']
                if coeff.imag >= 0:
                    coeff_str = f"{coeff.real:.3f}+{coeff.imag:.3f}j"
                else:
                    coeff_str = f"{coeff.real:.3f}{coeff.imag:.3f}j"
                result_text += f"  {mode['type']}{indices[0]}{indices[1]}: {coeff_str}\n"

            self.result_text.append(result_text)


    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())
